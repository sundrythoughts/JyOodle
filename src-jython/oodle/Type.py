class Type:
	''''''
	def __init__(self, nm):
		''''''
		self.m_name = nm
	
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

ARRAY   = Type('array')
BOOLEAN = Type('boolean')
ERROR   = Type('<error>')
INT     = Type('int')
STRING  = Type('string')
UDT     = Type('udt')
VOID    = Type('void')
NULL    = Type('null')
NONE    = Type('none')
