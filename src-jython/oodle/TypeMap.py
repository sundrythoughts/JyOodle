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

from Declarations import *

class TypeMap:
	'''Store a tree of types'''
	st_type_map = None #singleton TypeMap instance

	def __init__(self):
		''''''
		#class declarations
		self.m_klass_list = list()
		self.m_klass_dict = dict()
		
		#extern declarations
		self.m_extern_list = list()
		self.m_extern_dict = dict()
		
		#global variable declarations
		self.m_glb_var_list = list()
		self.m_glb_var_dict = dict()

		#global function declarations
		self.m_func_list = list()
		self.m_func_dict = dict()

	def addFunc(self, f_decl):
		'''add a FuncDecl to the TypeMap'''
		nm = f_decl.name()
		if self.funcExists(nm):
			return self.func(nm)
		self.m_func_list.append(f_decl)
		self.m_func_dict[nm] = self.m_func_list[-1]
		return f_decl

	def func(self, nm):
		'''get function by name or None if name is invalid'''
		return self.m_func_dict[nm] if nm in self.m_func_dict else None
	
	def funcs(self):
		'''get list of functions'''
		return self.m_func_list	

	def funcExists(self, nm):		
		'''does function name already exist in this scope'''
		if nm in self.m_func_dict:
			return True
		return False

	def addGlbVar(self, glb_decl):
		'''add a GlobalVarDecl to the TypeMap'''
		nm = glb_decl.name()
		if self.glbVarExists(nm):
			return self.glbVar(nm)
		self.m_glb_var_list.append(glb_decl)
		self.m_glb_var_dict[nm] = self.m_glb_var_list[-1]
		return glb_decl

	def glbVar(self, nm):
		'''get global variable by name or None if name is invalid'''
		return self.m_glb_var_dict[nm] if nm in self.m_glb_var_dict else None
	
	def glbVars(self):
		'''get list of global variables'''
		return self.m_glb_var_list	

	def glbVarExists(self, nm):		
		'''does global variable name already exist in this scope'''
		if nm in self.m_glb_var_dict:
			return True
		return False

	def addExtern(self, func_decl):
		'''add a FunctionDecl extern to the TypeMap'''
		nm = func_decl.name()
		if self.externExists(nm):
			return self.extern(nm)
		self.m_extern_list.append(func_decl)
		self.m_extern_dict[nm] = self.m_extern_list[-1]
		return func_decl

	def extern(self, nm):
		'''get extern by name or None if name is invalid'''
		return self.m_extern_dict[nm] if nm in self.m_extern_dict else None
	
	def externs(self):
		'''get list of externs'''
		return self.m_extern_list

	def externExists(self, nm):
		'''does extern name already exist in this scope'''
		if nm in self.m_extern_dict:
			return True
		return False

	def addKlass(self, cl_decl):
		'''add a ClassDecl to the TypeMap'''
		nm = cl_decl.name()
		if self.klassExists(nm):
			return self.klass(nm)
		self.m_klass_list.append(cl_decl)
		self.m_klass_dict[nm] = self.m_klass_list[-1]
		return cl_decl

	def klass(self, nm):
		'''Get class by name or None if name is not valid'''
		return self.m_klass_dict[nm] if nm in self.m_klass_dict else None
	
	def klasses(self):
		'''get list of classes'''
		return self.m_klass_list

	def klassExists(self, nm):
		'''does class name already exist in this scope'''
		if nm in self.m_klass_dict:
			return True
		return False

	def method(self, cl_nm, meth_nm):
		'''find method in class'''
		cl = self.klass(cl_nm)
		if not cl:
			return None
		meth = cl.method(meth_nm)
		return meth  #may be None
	
	def retVar(self, cl_nm, meth_nm, var_nm):
		'''Find a MethodDecl which is the return variable given class name,
		   method name, and variable name'''
		#global functions
		if cl_nm == '':
			func = self.func(meth_nm)
			if not func:
				return None
			var = func.retVar(var_nm)
			return var
		#methods
		else:
			cl = self.klass(cl_nm)
			if not cl:
				return None
			meth = cl.method(meth_nm)
			if not meth:
				return None
			var = meth.retVar(var_nm) #get method return value
			return var #may be None
	
	def localVar(self, cl_nm, meth_nm, var_nm):
		'''Find a LocalVarDecl given a class name, method name, and variable name
		   Otherwise return None'''
		#global functions
		if cl_nm == '':
			func = self.func(meth_nm)
			if not func:
				return None
			var = func.var(var_nm)
			if not var:
				var = func.param(var_nm)
			return var
		#methods
		else:
			cl = self.klass(cl_nm)
			if not cl:
				return None
			meth = cl.method(meth_nm)
			if not meth:
				return None
			var = meth.var(var_nm) #check in method locals list
			if not var:
				var = meth.param(var_nm) #check in method parameter list
			return var #may be None

	def instVar(self, cl_nm, var_nm):
		'''Find an InstanceVarDecl given a class name and variable name
		   Otherwise return None'''
		if cl_nm == '':
			return None
		cl = self.klass(cl_nm)
		if not cl:
			return None
		var = cl.var(var_nm) #may be None
		return var

	def var(self, cl_nm, meth_nm, var_nm):
		'''find a variable scoped to a given class and method'''
		v = self.localVar(cl_nm, meth_nm, var_nm)
		if v:
			return v
		v = self.retVar(cl_nm, meth_nm, var_nm)
		if v:
			return v
		v = self.instVar(cl_nm, var_nm) #may return None
		return v
			

	def __str__(self):
		'''convert the TypeMap to a nicely formated string'''
		s = ""
		for e in self.m_extern_list:
			s = s + str(e) + '\n'
		for v in self.m_glb_var_list:
			s = s + str(v) + '\n'
		for f in self.m_func_list:
			s = s + str(f) + '\n'
		for c in self.m_klass_list:
			s += str(c)
		return s
	
	@staticmethod
	def typeMap():
		'''Singleton method for this class'''
		if TypeMap.st_type_map == None:
			TypeMap.st_type_map = TypeMap ()
		return TypeMap.st_type_map

class Type:
	'''Declare builtin types'''
	#declare builtin types
	BOOLEAN   = TypeMap.typeMap().addKlass(ClassDecl('boolean'))
	INT    = TypeMap.typeMap().addKlass(ClassDecl('int'))
	NULL   = TypeMap.typeMap().addKlass(ClassDecl('null'))
	STRING = TypeMap.typeMap().addKlass(ClassDecl('string'))
	VOID   = TypeMap.typeMap().addKlass(ClassDecl('void'))
	NONE   = TypeMap.typeMap().addKlass(ClassDecl('none'))

#TESTING CODE
if __name__ == '__main__':
	tpmap = TypeMap()
	cl = ClassDecl('Klass')

	m = MethodDecl('funcAdd', 'int')
	p1 = LocalVarDecl('x', 'int')
	p2 = LocalVarDecl('y', 'int')
	m.addParam(p1)
	m.addParam(p2)
	l = LocalVarDecl('sum', 'string')
	m.addVar(l)
	cl.addMethod(m)
	
	m = MethodDecl('takeNothingGiveNothing')
	cl.addMethod(m)

	v = VarDecl('m_inst', 'boolean')
	cl.addVar(v)

	tpmap.addKlass(cl)
	print str(tpmap)

