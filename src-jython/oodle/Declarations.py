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
