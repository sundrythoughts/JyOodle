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

class Type:
	st_type_map = dict()
	
	''''''
	def __init__(self, nm, decl):
		''''''
		self.m_name = nm
		self.m_class_decl = decl
	
	def __eq__(self, t):
		'''Check for Type equivalence'''
		if not isinstance(t, Type):
			return False
		return self.m_name == t.m_name
	
	def __ne__(self, t):
		'''Check for Type non-equivalence'''
		return not(self == t)
	
	def name(self):
		'''Get name of Type'''
		return self.m_name
	
	def decl(self):
		''''''
		return self.m_class_decl

	@staticmethod
	def add(nm, decl):
		tp = Type(nm, decl)
		Type.st_type_map[nm] = tp 
		return tp

	@staticmethod
	def byName(nm):
		if nm in Type.st_type_map:
			return Type.st_type_map[nm]
		else:
			return None

	@staticmethod
	def printTypeMap():
		print '--------------------------'
		print '        Type Map          '
		print '--------------------------'
		for k in Type.st_type_map:
			print Type.st_type_map[k].name()

ARRAY   = Type.add('array', None)
BOOLEAN = Type.add('boolean', None)
ERROR   = Type.add('<error>', None)
INT     = Type.add('int', None)
STRING  = Type.add('string', None)
UDT     = Type.add('udt', None)
VOID    = Type.add('void', None)
NULL    = Type.add('null', None)
NONE    = Type.add('none', None)
