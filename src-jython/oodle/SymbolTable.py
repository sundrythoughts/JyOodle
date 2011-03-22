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
		''''''
		self.m_scope += 1
	
	def endScope(self):
		''''''
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
		''''''
		if SymbolTable.st_symtab == None:
			SymbolTable.st_symtab = SymbolTable ()
		return SymbolTable.st_symtab
	
	def printTable(self):
		print '------------------------------'
		print 'Symbol Table'
		print '------------------------------'
		for s in self.m_tab:
			print str(s)
