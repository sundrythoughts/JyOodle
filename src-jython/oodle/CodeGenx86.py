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

class CodeGenx86(DepthFirstAdapter):
	''''''
	def __init__(self):
		DepthFirstAdapter.__init__(self)
		self.typeMap = dict()       #dict<Node,Type>
		
		self.hack_has_class = False #HACK for MiniOodle
		self.valid_scope = False
		self.asm_list = []          #list of asm instructions
		self.label_counter = 0      #unique counter for label generation

	def prefix(self):
		'''Get the proper prefix for asm variables'''
		return '_'

	def writeAsm(self, asm_str):
		'''add asm to list
		   also add tabs to output for prettier printing'''
		self.asm_list.append('\t' + asm_str.replace('\n', '\n\t'))

	def writeAsmLabel(self, lbl_str):
		'''add asm labels to list'''
		self.asm_list.append(lbl_str + ':')

	def writeAsmComment(self, com_str, ln=None):
		'''add asm comments and line number to list'''
		com_str = com_str.strip().replace('\n', '\n#')
		if ln:
			self.asm_list.append('#Line ' + str(ln) + ': ' + com_str)
		else:
			self.asm_list.append('# ' + com_str)
	
	def printAsm(self):
		for l in self.asm_list:
			print l

	def nextLabel(self):
		self.label_counter += 1
		return '.L' + str(self.label_counter)
	
	###########################################################################
	## Methods to help with debugging										 ##
	###########################################################################
	def printFunc(self, f, node=None):
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

	def printTypeMap(self):
		for k in self.typeMap:
			print k,':',self.typeMap[k]

	###########################################################################
	## METHOD DECLARATION STUFF											  ##
	###########################################################################
	def outAMethod(self, node):
		self.printFunc(self.outAMethod)

	def inAMethodSig(self, node):
		''''''
		self.printFunc(self.inAMethodSig, node)

	def outAMethodSig(self, node):
		self.printFunc(self.outAMethodSig, node)
	
	def outAArgList(self, node):
		self.printFunc(self.outAArgList, node)
	
	def outAArgListTail(self, node):
		self.printFunc(self.outAArgListTail, node)
	
	def outAArg(self, node):
		self.printFunc(self.outAArg, node)
	
	def outAMethodVar(self, node):
		''''''
		self.printFunc(self.outAMethodVar)
	
	
	###########################################################################
	## GENERIC VARIABLE DECLARATION STUFF (also includes method return type) ##
	###########################################################################	
	def outAVar(self, node):
		self.printFunc(self.outAVar, node)
	
	def outAVarAssign(self, node):
		''''''
		self.printFunc(self.outAVarAssign, node)

	def outAVarType(self, node):
		self.printFunc(self.outAVarType, node)

	def outABoolType(self, node):
		self.printFunc(self.outABoolType, node)
	
	def outAIntType(self, node):
		self.printFunc(self.outAIntType, node)
		
	def outAStringType(self, node):
		'''Unsupported Feature for MiniOodle'''
		self.printFunc(self.outAStringType, node)
	
	def outAUdtType(self, node):
		self.printFunc(self.outAUdtType, node)
	
	def outAArrayType(self, node):
		self.printFunc(self.outAArrayType, node)

	###########################################################################
	## CLASS DECLARATION STUFF											   ##
	###########################################################################
	def outAKlass(self, node):
		'''Manage class declaration
		   Error Conditions:
			* Mismatched class header and footer names'''
		self.printFunc(self.outAKlass)
	
	def inAKlassHeader(self, node):
		''''''
		self.printFunc(self.inAKlassHeader, node)
	
	def inAKlassInherits(self, node):
		''''''
		self.printFunc(self.inAKlassInherits, node)

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
		self.writeAsm('.comm\t' + nm + ',4,4') #global class variable

	###########################################################################
	## STATEMENT STUFF													   ##
	###########################################################################
	def inAAssignStmt(self, node):
		'''Generate 'assignment statement' comments'''
		self.printFunc(self.inAAssignStmt, node)
		ln = node.getId().getLine()   #line number
		src = node.toString().strip() #assignment stmt source code
		self.writeAsmComment(src, ln)

	def outAAssignStmt(self, node):
		'''Manage 'assignment' statement
		   Error Conditions:
			* rhs id must exist and be a VarDecl or (return type) MethodDecl
			* lhs and rhs must have equal types'''
		self.printFunc(self.outAAssignStmt, node)
		nm = '_' + node.getId().getText()
		self.writeAsm('popl ' + nm)

	def caseAIfStmt(self, node):
		'''Generate 'if-else' code'''
		self.printFunc(self.caseAIfStmt, node)
		
		ln = node.getIf1().getLine() #if-else line number
		src_expr = node.getExpr().toString().strip() #if-else source code
		else_lbl = self.nextLabel() #unique label for else start
		end_lbl = self.nextLabel()  #unique label for end of if-else

		self.inAIfStmt(node)
		if node.getIf1() != None:
			node.getIf1().apply(self)
		if node.getExpr() != None:
			node.getExpr().apply(self)
			self.writeAsmComment('if ' + src_expr, ln)
			#check for boolean value in expression
			self.writeAsm('popl %eax\n'
						  'cmpl $0, %eax\n'
						  'jz ' + else_lbl
						  )
		if node.getKwThen() != None:
			node.getKwThen().apply(self)
		if node.getCrPlus() != None:
			node.getCrPlus().apply(self)
		if node.getStmtList() != None:
			node.getStmtList().apply(self)
			self.writeAsm('jmp ' + end_lbl) #jump to end of if-else
			self.writeAsmLabel(else_lbl)    #else label
		if node.getStmtElse() != None:
			node.getStmtElse().apply(self)
		if node.getKwEnd() != None:
			node.getKwEnd().apply(self)
			self.writeAsmLabel(end_lbl) #end label
		if node.getIf2() != None:
			node.getIf2().apply(self)
		self.outAIfStmt(node)

	def caseALoopStmt(self, node):
		'''Generate 'loop while' code'''
		self.printFunc(self.caseALoopStmt, node)

		ln = node.getLp1().getLine() #loop line number
		src_expr = node.getExpr().toString().strip() #loop source code
		start_lbl = self.nextLabel() #unique label for loop start
		end_lbl = self.nextLabel()   #unique label for loop end

		self.inALoopStmt(node)
		if node.getLp1() != None:
			node.getLp1().apply(self)
			self.writeAsmComment('loop while ' + src_expr, ln)
			self.writeAsmLabel(start_lbl) #start loop label
		if node.getKwWhile() != None:
			node.getKwWhile().apply(self)
		if node.getExpr() != None:
			node.getExpr().apply(self)
			#check boolean value of expression
			self.writeAsm('popl %eax\n'
						  'cmpl $0, %eax\n'
						  'jz ' + end_lbl
						  )
		if node.getCrPlus() != None:
			node.getCrPlus().apply(self)
		if node.getStmtList() != None:
			node.getStmtList().apply(self)
		if node.getKwEnd() != None:
			node.getKwEnd().apply(self)
			self.writeAsm('jmp ' + start_lbl) #repeat loop jump
			self.writeAsmLabel(end_lbl)       #end loop label
		if node.getLp2() != None:
			node.getLp2().apply(self)
		self.outALoopStmt(node)

	def outACallStmt(self, node):
		''''''
		self.printFunc(self.outACallStmt, node)

	###########################################################################
	## EXPRESSION STUFF													  ##
	###########################################################################
	def readBinExpr(self, node):
		''''''
		lhs = node.getE1()
		rhs = node.getE2()
		tp_lhs = self.typeMap[lhs]
		tp_rhs = self.typeMap[rhs]
		return (lhs, rhs, tp_lhs, tp_rhs)
	
	def checkBinExprTypes(self, node, tp_ls):
		''''''
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		for t in tp_ls:
			if tp_lhs == t and tp_rhs == t:
				return tp_lhs
		return Type.NONE
	
	def outAIdExpr9(self, node):
		'''Generate 'id' code
		   Types
		    * a variable name'''
		self.printFunc(self.outAIdExpr9, node)
		nm = self.prefix() + node.getId().getText()
		self.writeAsm('pushl ' + nm)

	def outAStrExpr9(self, node):
		''''''
		self.printFunc(self.outAStrExpr9, node)

	def outAIntExpr9(self, node):
		'''Generate 'int' code
		   Types
		    * Type.INT'''
		self.printFunc(self.outAIntExpr9, node)
		imm = '$' + node.getIntLit().getText()
		self.writeAsm('pushl ' + imm)

	def outATrueExpr9(self, node):
		'''Generate 'true' code
		   Types
		    * Type.BOOLEAN'''
		self.printFunc(self.outATrueExpr9, node)
		self.writeAsm('pushl $1')

	def outAFalseExpr9(self, node):
		'''Generate 'false' code
		   Types
		    * Type.BOOLEAN'''
		self.printFunc(self.outAFalseExpr9, node)
		self.writeAsm('pushl $0')

	def outANullExpr9(self, node):
		''''''
		self.printFunc(self.outANullExpr9, node)

	def outAParExpr9(self, node):
		''''''
		self.printFunc(self.outAParExpr9, node)

	def outACallExpr9(self, node):
		''''''
		self.printFunc(self.outACallExpr9, node)

	def outAPosExpr8(self, node):
		'''Generate 'positive' code
		   Types
		    * operand == Type.INT
		   Special Cases
		    * this operation does absolutely nothing'''
		self.printFunc(self.outAPosExpr8, node)

	def outANegExpr8(self, node):
		'''Generate 'negation' code
		   Types
		    * operand == Type.INT'''
		self.printFunc(self.outANegExpr8, node)
		self.writeAsm('popl %eax\n'
					  'neg %eax\n'
					  'pushl %eax'
					  )

	def outANotExpr8(self, node):
		'''Generate 'not' code
		   Types
		    * operand == Type.BOOLEAN'''
		self.printFunc(self.outANotExpr8, node)
		self.writeAsm('popl %eax\n'
					  'testl %eax, %eax\n'
					  'sete %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAMultExpr5(self, node):
		'''Generate 'multiplication' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outAMultExpr5, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'imul %ebx, %eax\n'
					  'pushl %eax')

	def outADivExpr5(self, node):
		'''Generate 'division' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outAMultExpr5, node)
		self.writeAsm('popl %ecx\n'
					  'popl %eax\n'
					  'cdq\n'
					  'idiv %ecx\n'
					  'pushl %eax')

	def outAAddExpr4(self, node):
		'''Generate 'addition' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outAAddExpr4, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'addl %ebx, %eax\n'
					  'pushl %eax')
	
	def outASubExpr4(self, node):
		'''Generate 'subtraction' code
		   Types
		    * lhs && rhs == Type.INT'''
		self.printFunc(self.outASubExpr4, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'subl %ebx, %eax\n'
					  'pushl %eax')

	def outAConcatExpr3(self, node):
		''''''
		self.printFunc(self.outAConcatExpr3, node)

	def outALteExpr2(self, node):
		'''Generate 'less than or equal' code
		   Types
			* lhs && rhs == Type.INT
			* lhs && rhs == Type.String'''
		self.printFunc(self.outALteExpr2)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setbeb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAGteExpr2(self, node):
		'''Generate 'greater than or equal' code
		   Types
			* lhs && rhs == Type.INT
			* lhs && rhs == Type.String'''
		self.printFunc(self.outAGteExpr2, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setaeb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outALtExpr2(self, node):
		'''Generate 'less than' code
		   Types
			* lhs && rhs == Type.INT
			* lhs && rhs == Type.STRING'''
		self.printFunc(self.outALtExpr2, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setbb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAGtExpr2(self, node):
		'''Generate 'greater than' code
		   Types
			* lhs && rhs == Type.INT
			* lhs && rhs == Type.STRING'''
		self.printFunc(self.outAGtExpr2, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'setab %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )

	def outAEqExpr2(self, node):
		'''Generate 'less than' code
		   Types
			* lhs && rhs == Type.INT
			* lhs && rhs == Type.STRING
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAEqExpr2, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'cmpl %ebx, %eax\n'
					  'seteb %al\n'
					  'movzxb %al, %eax\n'
					  'pushl %eax'
					  )
	
	def outAAndExpr1(self, node):
		'''Generate 'and' code
		   Types
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAAndExpr1, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'and %ebx, %eax\n'
					  'pushl %eax')
	
	def outAOrExpr(self, node):
		'''Generate 'or' code
		   Types
			* lhs && rhs == Type.BOOLEAN'''
		self.printFunc(self.outAAndExpr1, node)
		self.writeAsm('popl %ebx\n'
					  'popl %eax\n'
					  'or %ebx, %eax\n'
					  'pushl %eax')

	def outAExprList(self, node):
		'''Manage 'expr_list'
		   Error Conditions
			* NONE
		   Special Features
			* puts the entire list into the typeMap'''
		self.printFunc(self.outAExprList, node)

	###########################################################################
	## MISCELLANEOUS STUFF												   ##
	###########################################################################
	def outACall(self, node):
		'''Manage a method 'call'
		   Error Conditions
			* object does not contain method id
			* method id does not exist in 'me'
			* wrong number of parameters
			* wrong parameter types'''
		self.printFunc(self.outACall, node)
	
	