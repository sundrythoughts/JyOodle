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

class Symbol:
	''''''
	def __init__(self):
		''''''
		self.m_scope = 0
		self.m_name = ""
		self.m_decl = None #Declaration
	
	def scope(self):
		'''
		   @RETURN: Symbol scope -> int'''
		return self.m_scope

	def setScope(self, sc):
		'''
		   @sc: Symbol scope -> int
		   @RETURN: this Symbol -> Symbol'''
		self.m_scope = sc
		return self
	
	def name(self):
		'''
		   @RETURN: Symbol name -> String'''
		return self.m_name

	def setName(self, nm):
		'''
		   @nm: Symbol name -> String
		   @RETURN: this Symbol -> Symbol'''
		self.m_name = nm
		return self

	def decl(self):
		'''
		   @RETURN: Symbol declaration -> Declaration'''
		return self.m_decl;

	def setDecl(self, d):
		'''
		   @d: Symbol declaration -> Declaration
		   @RETURN: this Symbol -> Symbol'''
		self.m_decl = d
		return self
	
	def __str__(self):
		ret = self.m_name + ', ' + str(self.m_scope) + ', ' + str(self.m_decl) 
		return ret
