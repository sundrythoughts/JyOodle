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
		pass

class ClassDecl(Declaration):
	''''''
	def __init__(self):
		''''''
		Declaration.__init__(self)
	
	def __str__(self):
		'''Get ClassDecl as string'''
		return 'class'

class MethodDecl(Declaration):
	''''''
	def __init__(self, arg_types, ret_type):
		''''''
		self.m_arg_types = arg_types #list of Type
		self.m_ret_type = ret_type #Type
	
	def __str__(self):
		'''Get MethodDecl as string'''
		ret = 'method: ' + str([t.name() for t in self.m_arg_types])
		ret += ' -> '
		ret += self.m_ret_type.name()
		return ret 
	
	def __eq__(self, d):
		'''Check for MethodDecl equivalence'''
		if not isinstance(d, MethodDecl):
			return False
		return (self.m_arg_types == d.m_arg_types) and (self.m_ret_type == d.m_ret_type)
	
	def argStr(self):
		return str([t.name() for t in self.m_arg_types])
	
	def argTypes(self):
		return self.m_arg_types
	
	def setArgTypes(self, ls):
		self.m_arg_types = ls
	
	def retType(self):
		return self.m_ret_type
	
	def setRetType(self, r):
		self.m_ret_type = r

class VarDecl(Declaration):
	''''''
	def __init__(self, t):
		''''''
		Declaration.__init__(self)
		self.m_type = t #Type
	
	def __eq__(self, d):
		'''Check for VarDecl equivalence'''
		if not isinstance(d, VarDecl):
			return False
		return self.m_type == d.m_type

	def __str__(self):
		'''Get VarDecl as string'''
		return 'var: ' + self.m_type.name()

	def varType(self):
		return self.m_type
	
	def setVarType(self, t):
		self.m_type = t
