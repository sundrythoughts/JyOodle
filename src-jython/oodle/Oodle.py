#Oodle.py
#by Joseph Freeman

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
	
	code_gen = CodeGenx86()
	st_node.apply(code_gen)
	code_gen.printAsm()

if __name__ == "__main__":
	main()
