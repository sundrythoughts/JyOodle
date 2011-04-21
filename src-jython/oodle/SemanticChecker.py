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

import cps450
from cps450.oodle.analysis import DepthFirstAdapter
from oodle.G import G
from oodle.Declarations import *
from oodle.TypeMap import *

class SemanticChecker(DepthFirstAdapter):
	'''Check the Oodle source code for correctness'''
	def __init__(self):
		DepthFirstAdapter.__init__(self)
		self.typeMap = dict() #stores the Type of each node
		
		self.hack_has_class = False #HACK for MiniOodle
		self.valid_scope = False    #help determine whether a scope is valid or not
		self.m_cur_class = ""    #holds the name of the current class
		self.m_cur_method = ""   #holds the name of the current method
	
	###########################################################################
	## Methods to help with debugging                                        ##
	###########################################################################
	def printFunc(self, f, node=None):
		'''print the name of the node function and its node string
		   only works if 'printDebug()' is enabled'''
		n = (': ' + node.toString().strip()) if node else ''
		if G.options().printDebug():
			print 'SemanticChecker: ' + f.__name__ + n

	###########################################################################
	## Utility methods                                                       ##
	###########################################################################
	def curClass(self):
		''''''
		return self.m_cur_class;
	
	def setCurClass(self, nm):
		''''''
		self.m_cur_class = nm
		
	def curMethod(self):
		''''''
		return self.m_cur_method
	
	def setCurMethod(self, nm):
		''''''
		self.m_cur_method = nm

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
	
	def curClass(self):
		''''''
		return self.m_cur_class;
	
	def setCurClass(self, nm):
		''''''
		self.m_cur_class = nm
	
	def printTypeMap(self):
		'''print every node in the map and its Type'''
		for k in self.typeMap:
			print k,':',self.typeMap[k]

	###########################################################################
	## FUNCTION DECLARATION STUFF                                            ##
	###########################################################################
	def inAFuncSig(self, node):
		''''''
		self.printFunc(self.inAFuncSig, node)
		nm = node.getId().getText() #get the method name
		ln = node.getId().getLine()
		self.setCurMethod(nm)

	def outAFuncArg(self, node):
		'''Manage function 'arg'
		   Error Conditions:'''
		self.printFunc(self.outAFuncArg, node)
		nm = node.getId().getText() #get the variable name

		tp = self.typeMap[node.getTp()]   #get the variable type from the child node
		self.typeMap[node] = tp           #store this nodes type

	def outAFunc(self, node):
		''''''
		self.printFunc(self.outAFunc)
		vars = node.getVars()
		
		#HACK - local variable init is unsupported in MiniOodle
		sloc = -8
		for v in vars:
			ln = v.getId().getLine() #line number
			if v.getExpr() != None:
				G.errors().semantic().addUnsupportedFeature("local variable initialization", ln)
		self.setCurMethod("")

	###########################################################################
	## METHOD DECLARATION STUFF                                              ##
	###########################################################################
	def outAMethod(self, node):
		'''Manage method leaving a method'''
		self.printFunc(self.outAMethod)
		vars = node.getVars()
		

		#HACK - local variable init is unsupported in MiniOodle
		sloc = -8
		for v in vars:
			ln = v.getId().getLine() #line number
			if v.getExpr() != None:
				G.errors().semantic().addUnsupportedFeature("local variable initialization", ln)
		self.setCurMethod("")

	def inAMethodSig(self, node):
		'''Check method signature
		   Error Conditions:'''
		self.printFunc(self.inAMethodSig, node)
		nm = node.getId().getText() #get the method name
		ln = node.getId().getLine()
		self.setCurMethod(nm)

	def outAMethodSig(self, node):
		'''Add method signature to SymbolTable
		   Error Conditions:
		    * FIXME'''
		self.printFunc(self.outAMethodSig, node)
		nm = node.getId().getText() #get the method name

	def outAArg(self, node):
		'''Manage method 'arg'
		   Error Conditions:
		    * var id is alread used in this scope'''
		self.printFunc(self.outAArg, node)
		nm = node.getId().getText() #get the variable name

		tp = self.typeMap[node.getTp()]   #get the variable type from the child node
		self.typeMap[node] = tp           #store this nodes type

	###########################################################################
	## GENERIC VARIABLE DECLARATION STUFF (also includes method return type) ##
	###########################################################################	
	def outAVar(self, node):
		'''Manage 'var' declarations
		   Error Conditions:
		    * var type is not declared
		    * var type is mismatched'''
		self.printFunc(self.outAVar, node)
		err = False #set if error is detected
		id = node.getId() #TId node
		nm = id.getText() #variable name
		ln = id.getLine() #line number
		
		#check assignment type
		tp_assign = Type.NONE
		if node.getExpr() != None:
			tp_assign = self.typeMap[node.getExpr()]
			
		
		#check declared type
		tp_decl = Type.NONE
		if node.getTp() == None:
			G.errors().semantic().add("variable '" + nm + "' must have a type", ln)
		else:
			tp_decl = self.typeMap[node.getTp()] #get the variable type from the child node
		
		#compare declared and assigned types
		if tp_assign != Type.NONE and tp_decl != Type.NONE and tp_assign != tp_decl:
			G.errors().semantic().add("type mismatch '" + tp_decl.name() +
									  "' := '" + tp_assign.name(), ln)
		#store this nodes type
		self.typeMap[node] = tp_decl


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
		ln = node.getTp().getLine() #get the line number
		G.errors().semantic().addUnsupportedFeature('string', ln)
	
	def outAUdtType(self, node):
		'''Manage 'user defined types' (classes types) type
		   Error Conditions:'''
		self.printFunc(self.outAUdtType, node)
		err = False
		nm = node.getTp().getText()
		ln = node.getTp().getLine()

		tp = Type.NONE
		#invalid/undeclared type name
		if not G.typeMap().klassExists(nm):
			G.errors().semantic().add("invalid/undeclared type name", ln)
		else:
			tp = G.typeMap().klass(nm)
		self.typeMap[node] = tp
	
	def outAArrayType(self, node):
		'''Manage 'array' type
		   Error Conditions:
		    * Unsupported Feature'''
		self.printFunc(self.outAArrayType, node)
		ln = node.getLBrack().getLine()
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
		''''''
		self.printFunc(self.inAKlassHeader, node)
		id = node.getId() #TId node
		nm = id.getText() #class name
		ln = id.getLine() #line number
		self.setCurClass(nm)

	def outAKlass(self, node):
		''''''
		self.printFunc(self.outAKlass, node)
		self.setCurClass("")

	def inAKlassInherits(self, node):
		'''Manage inheritance
		   Error Conditions:
		    * HACK MiniOodle: inheritance is an unsupported feature'''
		self.printFunc(self.inAKlassInherits, node)
		ln = node.getKwFrom().getLine() #get the line number
		G.errors().semantic().addUnsupportedFeature("'inherits from'", ln)

	def inAKlassBody(self, node):
		'''Manage class variables
		   Error Conditions:
		    * HACK MiniOodle: no class variable initialization'''
		self.printFunc(self.inAKlassBody)
		vars = node.getVars()

		#class variable init is unsupported in MiniOodle
		for v in vars:
			if v.getExpr() != None:
				ln = v.getId().getLine() #line number
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
		ln = node.getId().getLine()
		nm = node.getId().getText()
		decl = G.typeMap().var(self.curClass(), self.curMethod(), nm)
		tp_lhs = Type.NONE
		tp_rhs = self.typeMap[node.getExpr()]
		
		#id does not exist or is not a variable or method
		if decl == None or not isinstance(decl, (VarDecl, MethodDecl, FuncDecl)):
			G.errors().semantic().add("'" + nm + "' does not exist", ln)
		#id exists and is a variable or method
		elif isinstance(decl, (VarDecl, MethodDecl, FuncDecl)):
			tp_lhs = G.typeMap().klass(decl.typeName())
		
		#check for equivalent types
		if decl != None and tp_lhs != tp_rhs:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' assignment requires 2 operands of the same type", ln)
	
	def outAIfStmt(self, node):
		'''Manage 'if' statement
		   Error Conditions:
		    * expr type != Type.BOOLEAN'''
		self.printFunc(self.outAIfStmt)
		ln = node.getThen().getLine()
		tp = self.typeMap[node.getExpr()]
		if tp != Type.BOOLEAN:
			G.errors().semantic().add("if statement must evaluate on type " +
									  Type.BOOLEAN.name(), ln)

	def outALoopStmt(self, node):
		'''Manage 'loop while' statement
		   Error Conditions:
		    * expr type != Type.BOOLEAN'''
		self.printFunc(self.outALoopStmt)
		ln = node.getWhile().getLine()
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
		lhs = node.getLeft()
		rhs = node.getRight()
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
	
	def outAIdExpr(self, node):
		'''Manage 'id' expression
		   Error Conditions
		    * Undefined id
		    * HACK MiniOodle 'out' and 'in' are allowed'''
		self.printFunc(self.outAIdExpr, node)
		nm = node.getId().getText()
		decl = G.typeMap().var(self.curClass(), self.curMethod(), nm)
		ln = node.getId().getLine()
		
		tp = Type.NONE
		#HACK - MiniOodle classes of 'in' and 'out'
		#if nm == 'out':
		#	pass
		#elif nm == 'in':
		#	pass
		#id is undefined
		if decl == None:
			G.errors().semantic().add("undefined variable '" + nm + "'", ln)
		else:
			tp = G.typeMap().klass(decl.typeName())
		self.typeMap[node] = tp #assign this nodes type

	def outAStrExpr(self, node):
		'''Manage 'string' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: string is unsupported'''
		self.printFunc(self.outAStrExpr, node)
		ln = node.getValue().getLine()
		G.errors().semantic().addUnsupportedFeature("string", ln)
		self.typeMap[node] = Type.STRING

	def outAIntExpr(self, node):
		'''Manage 'integer' expr9 expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAIntExpr, node)
		self.typeMap[node] = Type.INT

	def outATrueExpr(self, node):
		'''Manage 'true' expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outATrueExpr, node)
		self.typeMap[node] = Type.BOOLEAN

	def outAFalseExpr(self, node):
		'''Manage 'false' expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outAFalseExpr, node)
		self.typeMap[node] = Type.BOOLEAN

	def outANullExpr(self, node):
		'''Manage 'null' expr expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outANullExpr, node)
		self.typeMap[node] = Type.NULL

	def outAMeExpr(self, node):
		'''Manage 'me' expr9 expression
		   Error Conditions
		    * HACK MiniOodle: me is unsupported'''
		self.printFunc(self.outAMeExpr, node)
		ln = node.getKwMe().getLine()
		G.errors().semantic().addUnsupportedFeature('me', ln)
		self.typeMap[node] = Type.NONE

	def outANewExpr(self, node):
		'''Manage 'new' expression
		   Error Conditions
		    * HACK MiniOodle: new is unsupported'''
		self.printFunc(self.outANewExpr, node)
		ln = node.getValue().getLine()
		nm = node.getTp().getTp().getText()
		tp = G.typeMap().klass(nm)
		if not tp:
			tp = Type.NONE
		self.typeMap[node] = tp

	def outAArrayExpr(self, node):
		'''Manage 'array' expression
		   Error Conditions
		    * HACK MiniOodle: me is unsupported'''
		self.printFunc(self.outAArrayExpr, node)
		ln = node.getId().getLine()
		G.errors().semantic().addUnsupportedFeature('array', ln)
		self.typeMap[node] = Type.NONE

	def outACallExpr(self, node):
		'''Manage 'call' expression
		   Error Conditions
		    * NONE'''
		self.printFunc(self.outACallExpr, node)
		self.typeMap[node] = self.typeMap[node.getCall()]

	def outAPosExpr(self, node):
		'''Manage 'pos' expression
		   Error Conditions
		    * expression type != Type.INT'''
		self.printFunc(self.outAPosExpr, node)
		ln = node.getOp().getLine()
		tp = self.typeMap[node.getExpr()]
		tp_ret = Type.INT
		if tp != Type.INT:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outANegExpr(self, node):
		'''Manage 'neg' expression
		   Error Conditions
		    * expression type != Type.INT'''
		self.printFunc(self.outANegExpr, node)
		ln = node.getOp().getLine()
		tp = self.typeMap[node.getExpr()]
		tp_ret = Type.INT
		if tp != Type.INT:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outANotExpr(self, node):
		'''Manage 'not' expression
		   Error Conditions
		    * expression type not boolean'''
		self.printFunc(self.outANotExpr, node)
		ln = node.getOp().getLine()
		tp = self.typeMap[node.getExpr()]
		tp_ret = Type.BOOLEAN
		if tp != Type.BOOLEAN:
			tp_ret = Type.NONE
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' operation requires type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret

	def outAMultExpr(self, node):
		'''Manage 'mult' expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAMultExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' multiplication requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outADivExpr(self, node):
		'''Manage 'div' expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAMultExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' division requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outAAddExpr(self, node):
		'''Manage 'add' expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outAAddExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' addition requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret
	
	def outASubExpr(self, node):
		'''Manage 'sub' expr4 expression
		   Error Conditions
		    * lhs type != Type.INT and rhs type != Type.INT'''
		self.printFunc(self.outASubExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.INT])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' subtraction requires 2 operands of type " +
									  Type.INT.name(), ln)
		self.typeMap[node] = tp_ret

	def outAConcatExpr(self, node):
		'''Manage 'concat' expression
		   Error Conditions
		    * lhs type != Type.STRING and rhs type != Type.STRING'''
		self.printFunc(self.outAConcatExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be INT
		tp_ret = self.checkBinExprTypes(node, [Type.STRING])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' concatenation requires 2 operands of type " +
									  Type.STRING.name(), ln)
		self.typeMap[node] = tp_ret

	def outALteExpr(self, node):
		'''Manage 'less than or equal' expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outALteExpr)
		ln = node.getOp().getLine()
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

	def outAGteExpr(self, node):
		'''Manage 'greater than or equal' expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outAGteExpr, node)
		ln = node.getOp().getLine()
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

	def outALtExpr(self, node):
		'''Manage 'Less than' expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outALtExpr, node)
		ln = node.getOp().getLine()
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

	def outAGtExpr(self, node):
		'''Manage 'greater than' expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING)
		    * rhs_type != (Type.INT | Type.STRING)'''
		self.printFunc(self.outAGtExpr, node)
		ln = node.getOp().getLine()
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

	def outAEqExpr(self, node):
		'''Manage 'equal to' expression
		   Error Conditions
		    * lhs type != rhs type
		    * lhs_type != (Type.INT | Type.STRING | Type.BOOLEAN)
		    * rhs_type != (Type.INT | Type.STRING | Type.BOOLEAN)'''
		self.printFunc(self.outAEqExpr, node)
		ln = node.getOp().getLine()
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

	def outAAndExpr(self, node):
		'''Manage 'and' expression
		   Error Conditions
		    * lhs type != Type.BOOLEAN and rhs type != Type.BOOLEAN'''
		self.printFunc(self.outAAndExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be BOOLEAN
		tp_ret = self.checkBinExprTypes(node, [Type.BOOLEAN])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' and-logic requires 2 operands of type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret

	def outAOrExpr(self, node):
		'''Manage 'or' expression
		   Error Conditions
		    * lhs type != Type.BOOLEAN and rhs type != Type.BOOLEAN'''
		self.printFunc(self.outAOrExpr, node)
		ln = node.getOp().getLine()
		(lhs, rhs, tp_lhs, tp_rhs) = self.readBinExpr(node)
		
		#operand type must be BOOLEAN
		tp_ret = self.checkBinExprTypes(node, [Type.BOOLEAN])
		
		#incorrect operand types
		if tp_ret == Type.NONE:
			G.errors().semantic().add("'" + node.toString().strip() +
									  "' or-logic requires 2 operands of type " +
									  Type.BOOLEAN.name(), ln)
		self.typeMap[node] = tp_ret

	###########################################################################
	## MISCELLANEOUS STUFF                                                   ##
	###########################################################################
	def outACall(self, node):
		'''Manage a method 'call'
		   Error Conditions
		    * object does not contain method id
		    * method id does not exist in 'me'
		    * wrong number of parameters
		    * wrong parameter types'''
		self.printFunc(self.outACall, node)
		tp_map = G.typeMap()
		ln = node.getId().getLine()
		nm = node.getId().getText()
		klass = None
		if node.getExpr():
			klass = self.typeMap[node.getExpr()]
		if klass:
			klass = klass.typeName()
		else:
			klass = self.curClass()
		decl = G.typeMap().method(klass, nm) #FIXME - only allows calls to methods within the same class
		if not decl:
			decl = G.typeMap().func(nm)
		if not decl:
			decl = G.typeMap().extern(nm)
		ls_args = [self.typeMap[a] for a in node.getArgs()]

		tp_ret = Type.NONE
		#id does not exist or is not a method id
		if decl == None or not isinstance(decl, (MethodDecl, ExternDecl, FuncDecl)):
			G.errors().semantic().add("method '" + nm + "' does not exist", ln)
		#check for correct number and type of parameters
		elif len(ls_args) > 0:
			params = [tp_map.klass(p.typeName()) for p in decl.params()]
			if len(params) != len(ls_args):
				G.errors().semantic().add("method '" + nm + "' expects " +
										  str(len(params)) +
										  " parameter(s) but was given " +
										  str(len(ls_args)), ln)
			elif ls_args != params:
				G.errors().semantic().add("method '" + nm +
										  "' expects parameters " +
										  str([str(p) for p in params]) +
										  " but was given " +
										  str([str(a) for a in ls_args]), ln)
		#get method return type
		if decl != None:
			tp_ret = G.typeMap().klass(decl.typeName())
		
		self.typeMap[node] = tp_ret
	
	