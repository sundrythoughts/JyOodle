#Lexer.py
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
# * Neither the name of the <ORGANIZATION> nor the names of its contributors may
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

import java.lang

from java.io import BufferedReader
from java.io import FileNotFoundException
from java.io import FileReader
from java.io import IOException
from java.io import PushbackReader

from cps450.oodle import lexer
from cps450.oodle.lexer import LexerException
from cps450.oodle.node import *

from oodle.G import G

class Lexer(lexer.Lexer):
	'''Lexer. Inherits from the SableCC generated Lexer.
	   Reimplements the filter() method to customize behavior.
	   Prints all tokens if "-ds" is not an option.
	   Otherwise it only prints errors'''
	
	def __init__(self, fn):
		'''Initialize the Lexer
		   @fn: file name'''
		lexer.Lexer.__init__(self, PushbackReader(BufferedReader(FileReader(fn)), 1024))
		self.m_file_name = fn
	
	def nextToken(self):
		'''Get the next token from the Lexer.
		   Can be used to control which token the Lexer stops at.
		   @RETURN: Token'''
		t = None #Token
		t = self.next()
		return t

	def filter(self):
		'''Check and identify each token.
		   Used to ignore some tokens and print others.'''
		tk = self.peek() #Token
	 	if isinstance(tk, (TLineCont, TComment, TBlank)):
	 		tk = None #do not send to parser
		elif isinstance(tk, EOF):
			pass
		elif isinstance(tk, TEol):
			self.printNoError("cr", "")
		elif isinstance(tk, TId):
			self.printNoError("identifier")
		elif isinstance(tk, TIllegalChar):
			self.printError("Unrecognized char")
			tk = None; #do not send to parser
		elif isinstance(tk, TIntLit):
			self.printNoError("intlit")
		elif isinstance(tk, TStrLit):
			self.printNoError("string lit")
		elif isinstance(tk, TStrLitIllegal):
			self.printError("Illegal string")
		elif isinstance(tk, TStrLitUnterminated):
			self.printError("Unterminated string")
		else:
			self.printNoError("keyword")

	def printNoError(self, tok_name, txt=None):
		'''Print non-error messages
		   @tok_name: token name
		   @txt: custom token text'''
		#don't display tokens when -ds option is off
		if not G.options().displayTokens():
			return
		self.printMsg(tok_name, txt)

	def printError(self, tok_name, txt=None):
		'''Print error messages and also add it to the Lex error log 
		   @tok_name: token name
		   @txt: custom token text'''
		msg = self.printMsg(tok_name, txt)
		G.errors().lex().add(msg)
		
	def printMsg(self, tok_name, txt=None):
		'''Do the actual making and printing of the message
		   @tok_name: token name
		   @txt: token text
		   @RETURN: the message'''
		tk = self.peek() #Token
		txt = ':' + tk.getText() if txt == None else "" 
		msg = G.fileConcat().correctNameAndNumber(tk.getLine()) + ',' + str(tk.getPos()) + ':' + tok_name + txt
		print msg
		return msg
