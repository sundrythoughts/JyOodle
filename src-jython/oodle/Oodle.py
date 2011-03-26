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

from oodle.G import G
from oodle.Lexer import Lexer
from cps450.oodle.parser import Parser
from cps450.oodle.lexer import LexerException
from cps450.oodle.node import *
from cps450.oodle.parser import ParserException
from oodle.SemanticChecker import SemanticChecker
from oodle.CodeGenx86 import CodeGenx86
from java.io import *
import sys

class Oodle:
	'''Main class for the Oodle compiler
	   Takes command-line arguments and turns them into an Option class.
	   Then, it passes each file separately to the Lexer which may print
	   out the tokens. It ends each file when each reaches EOF.'''

	def __init__(self):
		pass

def main():
	if len(sys.argv) < 2:
		print "usage:"
		print "  java Oodle filename"
		sys.exit(-1)

	G.options().parseArgs(sys.argv[1:])

	flist = G.fileConcat ()
	for f in G.options().getFileList():
		flist.appendFile(f)

	st_node = None
	lex = Lexer(flist.getConcatFile().getAbsolutePath())
	par = Parser(lex)
	try:
		st_node = par.parse()
	except ParserException, e:
		G.errors().syntax().add(e.getMessage())
	except LexerException, f:
		print "LexerException in Oodle.__init__"
	
	if G.errors().hasErrors():
		G.errors().printErrors()
		sys.exit(-1)

	#perform semantic checks (new code)
	sem_check = SemanticChecker()
	st_node.apply(sem_check)  #invoke SemanticChecker traversal

	if G.errors().hasErrors():
		G.symTab().printTable()
		G.errors().printErrors()
		sys.exit(-1)
	
	if G.options().generateAssembly():
		code_gen = CodeGenx86()
		st_node.apply(code_gen)
		code_gen.printAsm()

if __name__ == "__main__":
	main()
