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

from java.io import *
from java.util import ArrayList
from java.util import Date

from cps450.oodle.parser import ParserException

class FileConcat:
	''''''
	
	st_fconcat = None #static FileConcat

	def __init__(self):
		self.m_file_dump = None #FileDump
		try:
			self.m_file_dump = FileDump ()
		except IOException, e:
			e.printStackTrace()
		self.m_file_info = list() #ArrayList<FileInfo>
	
	def appendFile(self, fn):
		'''@fn: file name'''
		start_line = self.m_file_dump.getLineCount()
		f = File (fn)
		frd = FileReader (f)
		lrd = LineNumberReader(frd)

		ln = lrd.readLine()
		while ln != None:
			self.m_file_dump.writeLine(ln)
			ln = lrd.readLine()
		self.m_file_dump.flush ()

		self.m_file_info.append(FileInfo (f, start_line, lrd.getLineNumber()))

	def correctParserException(self, ex):
		'''@ex: ParserException'''
		#FIXME
		pass
	
	def correctNameAndNumber(self, line_num):
		'''@line_num: line number
		   @RETURN: the original filename and the line number'''
		fi = self.correctInfo (line_num) #FileInfo
		return fi.getFileName() + ":" + str(line_num - fi.getDumpStartLine() + 1)
	
	def correctInfo(self, line_num):
		'''@line_num: line number
		   @RETURN: correct FileInfo structure'''
		for fi in self.m_file_info:
			if line_num <= fi.getDumpEndLine ():
				return fi
		return self.m_file_info[-1] #FIXME may not be completely accurate
	
	def getConcatFile(self):
		'''@RETURN: '''
		return self.m_file_dump.getFile()
	
	def printFileList(self):
		for fi in self.m_file_info:
			print fi.getFileName()
			print '\t' + str(fi.getDumpStartLine ())
			print '\t' + str(fi.getLineCount())
	
	@staticmethod
	def fileConcat():
		'''@RETURN: '''
		if FileConcat.st_fconcat == None:
			FileConcat.st_fconcat = FileConcat()
		return FileConcat.st_fconcat

class FileDump:
	''''''
	def __init__(self):
		'''@RETURN: '''
		dt = Date ()
		self.m_temp_file = File.createTempFile(str(dt.getTime()), '.ood')
		self.m_temp_file.deleteOnExit()
		self.m_temp_file_writer = FileWriter(self.m_temp_file)
		self.m_line_count = 1
	
	def writeLine(self, s):
		'''@s: line to write to file'''
		self.m_temp_file_writer.write(s + '\n')
		self.m_line_count += 1
	
	def flush(self):
		''''''
		self.m_temp_file_writer.flush ()
	
	def getLineCount(self):
		'''@RETURN: '''
		return self.m_line_count
	
	def getFile(self):
		'''@RETURN: '''
		return self.m_temp_file

class FileInfo:
	''''''
	def __init__(self, f, ln_start, ln_count):
		'''
		@f: File
		@ln_start: start line in dump
		@ln_count: num lines
		'''
		self.m_absolute_path = f.getAbsolutePath()
		self.m_file_name = f.getName()
		self.m_num_lines = ln_count
		self.m_start_line_in_dump = ln_start
	
	def getDumpStartLine(self):
		'''@RETURN: '''
		return self.m_start_line_in_dump
	
	def getDumpEndLine(self):
		'''@RETURN: '''
		return self.m_start_line_in_dump + self.m_num_lines - 1
	
	def getLineCount(self):
		'''@RETURN: '''
		return self.m_num_lines
	
	def getFileName(self):
		'''@RETURN: '''
		return self.m_file_name;
	
	def getAbsolutePath(self):
		'''@RETURN: '''
		return self.m_absolute_path
	
	def printOut(self):
		''''''
		print '{0}\n{1}\n{2}\n{3}'.format(self.m_start_line_in_dump,
										self.m_num_lines,
										self.m_file_name,
										self.m_absolute_path)
		