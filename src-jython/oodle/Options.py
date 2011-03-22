#Options.py
#by Joseph Freeman

from java.util import *

#Class for parsing command-line options. It also stores the input file list.
#It works as a singleton.
#
#FIXME - right now this is only for Options that have no parameters
class Options:
	''''''
	opts = None #static self-ref
	
	def __init__(self):
		''''''
		self.m_opts = dict() #{str:bool}
		self.m_files = list() #[str]
		self.m_opts['-ds'] = False

	def parseArgs(self, args):
		'''Parse the command-line arguments.
		   @args: string list '''
		for a in args:
			if a in self.m_opts:
				self.m_opts[a] = True
			else:
				self.m_files.append(a)
	
	def getFileList(self):
		''''''
		return self.m_files
	
	def displayTokens(self):
		'''[Option = -ds] -> should tokens be displayed or not'''
		return self.m_opts['-ds']
	
	@staticmethod
	def options():
		''''''
		if Options.opts == None:
			Options.opts = Options()
		return Options.opts
