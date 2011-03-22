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
