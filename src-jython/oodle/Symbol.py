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
		ret = self.m_name + ', ' + str(self.m_decl) + ', ' + str(self.m_scope)
		return ret
