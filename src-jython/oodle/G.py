from oodle.Errors import Errors
from oodle.FileConcat import FileConcat
from oodle.Options import Options
from oodle.SymbolTable import SymbolTable

class G:
	'''Globals. Holds static references to "singletons" and other globals'''
	
	@staticmethod
	def errors():
		'''@RETURN: Error reference'''
		return Errors.errors()
	
	@staticmethod
	def fileConcat():
		'''@RETURN: FileConcat reference'''
		return FileConcat.fileConcat()
	
	@staticmethod
	def options():
		'''@RETURN: Options reference'''
		return Options.options()

	@staticmethod
	def symTab():
		'''@RETURN: SymbolTable reference'''
		return SymbolTable.symTab()
