from java.io import IOException
from java.io import InputStreamReader
from java.io import PushbackReader
from java.io import BufferedReader
from java.io import FileReader

from cps450.oodle.lexer import Lexer
from cps450.oodle.lexer import LexerException
from cps450.oodle.node import *


class LexerTest:
	def __init__(self):
		self.m_lex = None

	def testSuccessfulScan(self):
		self.m_lex = Lexer(PushbackReader(BufferedReader(FileReader("lexertest.ood")), 1024))
		
		#line 1
		self.assertNextToken(TComment)
		self.assertNextToken(TEol)
		
		#line 2
		self.assertNextToken(TEol)
		
		#line 3
		self.assertNextToken(TId)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwBoolean)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TMiscLParen)
		self.assertNextToken(TKwTrue)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwOr)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwFalse)
		self.assertNextToken(TMiscRParen)
		self.assertNextToken(TEol)
		
		#line 4
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwInt)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpMult)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpPlus)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TEol)
		
		#line 5
		self.assertNextToken(TId)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwString)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TStrLit)
		self.assertNextToken(TEol)
		
		#line 6
		self.assertNextToken(TId)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwString)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TStrLitIllegal)
		self.assertNextToken(TEol)
		
		#line 7
		self.assertNextToken(TId)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwString)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TStrLitUnterminated)
		self.assertNextToken(TEol)
		
		#line 8
		self.assertNextToken(TKwClass)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwInherits)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwFrom)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwIs)
		self.assertNextToken(TEol)
		
		#line 9
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TMiscLParen)
		self.assertNextToken(TKwInt)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TMiscRParen)
		self.assertNextToken(TBlank)
		self.assertNextToken(TMiscColon)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwInt)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwIs)
		self.assertNextToken(TEol)
		
		#line 10
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwBegin)
		self.assertNextToken(TEol)
		
		#line 11
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwIf)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpGt)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwThen)
		self.assertNextToken(TEol)
		
		#line 12
		self.assertNextToken(TBlank)
		self.assertNextToken(TComment)
		self.assertNextToken(TEol)
		
		#line 13
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwElse)
		self.assertNextToken(TEol)
		
		#line 14
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TEol)
		
		#line 15
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwLoop)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwWhile)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpGt)
		self.assertNextToken(TBlank)
		self.assertNextToken(TIntLit)
		self.assertNextToken(TEol)
		
		#line 16
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpAssign)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TBlank)
		self.assertNextToken(TOpMult)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TEol)
		
		#line 17
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwEnd)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwLoop)
		self.assertNextToken(TEol)
		
		#line 18
		self.assertNextToken(TBlank)
		self.assertNextToken(TComment)
		self.assertNextToken(TEol)
		
		#line 19
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwEnd)
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwIf)
		self.assertNextToken(TEol)
		
		#line 20
		self.assertNextToken(TBlank)
		self.assertNextToken(TKwEnd)
		self.assertNextToken(TBlank)
		self.assertNextToken(TId)
		self.assertNextToken(TEol)

	#def assertNextToken(self, tp, val):
	#	tok = self.m_lex.next()
	#	print tok
	#	assertTrue(tok.getClass() == tp)
	#	assertTrue(tok.getText() == val)

	def assertNextToken(self, tp):
		tok = self.m_lex.next()
		print tok
		assert(isinstance(tok, tp))

if __name__ == "__main__":
	test = LexerTest()
	test.testSuccessfulScan()
