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
		self.m_opts['-S'] = False
		self.m_print_debug = False

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

	def generateAssembly(self):
		'''[Option = -S] -> should generate assembly or not'''
		return self.m_opts['-S']

	def printDebug(self):
		return self.m_print_debug

	def setPrintDebug(self, p=False):
		self.m_print_debug = p
	
	@staticmethod
	def options():
		''''''
		if Options.opts == None:
			Options.opts = Options()
		return Options.opts
