#===============================================================================
# Copyright (c) 2011, Joseph Freeman <jfree143dev AT gmail DOT com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Joseph Freeman nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================

from cps450.oodle.analysis import DepthFirstAdapter
from cps450.oodle.node import Node
from oodle.G import G
from oodle.Declarations import *
from oodle import Type
import os
import subprocess

class CodeGenx86(DepthFirstAdapter):
	'''Generate x86 32-bit assembly code and binaries using GCC'''
	def __init__(self):
		DepthFirstAdapter.__init__(self)
		
		self.asm_list = []          #list of asm instructions
		self.asm_data_list = []     #list of asm instructions in the .data segment
		self.asm_text_list = []     #list of asm instructions in the .text segment
		self.label_counter = 0      #unique counter for label generation

	def prefix(self):
		'''Get the proper prefix for asm variables'''
		return '_'

	def writeAsm(self, asm_str):
		'''add general asm to list'''
		self.asm_list += asm_str.split('\n')

	def writeAsmComment(self, com_str, ln=None):
		'''add general asm comments and line number to list'''
		com_str = com_str.strip().replace('\n', '\n#')
		if ln:
			self.asm_list.append('#Line ' + str(ln) + ': ' + com_str)
		else:
			self.asm_list.append('# ' + com_str)

	def writeAsmData(self, asm_str):
		'''add .data segment asm to list'''
		self.asm_data_list += asm_str.split('\n')

	def writeAsmDataComment(self, com_str, ln=None):
		'''add .data segment asm comments and line number to list'''
		com_str = com_str.strip().replace('\n', '\n#')
		if ln:
			self.asm_data_list.append('#Line ' + str(ln) + ': ' + com_str)
		else:
			self.asm_data_list.append('# ' + com_str)

	def writeAsmText(self, asm_str):
		'''add .text segment asm to list
		   also add tabs to output for prettier printing'''
		self.asm_text_list += ('\t' + asm_str.replace('\n', '\n\t')).split('\n')

	def writeAsmTextFunc(self, func_nm):
		'''add .text segment asm function to list'''
		self.asm_text_list.append('.globl ' + func_nm)
		self.asm_text_list.append('\t.type ' + func_nm + ', @function')
		self.asm_text_list.append(func_nm + ':')

	def writeAsmTextLabel(self, lbl_str):
		'''add .text segment asm labels to list'''
		self.asm_text_list.append(lbl_str + ':')

	def writeAsmTextComment(self, com_str, ln=None):
		'''add .text segment asm comments and line number to list'''
		com_str = com_str.strip().replace('\n', '\n#')
		if ln:
			self.asm_text_list.append('#Line ' + str(ln) + ': ' + com_str)
		else:
			self.asm_text_list.append('# ' + com_str)
	
	def printAsm(self):
		'''print all asm to stdout'''
		for l in self.asm_list:
			print l
		print '\t.data'
		for l in self.asm_data_list:
			print l
		print '\t.text'
		for l in self.asm_text_list:
			print l

	def buildBinary(self, sopt=False):
		'''generate the binary using GCC
		   if -S option is given, the generates a *.s assembly file instead'''
		#make new file with .s extension
		fn = G.options().getFileList()[-1]
		fn = fn[:fn.rfind('.ood')]
		asm_fn = fn + '.s'
		bin_fn = fn
		f = file(asm_fn, 'w')

		
		
		#write asm to .s file
		for l in self.asm_list:
			f.write(l)
			f.write('\n')
		f.write('\t.data\n')
		for l in self.asm_data_list:
			f.write(l)
			f.write('\n')
		f.write('\t.text\n')
		for l in self.asm_text_list:
			f.write(l)
			f.write('\n')
		f.flush()
		
		#compile asm with stdlib.c
		proc = subprocess.Popen(['gcc', '-g', '-m32', '-o', bin_fn, 'stdlib.c', asm_fn])
		proc.wait()
		if proc.stderr:
			print '------------------'
			print 'GCC Error Output:'
			print '------------------'
			print proc.stderr

		if not sopt:
			os.remove(asm_fn)

	def nextLabel(self):
		'''generate a unique label'''
		self.label_counter += 1
		return '.L' + str(self.label_counter)
	
	###########################################################################
	## Methods to help with debugging										 ##
	###########################################################################
	def printFunc(self, f, node=None):
		'''print the name of the node function and its node string
		   only works if 'printDebug()' is enabled'''
		n = (': ' + node.toString().strip()) if node else ''
		if G.options().printDebug():
			print 'CodeGenx86: ' + f.__name__ + n

	###########################################################################
	## Methods to help with querying/modifying the SymbolTable			   ##
	###########################################################################
	def isClassNameUsed(self, nm):
		'''Check whether class name is already used'''
		sym = G.symTab().lookup(nm)
		return sym != None
	
	def isMethodNameUsed(self, nm):
		'''Check whether method name is already used'''
		sym = G.symTab().lookup(nm)
		return sym != None
	
	def isVarNameUsed(self, nm):
		'''Check whether var name is already used'''
		ret = False
		sym = G.symTab().lookup(nm)
		if sym != None:
			ret = ret or isinstance(sym.decl(), ClassDecl)
			#ret = ret or isinstance(sym.decl(), MethodDecl) #FIXME - probably need this
			ret = ret or (isinstance(sym.decl(), VarDecl) and sym.scope() == G.symTab().getScope())
		return ret

	###########################################################################
	## METHOD DECLARATION STUFF											  ##
	###########################################################################
	def inAMethodSig(self, node):
		''''''
		self.printFunc(self.inAMethodSig, node)
		
		ln = node.getId().getLine()
		src = node.toString().strip()
		nm = node.getId().getText()
		
		self.writeAsmTextComment(src, ln)
		self.writeAsmTextFunc(nm)

	def outAMethodSig(self, node):
		''''''
		self.printFunc(self.outAMethodSig, node)
		mem = -4
		vars = node.parent().getVars()
		if vars != None:
			mem = G.symMap()[vars[-1]].decl().offset()
		self.writeAsmText('pushl %ebp')
		self.writeAsmText('movl %esp, %ebp')
		self.writeAsmText('addl $(' + str(mem) + '), %esp')

	def inAMethod(self, node):
		''''''
		self.printFunc(self.inAMethod)

	def outAMethod(self, node):
		''''''
		self.printFunc(self.outAMethod)
		self.writeAsmText('movl -4(%ebp), %eax')  # put return value in %eax
		self.writeAsmText('movl %ebp, %esp')      # delete local variables
		self.writeAsmText('popl %ebp')            # restore old %ebp
		self.writeAsmText('ret')
	
	def outAArgList(self, node):
		''''''
		self.printFunc(self.outAArgList, node)
	
	def outAArgListTail(self, node):
		''''''
		self.printFunc(self.outAArgListTail, node)
	
	def outAArg(self, node):
		''''''
		self.printFunc(self.outAArg, node)
	
	def outAMethodVar(self, node):
		''''''
		self.printFunc(self.outAMethodVar)
	
	
	###########################################################################
	## GENERIC VARIABLE DECLARATION STUFF (also includes method return type) ##
	###########################################################################	
	def outAVar(self, node):
		''''''
		self.printFunc(self.outAVar, node)
	
	def outAVarAssign(self, node):
		''''''
		self.printFunc(self.outAVarAssign, node)

	def outAVarType(self, node):
		''''''
		self.printFunc(self.outAVarType, node)

	def outABoolType(self, node):
		''''''
		self.printFunc(self.outABoolType, node)
	
	def outAIntType(self, node):
		''''''
		self.printFunc(self.outAIntType, node)
		
	def outAStringType(self, node):
		'''Unsupported Feature for MiniOodle'''
		self.printFunc(self.outAStringType, node)
	
	def outAUdtType(self, node):
		'''Unsupported Feature for MiniOodle'''
		self.printFunc(self.outAUdtType, node)
	
	def outAArrayType(self, node):
		'''Unsupported Feature for MiniOodle'''
		self.printFunc(self.outAArrayType, node)

	###########################################################################
	## CLASS DECLARATION STUFF											   ##
	###########################################################################
	def outAKlass(self, node):
		''''''
		self.printFunc(self.outAKlass)
	
	def inAKlassHeader(self, node):
		''''''
		self.printFunc(self.inAKlassHeader, node)
	
	def inAKlassInherits(self, node):
		''''''
		self.printFunc(self.inAKlassInherits, node)

	def inAKlassBody(self, node):
		'''Manage class variables
		   Error Conditions:
		    * HACK MiniOodle: no class variable initialization'''
		self.printFunc(self.inAKlassBody)
		vars = node.getVars()

		#class variable init is unsupported in MiniOodle
		for v in vars:
			ln = v.getId().getLine() #line number
			src = v.toString().strip()
			nm = self.prefix() + v.getId().getText() #variable name
			self.writeAsmComment('#' + src, ln)
			self.writeAsm('\t.comm\t' + nm + ',4,4') #global class variable

	def inAKlassVar(self, node):
		'''Generate 'class variable' comments'''
		self.printFunc(self.inAKlassVar)
		ln = node.getVar().getId().getLine()
		src = node.toString().strip()
		self.writeAsmComment('#' + src, ln)

	def outAKlassVar(self, node):
		'''Generate 'class variable' code
		   Types
			* any type'''
		self.printFunc(self.outAKlassVar)
		nm = self.prefix() + node.getVar().getId().getText() #variable name
		self.writeAsm('\t.comm\t' + nm + ',4,4') #global class variable

	###########################################################################
	## STATEMENT STUFF													   ##
	###########################################################################
	def inAAssignStmt(self, node):
		'''Generate 'assignment statement' comments'''
		self.printFunc(self.inAAssignStmt, node)
		ln = node.getId().getLine()   #line number
		src = node.toString().strip() #assignment stmt source code
		self.writeAsmTextComment(src, ln)

	def outAAssignStmt(self, node):
		'''Generate 'assignment' statement code
		   Error Conditions:
			* NONE'''
		self.printFunc(self.outAAssignStmt, node)
		nm = '_' + node.getId().getText()
		
		#get Declaration if it is in the SymbolTable
		decl = None
		if node in G.symMap():
			decl = G.symMap()[node].decl()

		#local variable
		if isinstance(decl, LocalVarDecl):
			self.writeAsmText('popl ' + str(decl.offset()) + '(%ebp)')
		#variable
		else:
			self.writeAsmText('popl ' + nm)

	def caseAIfStmt(self, node):
		'''Generate 'if-else' code'''
		self.printFunc(self.caseAIfStmt, node)
		
		ln = node.getThen().getLine() #if-else line number
		src_expr = node.getExpr().toString().strip() #if-else source code
		else_lbl = self.nextLabel() #unique label for else start
		end_lbl = self.nextLabel()  #unique label for end of if-else
		
		self.inAIfStmt(node)
		if node.getExpr() != None:
			node.getExpr().apply(self)
			self.writeAsmTextComment('if ' + src_expr, ln)
			#check for boolean value in expression
			self.writeAsmText('popl %eax\n'
						      'cmpl $0, %eax\n'
						      'jz ' + else_lbl
						      )
		if node.getThen() != None:
			node.getThen().apply(self)
		if True: #scope block
			copy = node.getIfStmts()[:]
			for e in copy:
				e.apply(self)
			self.writeAsmText('jmp ' + end_lbl) #jump to end of if-else
			self.writeAsmTextLabel(else_lbl)    #else label
		if True: #scope block
			copy = node.getElseStmts()[:]
			for e in copy:
				e.apply(self)
		self.writeAsmTextLabel(end_lbl) #end label
		self.outAIfStmt(node)

	def caseALoopStmt(self, node):
		'''Generate 'loop while' code'''
		self.printFunc(self.caseALoopStmt, node)

		ln = node.getWhile().getLine() #loop line number
		src_expr = node.getExpr().toString().strip() #loop source code
		start_lbl = self.nextLabel() #unique label for loop start
		end_lbl = self.nextLabel()   #unique label for loop end

		self.inALoopStmt(node);
		if node.getWhile() != None:
			node.getWhile().apply(self)
			self.writeAsmTextComment('loop while ' + src_expr, ln)
			self.writeAsmTextLabel(start_lbl) #start loop label
		if node.getExpr() != None:
			node.getExpr().apply(self)
			#check boolean value of expression
			self.writeAsmText('popl %eax\n'
						      'cmpl $0, %eax\n'
						      'jz ' + end_lbl
						      )
		if True: #scope block
			copy = node.getLoopStmts()[:]
			for e in copy:
				e.apply(self)
		self.writeAsmText('jmp ' + start_lbl) #repeat loop jump
		self.writeAsmTextLabel(end_lbl)       #end loop label
		self.outALoopStmt(node)

	def outACallStmt(self, node):
		'''Generate 'call stmt' code
		   This node is always used for calls that do not have return values'''
		self.printFunc(self.outACallStmt, node)

	###########################################################################
	## EXPRESSION STUFF													  ##
	###########################################################################
	
	def outAIdExpr(self, node):
		'''Generate 'id' code
		   Types
		    * a variable name'''
		self.printFunc(self.outAIdExpr, node)
		nm = self.prefix() + node.getId().getText()
		
		#get the Declaration if it is in the SymbolMap
		decl = None
		if node in G.symMap():
			decl = G.symMap()[node].decl()
		
		#local variable
		if isinstance(decl, LocalVarDecl):
			self.writeAsmText('pushl ' + str(decl.offset()) + '(%ebp)')
		#variable
		else:
			self.writeAsmText('pushl ' + nm)

	def outAStrExpr(self, node):
		''''''
		self.printFunc(self.outAStrExpr, node)

	def outAIntExpr(self, node):
		'''Generate 'int' code
		   Types
		    * Type.INT'''
		self.printFunc(self.outAIntExpr, node)
		imm = '$' + node.getValue().getText()
		self.writeAsmText('pushl ' + imm)

	def outATrueExpr(self, node):
		'''Generate 'true' code
		   Types
		    * Type.BOOLEAN'''
		self.printFunc(self.outATrueExpr, node)
		self.writeAsmText('pushl $1')

	def outAFalseExpr(self, node):
		'''Generate 'false' code
		   Types
		    * Type.BOOLEAN'''
		self.printFunc(self.outAFalseExpr, node)
		self.writeAsmText('pushl $0')

	def outANullExpr(self, node):
		''''''
		self.printFunc(self.outANullExpr, node)

	def outAParExpr(self, node):
		''''''
		self.printFunc(self.outAParExpr, node)

	def outACallExpr(self, node):
		'''Generate 'call expr9' code
		   This node is always used for calls that return a value'''
		self.printFunc(self.outACallExpr, node)
		self.writeAsmText('pushl %eax')

	def outAPosExpr(self, node):
		'''Generate 'positive' code
		   Types
		    * operand == Type.INT
		   Special Cases
		    * this operation does absolutely nothing'''
		self.printFunc(self.outAPosExpr, node)

	def outANegExpr(self, node):
		'''Generate 'negation' code
		   Types
		    * operand == Type.INT'''
		self.printFunc(self.outANegExpr, node)
		self.writeAsmText('popl %eax\n'
					      'neg %eax\n'
					      'pushl %eax'
					      )

	def outANotExpr(self, node):
		'''Generate 'not' code
		   Types
		    * operand == Type.BOOLEAN'''
		self.printFunc(self.outANotExpr, node)
		self.writeAsmText('popl %eax\n'
					      'testl %eax, %eax\n'
					      'sete %al\n'
					      'movzxb %al, %eax\n'
					      'pushl %eax'
					      )

	def outAMultExpr(self, node):
		'''Generate 'multiplication' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outAMultExpr, node)
		self.writeAsmText('popl %ebx\n'
					      'popl %eax\n'
					      'imul %ebx, %eax\n'
					      'pushl %eax')

	def outADivExpr(self, node):
		'''Generate 'division' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outADivExpr, node)
		self.writeAsmText('popl %ecx\n'
					  'popl %eax\n'
					  'cdq\n'
					  'idiv %ecx\n'
					  'pushl %eax')

	def outAAddExpr(self, node):
		'''Generate 'addition' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outAAddExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'addl %ebx, %eax\n'
					  'pushl %eax')
	
	def outASubExpr(self, node):
		'''Generate 'subtraction' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outASubExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'subl %ebx, %eax\n'
					  'pushl %eax')

	def outAConcatExpr(self, node):
		''''''
		self.printFunc(self.outAConcatExpr, node)

	def outALteExpr(self, node):
		'''Generate 'less than or equal' code
		   Types
			* lhs && rhs == Type.INT
			* FIXME - lhs && rhs == Type.String'''
		self.printFunc(self.outALteExpr)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setleb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAGteExpr(self, node):
		'''Generate 'greater than or equal' code
		   Types
			* lhs && rhs == Type.INT
			* FIXME - lhs && rhs == Type.String'''
		self.printFunc(self.outAGteExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setgeb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outALtExpr(self, node):
		'''Generate 'less than' code
		   Types
			* lhs && rhs == Type.INT
			* FIXME - lhs && rhs == Type.STRING'''
		self.printFunc(self.outALtExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setlb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAGtExpr(self, node):
		'''Generate 'greater than' code
		   Types
			* lhs && rhs == Type.INT
			* FIXME - lhs && rhs == Type.STRING'''
		self.printFunc(self.outAGtExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setgb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAEqExpr(self, node):
		'''Generate 'less than' code
		   Types
			* lhs && rhs == Type.INT
			* FIXME - lhs && rhs == Type.STRING
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAEqExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'seteb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )
	
	def outAAndExpr(self, node):
		'''Generate 'and' code
		   Types
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAAndExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'and %ebx, %eax\n'
					  'pushl %eax')
	
	def outAOrExpr(self, node):
		'''Generate 'or' code
		   Types
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAOrExpr, node)
		self.writeAsmText('popl %ebx\n'
					  'popl %eax\n'
					  'or %ebx, %eax\n'
					  'pushl %eax')

	##########################################################################
	# MISCELLANEOUS STUFF												   ##
	##########################################################################
	def caseACall(self, node):
		'''FIXME - huge hack for MiniOodle readint/writeint'''
		self.inACall(node)
		#FIXME - huge hack for MiniOodle readint/writeint
		#if node.getExpr() != None:
		#	node.getExpr().apply(self)
		if node.getId() != None:
			node.getId().apply(self)
		copy = node.getArgs()[::-1]
		for e in copy:
			e.apply(self)
		self.outACall(node)

	def outACall(self, node):
		'''Generate method 'call' code
		   Error Conditions
			* NONE'''
		self.printFunc(self.outACall, node)
		src = node.toString().strip()
		ln = node.getId().getLine()
		nm = node.getId().getText()
		sym = G.symTab().lookup(nm)
		decl = sym.decl()
		self.writeAsmTextComment(src, ln)
		self.writeAsmText('call ' + nm)
		
		#FIXME - HACK FOR REMOVING/NOT REMOVING PARAMETERS
		if len(decl.argTypes()) == 1 and decl.argTypes()[0] == Type.VOID:
			pass 
		else: 
			self.writeAsmText('addl $' + str(len(decl.argTypes()) * 4 ) + ', %esp')

	def inStart(self, node):
		''''''
		self.printFunc(self.inStart)
		self.writeAsmTextFunc('main')
		self.writeAsmText('call start\n'
						  'ret'
						  )
