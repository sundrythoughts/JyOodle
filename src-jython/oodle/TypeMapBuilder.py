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

class TypeMapBuilder(DepthFirstAdapter):
	'''Build the TypeMap which will be used during semantic checking.
	   Only produces an error when an identifier is used multiple times in the
	   same scope.'''
	def __init__(self):
		DepthFirstAdapter.__init__(self)
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
			print 'TypeMapBuilder: ' + f.__name__ + n
	
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
	## METHOD DECLARATION STUFF                                              ##
	###########################################################################
	def inAMethodSig(self, node):
		''''''
		self.printFunc(self.inAMethodSig, node)

		klass = G.typeMap().klass(self.curClass())
		nm = node.getId().getText()
		if klass.exists(nm):
			G.errors().semantic().add("method '" + nm + "' already exists", ln)
		else:
			klass.addMethod(MethodDecl(nm))
			self.setCurMethod(nm)

		ln = node.getId().getLine()
		
		meth = G.typeMap().klass(self.curClass()).method(self.curMethod())
		if node.getRet():
			tp = node.getRet().getTp().getText()
			meth.setTypeName(tp) #set the return type name

	def inAArg(self, node):
		''''''
		self.printFunc(self.inAArg, node)
		ln = node.getId().getLine()
		
		meth = G.typeMap().klass(self.curClass()).method(self.curMethod())
		nm = node.getId().getText()
		tp = node.getTp().getTp().getText()
		if meth.exists(nm):
			G.errors().semantic().add("variable '" + nm + "' already exists", ln)
		else:
			var_decl = LocalVarDecl(nm, tp)
			meth.addParam(var_decl) #add var to TypeMap

	def outAMethod(self, node):
		''''''
		self.printFunc(self.outAMethod)

		meth = G.typeMap().klass(self.curClass()).method(self.curMethod())
		vars = node.getVars()
		for v in vars:
			ln = v.getId().getLine()
			nm = v.getId().getText()
			tp = ""
			if v.getTp():
				tp = v.getTp().getTp().getText()
			if meth.exists(nm):
				G.errors().semantic().add("variable '" + nm + "' already exists", ln)
			else:
				var_decl = LocalVarDecl(nm, tp)
				meth.addVar(var_decl) #add var to TypeMap

	###########################################################################
	## CLASS DECLARATION STUFF                                               ##
	###########################################################################
	def inAKlassHeader(self, node):
		''''''
		self.printFunc(self.inAKlassHeader, node)
		ln = node.getId().getLine()
		
		tp_map = G.typeMap() 
		
		nm = node.getId().getText() #class name
		
		if tp_map.klassExists(nm):
			G.errors().semantic().add("class '" + nm + "' already exists", ln)
		else:
			tp_map.addKlass(ClassDecl(nm)) #add class to TypeMap
			self.setCurClass(nm)

	def inAKlassInherits(self, node):
		''''''
		self.printFunc(self.inAKlassInherits, node)
		ln = node.getId().getLine()
		
		tp_map = G.typeMap()
		nm = node.getId().getText()
		tp_map.klass(self.curClass()).setParent(nm)

	def inAKlassBody(self, node):
		''''''
		self.printFunc(self.inAKlassBody)
				
		klass = G.typeMap().klass(self.curClass())
		vars = node.getVars()
		for v in vars:
			ln = v.getId().getLine()
			nm = v.getId().getText()
			tp = ""
			if v.getTp():
				tp = v.getTp().getTp().getText()
			
			if klass.exists(nm):
				G.errors().semantic().add("variable '" + nm + "' already exists", ln)
			else:
				var_decl = InstanceVarDecl(nm, tp)
				klass.addVar(var_decl) #add var to TypeMap
