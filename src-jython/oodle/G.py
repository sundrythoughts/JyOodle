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

from oodle.Errors import Errors
from oodle.FileConcat import FileConcat
from oodle.Options import Options
from oodle.SymbolTable import SymbolTable
from oodle.SymbolMap import SymbolMap
from oodle.TypeMap import TypeMap

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

	#@staticmethod
	#def symTab():
	#	'''@RETURN: SymbolTable reference'''
	#	return SymbolTable.symTab()
	
	@staticmethod
	def symMap():
		'''@RETURN: SymbolMap reference'''
		return SymbolMap.symMap()
	
	@staticmethod
	def typeMap():
		'''@RETURN: TypeMap reference'''
		return TypeMap.typeMap()
