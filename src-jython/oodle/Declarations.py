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

from oodle.Type import Type

class Declaration:
	''''''
	def __init__(self):
		''''''
		self.m_name = ""
		self.m_type_name = ""

	def name(self):
		'''Get the name'''
		return self.m_name
	
	def setName(self, nm):
		'''Set the name'''
		self.m_name = nm

	def typeName(self):
		'''Get the type name'''
		return self.m_type_name
	
	def setTypeName(self, nm):
		'''Set the type name'''
		self.m_type_name = nm

class ClassDecl(Declaration):
	''''''
	def __init__(self, nm):
		'''Must initialize with a name'''
		Declaration.__init__(self)

		self.m_parent_class = None #assume base class to start with

		self.m_var_list = list() #list of VarDecls
		self.m_var_dict = dict() #dict of VarDecl pointers indexed by name 

		self.m_method_list = list() #list of MethodDecls
		self.m_method_dict = dict() #dict of MethodDecl pointers indexed by name
		
		#set the name and the typeName to be the same
		self.setName(nm)
		self.setTypeName(nm)

	def __str__(self):
		'''Get ClassDecl as string'''
		s = 'class ' + self.name()
		if self.parent():
			s = s + ' : ' + self.parent() 
		for v in self.m_var_list:
			s = s + '\n\t' + str(v)
		for m in self.m_method_list:
			s = s + '\n\t' + str(m)
		return s + '\n'
	
	def parent(self):
		'''Get the parent class'''
		return self.m_parent_class
	
	def setParent(self, p):
		'''Set the parent class'''
		self.m_parent_class = p

	def addVar(self, var_decl):
		'''Add VarDecl to class'''
		self.m_var_list.append(var_decl)
		
		#point the dict index to the last element inserted in the list
		self.m_var_dict[var_decl.name()] = self.m_var_list[-1]

	def var(self, nm):
		'''Get variable by name or None if name is not valid'''
		return self.m_var_dict[nm] if nm in self.m_var_dict else None

	def vars(self):
		'''Get the variable list'''
		return self.m_var_list
	
	def addMethod(self, meth_decl):
		'''Add MethodDecl to class'''
		self.m_method_list.append(meth_decl)
		
		#point the dict index to the last element inserted in the list
		self.m_method_dict[meth_decl.name()] = self.m_method_list[-1]

	def method(self, nm):
		'''Get method by name or None if name is not valid'''
		return self.m_method_dict[nm] if nm in self.m_method_dict else None
	
	def methods(self):
		'''Get method list'''
		return self.m_method_list

	def exists(self, nm):
		'''does name already exist in this scope'''
		if nm in self.m_var_dict or nm in self.m_method_dict:
			return True
		return False

class MethodDecl(Declaration):
	''''''
	def __init__(self, nm, tp_nm='void'):
		''''''
		self.m_param_list = list() #parameters of LocalVarDecl
		self.m_param_dict = dict() #index on LocalVarDecl.name() into list above
		
		self.m_var_list = list() #vars of LocalVarDecl
		self.m_var_dict = dict() #index on LocalVarDecl.name() into list above
		
		self.setName(nm)        #method name
		self.setTypeName(tp_nm) #method return type name
	
	def __str__(self):
		'''Get MethodDecl as string'''
		s = self.typeName() + ' '
		s += self.name()
		s = s + '(' + ', '.join([str(t) for t in self.m_param_list]) + ')'
		for v in self.m_var_list:
			s = s + '\n\t\t' + str(v)
		return s 
	
	def __eq__(self, d):
		'''Check for MethodDecl equivalence'''
		if not isinstance(d, MethodDecl):
			return False
		return (self.m_arg_types == d.m_arg_types) and (self.m_ret_type == d.m_ret_type)
	
	def addParam(self, p):
		self.m_param_list.append(p)
		self.m_param_dict[p.name()] = self.m_param_list[-1]

	def param(self, nm):
		'''Get param by name or None if name is not valid'''
		return self.m_param_dict[nm] if nm in self.m_param_dict else None
	
	def params(self):
		'''Get the param list'''
		return self.m_param_list

	def addVar(self, var_decl):
		self.m_var_list.append(var_decl)
		self.m_var_dict[var_decl.name()] = self.m_var_list[-1]

	def var(self, nm):
		'''Get variable by name or None if name is not valid'''
		return self.m_var_dict[nm] if nm in self.m_var_dict else None

	def vars(self):
		'''Get the variable list'''
		return self.m_var_list

	def exists(self, nm):
		'''does variable name already exist in this scope'''
		if nm in self.m_var_dict or nm in self.m_param_dict:
			return True
		return False

	def retTypeName(self):
		'''Get the return type--same as self.typeName()'''
		return self.typeName()

	def setRetTypeName(self, nm):
		'''Set the return type--same as self.setTypeName()'''
		self.setTypeName(nm)

class VarDecl(Declaration):
	''''''
	def __init__(self, nm, tp_nm):
		'''Must pass the type name and name of the variable'''
		Declaration.__init__(self)
		self.setName(nm)
		self.setTypeName(tp_nm)
		self.m_offset = 0
	
	def __eq__(self, d):
		'''Check for VarDecl equivalence'''
		if not isinstance(d, VarDecl):
			return False
		return self.typeName() == d.typeName()

	def __str__(self):
		'''Get VarDecl as string'''
		return self.typeName() + ' ' + self.name()

	def offset(self):
		'''get the memory offset of the variable'''
		return self.m_offset

	def setOffset(self, o):
		'''set the memory offset of the variable'''
		self.m_offset = o

class LocalVarDecl(VarDecl):
	'''Store local variables'''
	def __init__(self, nm, tp_nm):
		'''Must pass the type name and name of the variable'''
		VarDecl.__init__(self, nm, tp_nm)

	def __eq__(self, d):
		'''Check for LocalVarDecl equivalence'''
		if not isinstance(d, LocalVarDecl):
			return False
		return self.typeName() == d.typeName()

class InstanceVarDecl(VarDecl):
	'''Store instance variables'''
	def __init__(self, nm, tp_nm):
		'''Must pass the type name and name of the variable'''
		VarDecl.__init__(self, nm, tp_nm)

	def __eq__(self, d):
		'''Check for InstanceVarDecl equivalence'''
		if not isinstance(d, InstanceVarDecl):
			return False
		return self.typeName() == d.typeName()
