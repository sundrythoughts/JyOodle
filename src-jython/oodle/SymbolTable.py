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

from oodle.Symbol import Symbol

class SymbolTableScopeError(Exception):
	'''Generally used when the scope level of the Symbol Table drops below 0'''
	pass

class SymbolTable:
	''''''
	st_symtab = None #static SymbolTable
	
	def __init__(self):
		''''''
		self.m_scope = 0
		self.m_tab = list() #list of Symbol

	def push(self, nm, decl):
		'''
		   @nm: symbol name -> String
		   @decl: Declaration
		   @RETURN: the Symbol at the top of the table'''
		s = Symbol()
		s.setName(nm).setScope(self.m_scope).setDecl(decl)
		self.m_tab.insert(0, s)
		return s
	
	def lookup(self, nm):
		'''
		   @nm: symbol name -> String
		   @RETURN: the Symbol or None if not found'''
		for s in self.m_tab:
			if s.name() == nm:
				return s
		return None
	
	def beginScope(self):
		'''Start a new scope in the table'''
		self.m_scope += 1
	
	def endScope(self):
		'''End the current scope in the table'''
		while len(self.m_tab) > 0 and self.m_tab[0].scope() == self.m_scope:
			self.m_tab.pop(0)
		if self.m_scope - 1 < 0:
			#FIXME
			#Raise an exception if the scope level would drop below 0.
			#print "FIXME: SymbolTable.endscope() should raise an exception."
			raise SymbolTableScopeError('Scope level dropped below 0')
		self.m_scope -= 1

	def getScope(self):
		'''
		   @RETURN: scope number -> int'''
		return self.m_scope

	@staticmethod
	def symTab():
		'''Singleton method for this class'''
		if SymbolTable.st_symtab == None:
			SymbolTable.st_symtab = SymbolTable ()
		return SymbolTable.st_symtab
	
	def printTable(self):
		'''Debug method for printing the SymbolTable'''
		print '------------------------------'
		print 'Symbol Table'
		print '------------------------------'
		for s in self.m_tab:
			print str(s)
