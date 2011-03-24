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

from java.util import ArrayList
from oodle.FileConcat import FileConcat

class LexErrors:
	''''''
	def __init__(self):
		self.m_err = list()
	
	def add(self, s):
		self.m_err.append(s)
	
	def count(self):
		return len(self.m_err)
	
	def hasErrors(self):
		return len(self.m_err) > 0
	
	def printErrors(self):
		for s in self.m_err:
			print s

class SyntaxErrors:
	''''''
	def __init__(self):
		self.m_err = list()
	
	def add(self, s):
		msg = s[s.find(']') + 1 :] #error message
		s = s[1 : s.find(']')] #line and column numbers
		ln = int(s[0 : s.find(',')]) #line number
		col = int(s[s.find(',') + 1 :]) #column number
		self.m_err.append(FileConcat.fileConcat()
						  .correctNameAndNumber(ln) + ',' +
						  str(col) + ':' + msg)
	
	def count(self):
		return len(self.m_err)
	
	def hasErrors(self):
		return len(self.m_err) > 0
	
	def printErrors(self):
		for s in self.m_err:
			print s

class SemanticErrors:
	''''''
	def __init__(self):
		self.m_err = list()
	
	def add(self, s, ln):
		self.m_err.append('Error: ' +
						  FileConcat.fileConcat().correctNameAndNumber(ln) +
						  ': ' + s)
	
	def addUnsupportedFeature(self, s, ln):
		self.m_err.append('Unsupported Feature: ' +
						  FileConcat.fileConcat().correctNameAndNumber(ln) +
						  ': ' + s)
	
	def count(self):
		return len(self.m_err)
	
	def hasErrors(self):
		return len(self.m_err) > 0
	
	def printErrors(self):
		for s in self.m_err:
			print s

class Errors:
	''''''
	st_err = None #static Errors
	
	def __init__(self):
		''''''
		self.m_lex_err_count = 0
		self.m_syntax_err_count = 0
		self.m_err = list()
		
		self.m_err_lex = LexErrors()
		self.m_err_syntax = SyntaxErrors()
		self.m_err_semantic = SemanticErrors()
	
	def lex(self):
		'''Lexical errors'''
		return self.m_err_lex
	
	def syntax(self):
		'''Syntactic errors'''
		return self.m_err_syntax
	
	def semantic(self):
		'''Semantic errors'''
		return self.m_err_semantic
	
	def hasErrors(self):
		return self.count() != 0
	
	def count(self):
		cnt = 0
		cnt += self.lex().count()
		cnt += self.syntax().count()
		cnt += self.semantic().count()
		return cnt

	def getLexErrorCount(self):
		''''''
		return self.m_lex_err_count
	
	def getSyntaxErrorCount(self):
		''''''
		return self.m_syntax_err_count
	
	def appendLexError(self, s):
		'''@s: Error string'''
		self.m_lex_err_count += 1
		self.m_err.append(s)
	
	def appendSyntaxError(self, s):
		'''@s: Error string'''
		msg = s[s.find(']') + 1 :] #error message
		s = s[1 : s.find(']')] #line and column numbers
		ln = int(s[0 : s.find(',')]) #line number
		col = int(s[s.find(',') + 1 :]) #column number
		self.m_syntax_err_count += 1
		self.m_err.append(FileConcat.fileConcat()
						  .correctNameAndNumber(ln) + ',' +
						  str(col) + ':' + msg)
	
	def printErrors(self):
		''''''
		print '-------------------------------------------------'
		print 'Results:'
		#for s in self.m_err:
		#	print s
		self.lex().printErrors()
		self.syntax().printErrors()
		self.semantic().printErrors()
		print '-------------------------------------------------'
		print str(self.lex().count()) + ' lexing error(s)'
		print str(self.syntax().count()) + ' syntax error(s)'
		print str(self.semantic().count()) + ' semantic error(s)'
		print '-------------------------------------------------'
		print str(self.count()) + ' error(s) found'
	
	@staticmethod
	def errors():
		''''''
		if Errors.st_err == None:
			Errors.st_err = Errors()
		return Errors.st_err
