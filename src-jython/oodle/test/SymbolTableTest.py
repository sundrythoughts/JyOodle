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
from oodle.SymbolTable import SymbolTable, SymbolTableScopeError
from oodle.Type import Type
from oodle import Type
from oodle.Declarations import VarDecl
from oodle.Declarations import MethodDecl

class SymbolTableTest:
	def testSymbolTable(self):
		table = SymbolTable.symTab()
		s = table.push('x', VarDecl(Type.INT))
		assert(s.name() == 'x')
		assert(s.scope() == 0)
		assert(s.decl() == VarDecl(Type.INT))
		s = table.push('intToBoolean', MethodDecl([Type.INT], Type.BOOLEAN))
		assert(s.name() == 'intToBoolean')
		assert(s.scope() == 0)
		assert(s.decl() == MethodDecl([Type.INT], Type.BOOLEAN))
		table.beginScope()
		s = table.push('x', VarDecl(Type.INT))
		assert(s.name() == 'x')
		assert(s.scope() == 1)
		assert(s.decl() == VarDecl(Type.INT))

		try:		
			table.endScope()
		except SymbolTableScopeError, e:
			assert(False)
		
		try:
			table.endScope()
		except SymbolTableScopeError, e:
			assert(True)

		table.printTable()
		print "SymbolTableTest.testSymbolTable = no errors"

if __name__ == "__main__":
	test = SymbolTableTest()
	test.testSymbolTable()
