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

class SemanticChecker(DepthFirstAdapter):
	'''Check the Oodle source code for correctness'''
	def __init__(self):
		DepthFirstAdapter.__init__(self)
		self.typeMap = dict() #stores the Type of each node
		
		self.hack_has_class = False #HACK for MiniOodle
		self.valid_scope = False #help determine whether a scope is valid or not
	
	###########################################################################
	## Methods to help with debuggin                                         ##
	###########################################################################
	def printFunc(self, f, node=None):
		'''print the name of the node function and its node string
		   only works if 'printDebug()' is enabled'''
		n = (': ' + node.toString().strip()) if node else ''
		if G.options().printDebug():
			print 'SemanticChecker: ' + f.__name__ + n
	
	###########################################################################
	## Methods to help with querying/modifying the SymbolTable               ##
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
	
	def beginScope(self, b=True):
		'''shorten the call to add a new scope'''
		self.valid_scope = b
		G.symTab().beginScope()
	
	def endScope(self, b=True):
		'''shorten the call to end a new scope'''
		if self.valid_scope:
			G.symTab().endScope()
		self.valid_scope = b
	
	def printTypeMap(self):
		'''print every node in the map and its Type'''
		for k in self.typeMap:
			print k,':',self.typeMap[k]

	###########################################################################
	## METHOD DECLARATION STUFF                                              ##
	###########################################################################
	def outAMethod(self, node):
		'''Manage method leaving a method'''
		self.printFunc(self.outAMethod)
		self.endScope() #remove all local variables 
		
	def inAMethodSig(self, node):
		'''Check method signature
		   Error Conditions:
		    * Method already declared
		    * HACK MiniOodle: any method besides start()'''
		self.printFunc(self.inAMethodSig, node)
		nm = node.getId().getText() #get the method name
		ln = node.getId().getLine()
		sym = G.symTab().lookup(nm)
		if sym != None:
			G.errors().semantic().add("redeclared identifier '" + nm + "'", ln)
			self.beginScope(False)
		else:
			#HACK: if method is something other than start()
			if nm != 'start':
				G.errors().semantic().addUnsupportedFeature('method must be named start()', ln)
			G.symTab().push(nm, MethodDecl([], Type.VOID))   #add the (node id, type) to the SymbolTable
			self.beginScope() #make new scope for local variables

	def outAMethodSig(self, node):
		'''Add method signature to SymbolTable
		   Error Conditions:
		    * FIXME'''
		self.printFunc(self.outAMethodSig, node)
		nm = node.getId().getText() #get the method name
		decl = G.symTab().lookup(nm).decl() #get the MethodDecl

		#get argument list
		n_args = [] #initialize to void parameters
		tmp = node.getArgList()
		tmp = None if tmp == None else tmp.getArg()
		if tmp != None:
			n_args = [self.typeMap[tmp]] #get first argument
			for n in node.getArgList().getArgListTail(): #get remaining arguments
				n_args.append(self.typeMap[n])

		#get return type
		n_ret = Type.VOID #initialize to void return
		tmp = node.getVarType()
		if tmp != None:
			n_ret = self.typeMap[tmp]

		#set MethodDecl arg types and return type
		decl.setArgTypes(n_args)
		decl.setRetType(n_ret)
	
	def outAArgList(self, node):
		''''''
		self.printFunc(self.outAArgList, node)
		#self.typeMap[node] = self.typeMap[node.getArgListTail()]
	
	def outAArgListTail(self, node):
		''''''
		self.printFunc(self.outAArgListTail, node)
		self.typeMap[node] = self.typeMap[node.getArg()]
	
	def outAArg(self, node):
		'''Manage method 'arg'
		   Error Conditions:
		    * var id is alread used in this scope'''
		self.printFunc(self.outAArg, node)
		nm = node.getId().getText() #get the variable name
		if self.isVarNameUsed(nm):
			G.errors().semantic().add("variable '" + nm + "' already used", ln)

		tp = self.typeMap[node.getType()] #get the variable type from the child node
		self.typeMap[node] = tp              #store this nodes type
		G.symTab().push(nm, VarDecl(tp))   #add the (node id, type) to the SymbolTable
	
	def outAMethodVar(self, node):
		'''Manage local method variables
		   Error Conditions
		    * Any local variables declared'''
		self.printFunc(self.outAMethodVar)
		var_node = node.getVar()
		if var_node != None: #method variable init is unsupported in MiniOodle
			ln = node.getVar().getId().getLine()
			G.errors().semantic().addUnsupportedFeature('local method variables', ln)
		self.typeMap[node] = self.typeMap[node.getVar()]
	
	
	###########################################################################
	## GENERIC VARIABLE DECLARATION STUFF (also includes method return type) ##
	###########################################################################	
	def outAVar(self, node):
		'''Manage 'var' declarations
		   Error Conditions:
		    * var id already used in this scope
		    * var type is not declared
		    * var type is mismatched'''
		self.printFunc(self.outAVar, node)
		err = False #set if error is detected
		id = node.getId() #TId node
		nm = id.getText() #variable name
		ln = id.getLine() #line number
		
		#variable name already used
		if self.isVarNameUsed(nm):
			err = True
			G.errors().semantic().add("variable '" + nm + "' already used", ln)
		
		#check assignment type
		tp_assign = Type.NONE
		if node.getVarAssign() != None:
			tp_assign = self.typeMap[node.getVarAssign()]
			
		
		#check declared type
		tp_decl = Type.NONE
		if node.getVarType() == None:
			G.errors().semantic().add("variable '" + nm + "' must have a type", ln)
		else:
			tp_decl = self.typeMap[node.getVarType()] #get the variable type from the child node
		
		#compare declared and assigned types
		if tp_assign != Type.NONE and tp_decl != Type.NONE and tp_assign != tp_decl:
			G.errors().semantic().add("type mismatch '" + tp_decl.name() +
									  "' := '" + tp_assign.name(), ln)

		#add name to SymbolTable (even if an error occurred)
		self.typeMap[node] = tp_decl              #store this nodes type
		G.symTab().push(nm, VarDecl(tp_decl))   #add the (node id, type) to the SymbolTable
	
	def outAVarAssign(self, node):
		'''Manage assignment during variable declaration
		   Error Conditions:
		    * HACK MiniOodle: any assigment during declaration is unsupported'''
		self.printFunc(self.outAVarAssign, node)
		#HACK MiniOodle: assignment not supported
		ln = node.getOpAssign().getLine()
		G.errors().semantic().addUnsupportedFeature('variable initialization', ln)

		self.typeMap[node] = self.typeMap[node.getExpr()]

	def outAVarType(self, node):
		'''Manage 'var' type'''
		self.printFunc(self.outAVarType, node)
		self.typeMap[node] = self.typeMap[node.getType()] #store this nodes type

	def outABoolType(self, node):
		'''Manage 'boolean' type'''
		self.printFunc(self.outABoolType, node)
		self.typeMap[node] = Type.BOOLEAN #store this nodes type
	
	def outAIntType(self, node):
		'''Manage 'int' type'''
		self.printFunc(self.outAIntType, node)
		self.typeMap[node] = Type.INT #store this nodes type
		
	def outAStringType(self, node):
		'''Unsupported Feature for MiniOodle'''
		self.printFunc(self.outAStringType, node)
		self.typeMap[node] = Type.STRING      #store this nodes type
		ln = node.getKwString().getLine() #get the line number
		G.errors().semantic().addUnsupportedFeature('string', ln)
	
	def outAUdtType(self, node):
		'''Manage 'array' type
		   Error Conditions:
		    * Unsupported Feature'''
		self.printFunc(self.outAUdtType, node)
		err = False
		nm = node.getId().getText()
		ln = node.getId().getLine()

		G.errors().semantic().addUnsupportedFeature('user-defined type', ln)
		
		#invalid/undeclared type name
		if G.symTab().lookup(nm) == None:
			err = True
			G.errors().semantic().add("invalid/undeclared type name", ln)
		
		#add name to SymbolTable (even if and error occurred)
		self.typeMap[node] = Type.Type(nm)
	
	def outAArrayType(self, node):
		'''Manage 'array' type
		   Error Conditions:
		    * Unsupported Feature'''
		self.printFunc(self.outAArrayType, node)
		ln = node.getMiscLBrack().getLine()
		G.errors().semantic().addUnsupportedFeature('array', ln)
		self.typeMap[node] = Type.NONE

	###########################################################################
	## CLASS DECLARATION STUFF                                               ##
	###########################################################################
	def outAKlass(self, node):
		'''Manage class declaration
		   Error Conditions:
		    * Mismatched class header and footer names'''
		self.printFunc(self.outAKlass)
		err = False
		nm_hd = node.getKlassHeader().getId().getText() #class header name
		nm_ft = node.getKlassFooter().getId().getText() #class footer name
		ln_ft = node.getKlassFooter().getId().getLine() #class footer line number
		
		#class names are mismatched
		if nm_hd != nm_ft:
			err = True
			G.errors().semantic().add("mismatched class names 'class " + nm_hd +
									  " is ... end " + nm_ft + "'", ln_ft)
	
	def inAKlassHeader(self, node):
		'''Push class name into SymbolTable
		   Error Conditions:
		    * HACK MiniOodle: only one class can be declared 
		    * Class name already used'''
		self.printFunc(self.inAKlassHeader, node)
		err = False       #set if an error is detected
		id = node.getId() #TId node
		nm = id.getText() #class name
		ln = id.getLine() #line number
		
		#HACK for MiniOodle: no class declared yet
		if self.hack_has_class:
			err = True
			G.errors().semantic().addUnsupportedFeature("multiple classes", ln)

		#class name has already been used
		if self.isClassNameUsed(nm):
			err = True
			G.errors().semantic().add("class '" + nm + "' already used", ln)

		#add name to SymbolTable (even if and error occurred)
		G.symTab().push(node.getId().getText(), ClassDecl())
		self.beginScope()
		self.hack_has_class = True #HACK for MiniOodle: no class declared yet
			
	
	def inAKlassInherits(self, node):
		'''Manage inheritance
		   Error Conditions:
		    * HACK MiniOodle: inheritance is an unsupported feature'''
		self.printFunc(self.inAKlassInherits, node)
		ln = node.getKwFrom().getLine() #get the line number
		G.errors().semantic().addUnsupportedFeature("'inherits from'", ln)
		
	def outAKlassVar(self, node):
		'''Manage class variables
		   Error Conditions:
		    * HACK MiniOodle: no class variable initialization'''
		self.printFunc(self.outAKlassVar)
		var_node = node.getVar().getVarAssign()
		
		#class variable init is unsupported in MiniOodle
		if var_node != None:
			ln = node.getVar().getVarAssign().getOpAssign().getLine() #line number
			G.errors().semantic().addUnsupportedFeature("class variable initialization", ln)

	###########################################################################
	## STATEMENT STUFF                                                       ##
	###########################################################################
	def outAAssignStmt(self, node):
		'''Manage 'assignment' statement
		   Error Conditions:
		    * rhs id must exist and be a VarDecl or (return type) MethodDecl
		    * lhs and rhs must have equal types'''
		self.printFunc(self.outAAssignStmt, node)
		ln = node.getOpAssign().getLine()
		nm = node.getId().getText()
		sym = G.symTab().lookup(nm)
		tp_lhs = Type.NONE
		tp_rhs = self.typeMap[node.getExpr()]
		
		#id does not exist or is not a variable or method
		if sym == None or not isinstance(sym.decl(), (VarDecl, MethodDecl)):
			G.errors().semantic().add("'" + nm + "' does not exist", ln)
		#id exists and is a variable
		elif isinstance(sym.decl(), VarDecl):
			tp_lhs = sym.decl().varType()
		#id exists and is a method
		elif isinstance(sym.decl(), MethodDecl):
			G.errors().semantic().addUnsupportedFeature("method return", ln)
			tp_lhs = sym.decl().retType()
		
		#check for equivalent types
		if sym != None and tp_lhs != tp_rhs:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' assignment requires 2 operands of the same type", ln)
	
	def outAIfStmt(self, node):
		'''Manage 'if' statement
		   Error Conditions:
		    * expr type != Type.BOOLEAN'''
		self.printFunc(self.outAIfStmt)
		ln = node.getKwThen().getLine()
		tp = self.typeMap[node.getExpr()]
		if tp != Type.BOOLEAN:
			G.errors().semantic().add("if statement must evaluate on type " +
									  Type.BOOLEAN.name(), ln)

	def outAStmtElse(self, node):
		'''Manage 'else' statement
		   Error Conditions:
		    * '''
		self.printFunc(self.outAStmtElse, node)
		

	def outALoopStmt(self, node):
		'''Manage 'loop while' statement
		   Error Conditions:
		    * expr type != Type.BOOLEAN'''
		self.printFunc(self.outALoopStmt)
		ln = node.getKwWhile().getLine()
		tp = self.typeMap[node.getExpr()]
		if tp != Type.BOOLEAN:
			G.errors().semantic().add("loops must evaluate on type " +
									  Type.BOOLEAN.name(), ln)
	
	def outACallStmt(self, node):
		'''Manage 'call' statement
		   Error Conditions:
		    * NONE'''
		self.printFunc(self.outACallStmt, node)
		self.typeMap[node] = self.typeMap[node.getCall()]

	
	###########################################################################
	## EXPRESSION STUFF                                                      ##
	###########################################################################
	def readBinExpr(self, node):
		'''Takes any binary expression and returns a tuple of...
		   (lhs node, rhs node, lhs type, rhs type)
		   It assumes that the lhs == node.getE1() and rhs == node.getE2()'''
		lhs = node.getE1()
		rhs = node.getE2()
		tp_lhs = self.typeMap[lhs]
		tp_rhs = self.typeMap[rhs]
		return (lhs, rhs, tp_lhs, tp_rhs)
	
	def checkBinExprTypes(self, node, tp_ls):
		'''Check the binary expression node's lhs and rhs types.
		   Takes a list of types used to check.
		   Assumes that both sides are required to be the same type.
		   Return Type.* on match or Type.NONE if no matches.'''
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		for t in tp_ls:
			if tp_lhs == t and tp_rhs == t:
				return tp_lhs
		return Type.NONE
	
	def outAIdExpr9(self, node):
		'''Manage 'id' expr9 expression
		   Error Conditions
		    * Undefined id
		    * HACK MiniOodle 'out' and 'in' are allowed'''
		self.printFunc(self.outAIdExpr9, node)
		nm = node.getId().getText()
		sym = G.symTab().lookup(nm)
		ln = node.getId().getLine()
		
		tp = Type.NONE
		if nm == 'out':
			pass
		elif nm == 'in':
			pass
		#id is undefined
		elif sym == None:
			G.errors().semantic().add("undefined variable '" + nm + "'", ln)
		else:
			tp = sym.decl().varType()
		
		self.typeMap[node] = tp

	def outAStrExpr9(self, node):
		'''Manage 'string' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: string is unsupported'''
		self.printFunc(self.outAStrExpr9, node)
		ln = node.getStrLit().getLine()
		G.errors().semantic().addUnsupportedFeature("string", ln)
		self.typeMap[node] = Type.STRING

	def outAIntExpr9(self, node):
		'''Manage 'integer' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAIntExpr9, node)
		self.typeMap[node] = Type.INT

	def outATrueExpr9(self, node):
		'''Manage 'true' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outATrueExpr9, node)
		self.typeMap[node] = Type.BOOLEAN

	def outAFalseExpr9(self, node):
		'''Manage 'false' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAFalseExpr9, node)
		self.typeMap[node] = Type.BOOLEAN

	def outANullExpr9(self, node):
		'''Manage 'null' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outANullExpr9, node)
		self.typeMap[node] = Type.NULL

	def outAMeExpr9(self, node):
		'''Manage 'me' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: me is unsupported'''
		self.printFunc(self.outAMeExpr9, node)
		ln = node.getKwMe().getLine()
		G.errors().semantic().addUnsupportedFeature('me', ln)
		self.typeMap[node] = Type.NONE

	def outANewExpr9(self, node):
		'''Manage 'new' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: new is unsupported'''
		self.printFunc(self.outANewExpr9, node)
		ln = node.getKwNew().getLine()
		G.errors().semantic().addUnsupportedFeature('new', ln)
		self.typeMap[node] = Type.NONE

	def outAParExpr9(self, node):
		'''Manage parentheses expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAParExpr9, node)
		self.typeMap[node] = self.typeMap[node.getExpr()]

	def outAArrayExpr9(self, node):
		'''Manage 'array' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: me is unsupported'''
		self.printFunc(self.outAMeExpr9, node)
		ln = node.getId().getLine()
		G.errors().semantic().addUnsupportedFeature('array', ln)
		self.typeMap[node] = Type.NONE

	def outACallExpr9(self, node):
		'''Manage 'call' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outACallExpr9, node)
		self.typeMap[node] = self.typeMap[node.getCall()]

	def outAPosExpr8(self, node):
		'''Manage 'pos' expr8 expression
		   Error Conditions
		    * expression type != Type.INT'''
		self.printFunc(self.outAPosExpr8, node)
		ln = node.getOpPlus().getLine()
		tp = self.typeMap[node.getExpr9()]
		tp_ret = Type.INT
		if tp != Type.INT:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outANegExpr8(self, node):
		'''Manage 'neg' expr8 expression
		   Error Conditions
		    * expression type != Type.INT'''
		self.printFunc(self.outANegExpr8, node)
		ln = node.getOpMinus().getLine()
		tp = self.typeMap[node.getExpr9()]
		tp_ret = Type.INT
		if tp != Type.INT:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outANotExpr8(self, node):
		'''Manage 'not' expr8 expression
		   Error Conditions
		    * expression type not boolean'''
		self.printFunc(self.outANotExpr8, node)
		ln = node.getKwNot().getLine()
		tp = self.typeMap[node.getExpr9()]
		tp_ret = Type.BOOLEAN
		if tp != Type.BOOLEAN:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret

	def outAOtherExpr8(self, node):
		'''Manage 'other' expr8 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr8, node)
		self.typeMap[node] = self.typeMap[node.getExpr9()]

	def outAMultExpr5(self, node):
		'''Manage 'mult' expr4 expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAMultExpr5, node)
		ln = node.getOpMult().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' multiplication requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outADivExpr5(self, node):
		'''Manage 'div' expr4 expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAMultExpr5, node)
		ln = node.getOpDiv().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' division requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outAOtherExpr5(self, node):
		'''Manage 'other' expr5 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr5, node)
		self.typeMap[node] = self.typeMap[node.getExpr8()]

	def outAAddExpr4(self, node):
		'''Manage 'add' expr4 expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAAddExpr4, node)
		ln = node.getOpPlus().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' addition requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret
	
	def outASubExpr4(self, node):
		'''Manage 'sub' expr4 expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outASubExpr4, node)
		ln = node.getOpMinus().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' subtraction requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret
		
	
	def outAOtherExpr4(self, node):
		'''Manage 'other' expr4 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr4, node)
		self.typeMap[node] = self.typeMap[node.getExpr5()]

	def outAConcatExpr3(self, node):
		'''Manage 'concat' expr3 expression
		   Error Conditions
		    * lhs type != Type.STRING and rhs type != Type.STRING'''
		self.printFunc(self.outAConcatExpr3, node)
		ln = node.getOpConcat().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' concatenation requires 2 operands of type " +
									  Type.STRING.name(), ln)
		self.typeMap[node] = tp_ret

	def outAOtherExpr3(self, node):
		'''Manage 'other' expr3 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr3, node)
		self.typeMap[node] = self.typeMap[node.getExpr4()]

	def outALteExpr2(self, node):
		'''Manage 'less than or equal' expr2 expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outALteExpr2)
		ln = node.getOpLtEq().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand types must be INT xor STRING
		tp_ret = self.checkBinExprTypes(node, [Type.INT, Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' comparison requires 2 operands of type " +
									  Type.INT.name() + " or " +
									  Type.STRING.name(), ln)
		else:
			tp_ret = Type.BOOLEAN
		self.typeMap[node] = tp_ret

	def outAGteExpr2(self, node):
		'''Manage 'greater than or equal' expr2 expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outAGteExpr2, node)
		ln = node.getOpGtEq().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand types must be INT xor STRING
		tp_ret = self.checkBinExprTypes(node, [Type.INT, Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' comparison requires 2 operands of type " +
									  Type.INT.name() + " or " +
									  Type.STRING.name(), ln)
		else:
			tp_ret = Type.BOOLEAN
		self.typeMap[node] = tp_ret

	def outALtExpr2(self, node):
		'''Manage 'Less than' expr2 expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outALtExpr2, node)
		ln = node.getOpLt().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand types must be INT xor STRING
		tp_ret = self.checkBinExprTypes(node, [Type.INT, Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' comparison requires 2 operands of type " +
									  Type.INT.name() + " or " +
									  Type.STRING.name(), ln)
		else:
			tp_ret = Type.BOOLEAN
		self.typeMap[node] = tp_ret

	def outAGtExpr2(self, node):
		'''Manage 'greater than' expr2 expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outAGtExpr2, node)
		ln = node.getOpGt().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand types must be INT xor STRING
		tp_ret = self.checkBinExprTypes(node, [Type.INT, Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' comparison requires 2 operands of type " +
									  Type.INT.name() + " or " +
									  Type.STRING.name(), ln)
		else:
			tp_ret = Type.BOOLEAN
		self.typeMap[node] = tp_ret

	def outAEqExpr2(self, node):
		'''Manage 'equal to' expr2 expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING | Type.BOOLEAN)
		    * rhs_type != (Type.INT | Type.STRING | Type.BOOLEAN)'''
		self.printFunc(self.outAEqExpr2, node)
		ln = node.getOpEq().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand types must be INT xor STRING
		tp_ret = self.checkBinExprTypes(node, [Type.INT, Type.STRING, Type.BOOLEAN])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' comparison requires 2 operands of type " +
									  Type.INT.name() + " or " +
									  Type.STRING.name() + ' or ' +
									  Type.BOOLEAN.name(), ln)
		else:
			tp_ret = Type.BOOLEAN
		self.typeMap[node] = tp_ret

	def outAOtherExpr2(self, node):
		'''Manage 'other' expr2 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr2, node)
		self.typeMap[node] = self.typeMap[node.getExpr3()]
	
	def outAAndExpr1(self, node):
		'''Manage 'and' expr1 expression
		   Error Conditions
		    * lhs type != Type.BOOLEAN and rhs type != Type.BOOLEAN'''
		self.printFunc(self.outAAndExpr1, node)
		ln = node.getKwAnd().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be BOOLEAN
		tp_ret = self.checkBinExprTypes(node, [Type.BOOLEAN])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' and-logic requires 2 operands of type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret


	def outAOtherExpr1(self, node):
		'''Manage 'other' expr1 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr1, node)
		self.typeMap[node] = self.typeMap[node.getExpr2()]
	
	def outAOrExpr(self, node):
		'''Manage 'or' expr expression
		   Error Conditions
		    * lhs type != Type.BOOLEAN and rhs type != Type.BOOLENA'''
		self.printFunc(self.outAAndExpr1, node)
		ln = node.getKwOr().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be BOOLEAN
		tp_ret = self.checkBinExprTypes(node, [Type.BOOLEAN])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' or-logic requires 2 operands of type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret

	def outAOtherExpr(self, node):
		'''Manage 'other' expr expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAOtherExpr, node)
		self.typeMap[node] = self.typeMap[node.getExpr1()]


	def outAExprList(self, node):
		'''Manage 'expr_list'
		   Error Conditions
		    * NONE
		   Special Features
		    * puts the entire list into the typeMap'''
		self.printFunc(self.outAExprList, node)
		ls = []
		expr = node.getExpr()
		expr_tail = node.getExprListTail()
		if expr != None:
			ls.append(self.typeMap[expr])
		if len(expr_tail) > 0:
			for i in expr_tail:
				ls.append(self.typeMap[i.getExpr()])
		self.typeMap[node] = ls

	###########################################################################
	## MISCELLANEOUS STUFF                                                   ##
	###########################################################################
	def outAObjExpr(self, node):
		''''''
		self.printFunc(self.outAObjExpr, node)
	
	def outACall(self, node):
		'''Manage a method 'call'
		   Error Conditions
		    * object does not contain method id
		    * method id does not exist in 'me'
		    * wrong number of parameters
		    * wrong parameter types'''
		self.printFunc(self.outACall, node)
		ln = node.getId().getLine()
		nm = node.getId().getText()
		sym = G.symTab().lookup(nm)
		ls_args = []
		if node.getExprList() != None:
			ls_args = self.typeMap[node.getExprList()]

		tp_ret = Type.NONE
		#id does not exist or is not a method id
		if sym == None or not isinstance(sym.decl(), MethodDecl):
			G.errors().semantic().add("method '" + nm + "' does not exist", ln)
		#check for correct number and type of parameters
		elif len(ls_args) > 0:
			call_args = ls_args
			meth_args = sym.decl().argTypes()
			if len(call_args) != len(meth_args):
				G.errors().semantic().add("method '" + nm + "' expects " +
										  str(len(meth_args)) +
										  " parameter(s) but was given " +
										  str(len(call_args)), ln)
			elif call_args != meth_args:
				G.errors().semantic().add("method '" + nm +
										  "' expects parameters " +
										  sym.decl().argStr() +
										  " but was given " +
										  MethodDecl(call_args, None).argStr(), ln)
		#get method return type
		if sym != None:
			tp_ret = sym.decl().retType()
		
		self.typeMap[node] = tp_ret
	
	