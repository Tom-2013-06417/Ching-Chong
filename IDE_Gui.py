import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QRegExp
from PyQt4.Qt import QWidget
from PyQt4.Qt import QTextFormat
from PyQt4.Qt import QVariant
from PyQt4.Qt import QPainter
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QRect

import subprocess

from ext import *



def format(color, style=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QtGui.QColor()
	_color.setNamedColor(color)

	_format = QtGui.QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QtGui.QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)

	return _format


# Syntax styles that can be shared by all languages
STYLES = {
	'keyword': format('#2B43BA'),
	'operator': format('red'),
	'brace': format('darkGray'),
	'defclass': format('black', 'bold'),
	'string': format('#A8CD3A'),
	'string2': format('#777777'),			 #Comments
	'comment': format('#777777', 'italic'),
	'self': format('black', 'italic'),
	'numbers': format('brown'),
	'terminator': format('green'),
	'loops': format('#FF7E00'),
	'startingline': format('#FF7E00'),
	'senderclass': format('#CD4422', 'bold'),	#Name of sender
	'defname': format('#FF7E00'),
}



class PythonHighlighter (QtGui.QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	keywords = [
		'and', 'assert', 'ask', 'again', 'break', 'class', 'continue', 'Homework', 'Finish homework',
		'del', 'Diary', 'no more', 'except', 'exec', 'finally',
		'from', 'From', 'global', 'Get me', 'get me', 'if', 'import', 'in', 
		'lambda', 'not', 'or', 'pass', 'raise', 'return', 'then', 'try', 'while', 'with', 'yield',
		'None', 'Own', 'Disown', 'GWA', 'Score', 'Essay', 'Honor', 'okay'
	]

	# Python operators
	operators = [		
		# Comparison
		'!=', '<', '<=', '>', '>=',
		'more lesser to', 'more greaterer to', 'same to', 'greaterer to', 'lesser to',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*',
		# In-place
		'\+=', '-=', '\*=', '/=', '\%=',
		# Bitwise
		'\^', '\|', '\&', '\~', '>>', '<<',
	]

	# Python braces
	braces = [
		'\{', '\}', '\(', '\)', '\[', '\]',
	]
	def __init__(self, document):
		QtGui.QSyntaxHighlighter.__init__(self, document)

		# Multi-line strings (expression, flag, style)
		# FIXME: The triple-quotes in these two lines will mess up the
		# syntax highlighting from this point onward
		self.tri_single = (QRegExp("-_-"), 1, STYLES['string2'])

		rules = []

		# Keyword, operator, and brace rules
		rules += [(r'%s' % o, 0, STYLES['operator']) for o in PythonHighlighter.operators]
		rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in PythonHighlighter.keywords]
		rules += [(r'%s' % b, 0, STYLES['brace']) for b in PythonHighlighter.braces]

		# All other rules
		rules += [
			# 'self'
			(r'\bself\b', 0, STYLES['self']),

			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

			# 'def' followed by an identifier
			(r'\bHi, I am\b\s*(\w+)\.', 1, STYLES['senderclass']),
			(r'\bHi, I am\b', 0, STYLES['startingline']),
			(r'Sincerely,\s*(\w+)\.', 1, STYLES['senderclass']),
			(r'Sincerely,', 0, STYLES['startingline']),
			# 'class' followed by an identifier
			(r'\bDear\b', 0, STYLES['defname']),
			(r'\bDear\b\s*(\w+)\,', 1, STYLES['defclass']),

			# From '#' until a newline			
			(r'lah.', 0, STYLES['terminator']),
			(r'Do your chores', 0, STYLES['loops']),
			(r'End chores', 0, STYLES['loops']),
			(r'I show Father', 0, STYLES['keyword']),
			(r'I give Father', 0, STYLES['keyword']),
			(r'Father wants', 0, STYLES['keyword']),
			(r'I write to', 0, STYLES['keyword']),
			(r'I get', 0, STYLES['keyword']),
			(r'Father surprise quiz:', 0, STYLES['keyword']),
			(r'Father surprise long quiz:', 0, STYLES['keyword']),
			(r'Father say make repeat', 0, STYLES['keyword']),
			(r'to become doctor', 0, STYLES['keyword']),
			(r'Father says that I need', 0, STYLES['keyword']),
			(r'Must do', 0, STYLES['keyword']),
			(r'I\'m done', 0, STYLES['keyword']),
			(r'Father ask', 0, STYLES['keyword']),
			(r'I double confirm', 0, STYLES['keyword']),
			(r'Father says that I need', 0, STYLES['keyword']),
			(r'Father ashamed of son for not answer', 0, STYLES['keyword']),
			(r'I want dumplings and', 0, STYLES['keyword']),
			(r'I send shrimp fried rice to all:', 0, STYLES['keyword']),
			(r'I no pass', 0, STYLES['keyword']),
			

			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

			(r'-.-[^\n]*', 0, STYLES['comment']),
		]

		# Build a QRegExp for each pattern
		self.rules = [(QRegExp(pat), index, fmt)
			for (pat, index, fmt) in rules]


	def highlightBlock(self, text):
		"""Apply syntax highlighting to the given block of text.
		"""
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				# We actually want the index of the nth match
				index = expression.pos(nth)
				length = expression.cap(nth).length()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line strings
		in_multiline = self.match_multiline(text, *self.tri_single)
		# if not in_multiline:
			# in_multiline = self.match_multiline(text, *self.tri_double)


	def match_multiline(self, text, delimiter, in_state, style):
		"""Do highlighting of multi-line strings. ``delimiter`` should be a
		``QRegExp`` for triple-single-quotes or triple-double-quotes, and
		``in_state`` should be a unique integer to represent the corresponding
		state changes when inside those strings. Returns True if we're still
		inside a multi-line string when this function is finished.
		"""
		# If inside triple-single quotes, start at 0
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		# Otherwise, look for the delimiter on this line
		else:
			start = delimiter.indexIn(text)
			# Move past this match
			add = delimiter.matchedLength()

		# As long as there's a delimiter match on this line...
		while start >= 0:
			# Look for the ending delimiter
			end = delimiter.indexIn(text, start + add)
			# Ending delimiter on this line?
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			# No; multi-line string
			else:
				self.setCurrentBlockState(in_state)
				length = text.length() - start + add
			# Apply formatting
			self.setFormat(start, length, style)
			# Look for the next match
			start = delimiter.indexIn(text, start + length)

		# Return True if still inside a multi-line string, False otherwise
		if self.currentBlockState() == in_state:
			return True
		else:
			return False


class NumberBar(QWidget):

	def __init__(self, edit):
		QWidget.__init__(self, edit)

		self.edit = edit
		self.adjustWidth(1)

		self.font = QtGui.QFont()
		self.font.setFamily("Consolas")
		self.font.setPointSize(10)

		self.setFont(self.font)

	def paintEvent(self, event):
		self.edit.numberbarPaint(self, event)
		QWidget.paintEvent(self, event)

	def adjustWidth(self, count):
		width = self.fontMetrics().width(unicode(count))
		if self.width() != width:
			self.setFixedWidth(width)

	def updateContents(self, rect, scroll):
		if scroll:
			self.scroll(0, scroll)
		else:
			# It would be nice to do
			# self.update(0, rect.y(), self.width(), rect.height())
			# But we can't because it will not remove the bold on the
			# current line if word wrap is enabled and a new block is
			# selected.
			self.update()



class Editor(QtGui.QPlainTextEdit):
	
	def __init__(self, parent=None):
		
		QtGui.QPlainTextEdit.__init__(self)
		QtGui.QFrame.__init__(self)	

		self.filename = ''

		self.font = QtGui.QFont()
		#self.font.setFamily("Faraco Hand")
		self.font.setFamily("Consolas")
		self.font.setPointSize(10)

		self.setFont(self.font)
		self.setTabStopWidth(33)

		self.setFrameShape(QtGui.QFrame.NoFrame)

		self.highlight = PythonHighlighter(self.document())

		self.cursorPositionChanged.connect(self.highlightline)

		self.setWordWrapMode(0)

		pal = QtGui.QPalette()
		# bgc = QtGui.QColor("#1E1E1E")
		# pal.setColor(QtGui.QPalette.Base, bgc)		
		textc = QtGui.QColor(40, 40, 40)
		pal.setColor(QtGui.QPalette.Text, textc)
		self.setPalette(pal)

		scrollbarStyleSheet = """
		/* HORIZONTAL */
		QScrollBar:horizontal {
			border: none;
			background: none;
			height: 8px;
		}

		QScrollBar::handle:horizontal {
			background: lightgray;
			min-width: 26px;
		}

		/* VERTICAL */
		QScrollBar:vertical {
			border: none;
			background: none;
			width: 8px;		
		}

		QScrollBar::handle:vertical {
			background: lightgray;
			min-height: 26px;
		}

		"""	
		self.setStyleSheet(scrollbarStyleSheet)


	def highlightline(self):
		hi_selection = QtGui.QTextEdit.ExtraSelection()

		hi_selection.format.setBackground(QtGui.QColor("#FFFFDA"))
		hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
		hi_selection.cursor = self.textCursor()
		hi_selection.cursor.clearSelection()

		self.setExtraSelections([hi_selection])

	def numberbarPaint(self, number_bar, event):
		font_metrics = self.fontMetrics()
		current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1

		block = self.firstVisibleBlock()
		line_count = block.blockNumber()
		painter = QPainter(number_bar)
		painter.fillRect(event.rect(), self.palette().base())

		# Iterate over all visible text blocks in the document.
		while block.isValid():
			line_count += 1
			block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

			# Check if the position of the block is out side of the visible
			# area.
			if not block.isVisible() or block_top >= event.rect().bottom():
				break

			# We want the line number for the selected line to be bold.
			if line_count == current_line:
				font = painter.font()
				# font.setBold(True)
				painter.setFont(font)
			else:
				font = painter.font()
				font.setBold(False)
				painter.setFont(font)

			# Draw the line number right justified at the position of the line.
			paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
			painter.drawText(paint_rect, Qt.AlignRight, unicode(line_count))

			block = block.next()

		painter.end()



class LNTextEdit(QtGui.QFrame):
	
	def __init__(self, *args):
		QtGui.QFrame.__init__(self, *args)		

		self.edit = Editor()
		self.pyFile = ""
		self.number_bar = NumberBar(self.edit)

		hbox = QHBoxLayout(self)
		hbox.setSpacing(10)
		hbox.setContentsMargins(10,0,0,0)
		hbox.addWidget(self.number_bar)
		hbox.addWidget(self.edit)

		self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
		self.edit.updateRequest.connect(self.number_bar.updateContents)

	def setFileName(self, name):
		self.edit.filename = name

	def getFileName(self):
		return self.edit.filename
		
	def setPyFile(self,name):
		self.pyFile = name
	
	def getPyFile(self):
		return self.pyFile


		
class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		
		# super(Main, self).__init__(parent)
		QtGui.QMainWindow.__init__(self, parent)				

		self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

		try:
			self.recentFiles = open('saved', 'r+')
		
		except IOError:
			self.recentFiles = open('saved', 'w')
			self.recentFiles.close()
			self.recentFiles = open('saved', 'r+')
		
		self.writeRecentFiles = open('saved', 'a+')
		
		try:
			self.toReadCurrentTab = open('currTab', 'r')		
		
		except IOError:
			self.toReadCurrentTab = open('saved', 'w')
			self.toReadCurrentTab.close()
			self.toReadCurrentTab = open('saved', 'r+')
			
		self.writeRecentFiles = open('saved', 'a+')		
		
		readRecentTab = self.toReadCurrentTab.read()

		self.listOfOpenTabs = []

		self.openedFiles = self.recentFiles.read().split('\n')

		if self.openedFiles[0] == '':
			self.initUI()
			self.initEditor("")
			self.initToolbar()
			self.initMenubar()														# Initialize the bars	

		else:
			self.initUI()

			counter = 0
			
			for files in self.openedFiles:
				
				if files != '':
					self.initEditor(files)

					try:					
						with open(files,"rt") as file:
							self.listOfOpenTabs[counter].edit.setPlainText(file.read())

					except:
						pass

				counter += 1

				if readRecentTab == files:
					self.tab.setCurrentWidget(self.listOfOpenTabs[-1])

			self.initToolbar()
			self.initMenubar()

	def writeRecentlyOpenedFiles(self):
		self.writeRecentFiles = open('saved', 'w')
		
		for files in self.listOfOpenTabs:
			if files.getFileName():
				self.writeRecentFiles.write(str(files.getFileName()) + '\n')
		
		self.writeRecentFiles.close()

	def writeCurrentTab(self):
		try:
			self.toWriteCurrentTab = open('currTab', 'w')
			self.toWriteCurrentTab.write(self.tab.currentWidget().getFileName())
			self.toWriteCurrentTab.close()
		except:
			pass

	def initEditor(self, files):

		a = LNTextEdit()

		a.setFileName(files)
		self.listOfOpenTabs.append(a)
		
		if files == "":
			self.tab.addTab(a, 'Untitled')
		else:
			self.tab.addTab(a, os.path.basename(files))

		a.edit.cursorPositionChanged.connect(self.cursorPosition)

	def initUI(self):

		self.tab = QtGui.QTabWidget(self)
		self.tab.setMovable(True)
		self.tab.setTabsClosable(True)
		self.setCentralWidget(self.tab)
		self.tab.tabCloseRequested.connect(self.closeTab)

		self.statusbar = self.statusBar()										# Initialize a statusbar for the window			
		
		self.setGeometry(180,100,1030,600)										# x and y coordinates on the screen, width, height
		self.setWindowTitle("Ching Chong IDE")

	def initToolbar(self):
		# self.toolbar = self.addToolBar("Options")								# Initialize the OPTIONS toolbar

		self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New File",self)
		self.newAction.setStatusTip("Create a new document from scratch.")
		self.newAction.setShortcut("Ctrl+N")
		self.newAction.triggered.connect(self.new)

		self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open File",self)
		self.openAction.setStatusTip("Open existing document")
		self.openAction.setShortcut("Ctrl+O")
		self.openAction.triggered.connect(self.open)

		self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
		self.saveAction.setStatusTip("Save document")
		self.saveAction.setShortcut("Ctrl+S")
		self.saveAction.triggered.connect(self.save)

		self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut",self)
		self.cutAction.setStatusTip("Delete and copy text to clipboard")
		self.cutAction.setShortcut("Ctrl+X")
		self.cutAction.triggered.connect(self.tab.currentWidget().edit.cut)

		self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)
		self.copyAction.setStatusTip("Copy text to clipboard")
		self.copyAction.setShortcut("Ctrl+C")
		self.copyAction.triggered.connect(self.tab.currentWidget().edit.copy)

		self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste",self)
		self.pasteAction.setStatusTip("Paste text from clipboard")
		self.pasteAction.setShortcut("Ctrl+V")
		self.pasteAction.triggered.connect(self.tab.currentWidget().edit.paste)

		self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)
		self.undoAction.setStatusTip("Undo last action")
		self.undoAction.setShortcut("Ctrl+Z")
		self.undoAction.triggered.connect(self.tab.currentWidget().edit.undo)

		self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)
		self.redoAction.setStatusTip("Redo last undone thing")
		self.redoAction.setShortcut("Ctrl+Y")
		self.redoAction.triggered.connect(self.tab.currentWidget().edit.redo)

		self.indentAction = QtGui.QAction("Indent Area",self)
		self.indentAction.setShortcut("Ctrl+Tab")
		self.indentAction.triggered.connect(self.indent)

		self.dedentAction = QtGui.QAction("Dedent Area",self)
		self.dedentAction.setShortcut("Shift+Tab")
		self.dedentAction.triggered.connect(self.dedent)

		self.findAction = QtGui.QAction("Find and replace",self)
		self.findAction.setStatusTip("Find and replace words in your document")
		self.findAction.setShortcut("Ctrl+F")
		self.findAction.triggered.connect(find.Find(self).show)

		self.buildAction = QtGui.QAction("Build", self)
		self.buildAction.setStatusTip("Compile then run the program")
		self.buildAction.setShortcut("Ctrl+B")
		self.buildAction.triggered.connect(self.build)

		self.wordWrapAction = QtGui.QAction("Word Wrap", self, checkable = True)
		self.wordWrapAction.setStatusTip("Set a word wrap.")
		self.wordWrapAction.triggered.connect(self.setWordWrap)

		self.fontSizeIndex = 6

		self.fontSizes = ['6','7','8','9','10','11','12','13','14',
			 '15','16','18','20','22','24','26','28',
			 '32','36','40','44','48','54','60','66',
			 '72','80','88','96']

		self.incFontSize = QtGui.QAction("Increment Font", self)
		self.incFontSize.setShortcut("Ctrl++")
		# self.incFontSize.triggered.connect(self.incFontSize)

		self.exitAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"), "Exit", self)
		self.exitAction.setShortcut("Ctrl+W")
		self.exitAction.triggered.connect(self.closeEvent)

	def initFormatbar(self):
		self.formatbar = self.addToolBar("Format")								# Initialize the FORMAT toolbar

	def initMenubar(self):														# Initialize the elements of the MENU bar
		menubar = self.menuBar()

		file = menubar.addMenu("File")
		edit = menubar.addMenu("Edit")
		view = menubar.addMenu("View")
		tools = menubar.addMenu("Tools")

		file.addAction(self.newAction)
		file.addAction(self.openAction)
		file.addAction(self.saveAction)

		edit.addAction(self.undoAction)
		edit.addAction(self.redoAction)
		edit.addSeparator()
		edit.addAction(self.cutAction)
		edit.addAction(self.copyAction)
		edit.addAction(self.pasteAction)
		edit.addSeparator()
		edit.addAction(self.indentAction)
		edit.addAction(self.dedentAction)
		edit.addSeparator()
		edit.addAction(self.findAction)

		view.addAction(self.wordWrapAction)

		tools.addAction(self.buildAction)

		# view.addAction(self.setFontSize)

	def something(self):
		subprocess.Popen("start chrome.exe", shell=True)

	def new(self):
		a = LNTextEdit()		
		self.listOfOpenTabs.append(a)		
		self.tab.insertTab(self.tab.currentIndex()+1, a, "Untitled")
		self.tab.setCurrentWidget(a)
		a.edit.cursorPositionChanged.connect(self.cursorPosition)
		a.edit.setFocus()

	def open(self):

		fileAlreadyOpen = False

		filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.chng)"))

		for files in self.listOfOpenTabs:
			if files.getFileName() == filename:
				self.tab.setCurrentWidget(files)
				fileAlreadyOpen = True
				break

		if filename and not fileAlreadyOpen:
			with open(filename,"r") as file:
				a = LNTextEdit()
				a.edit.setPlainText(file.read())
				self.listOfOpenTabs.append(a)
				self.tab.insertTab(self.tab.currentIndex()+1, a, os.path.basename(filename))
				
				a.setFileName(filename)
				self.tab.setCurrentWidget(a)
				a.edit.cursorPositionChanged.connect(self.cursorPosition)
				a.edit.setFocus()

		# if filename not in self.openedFiles:		
		# 	self.writeRecentlyOpenedFiles()

	def save(self):
		if not self.tab.currentWidget().getFileName():
			self.tab.currentWidget().setFileName(QtGui.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.chng)"))
			
			if self.tab.currentWidget().getFileName() != "":
				self.tab.setTabText(self.tab.currentIndex(), self.tab.currentWidget().getFileName().split('/')[-1])

				with open(self.tab.currentWidget().getFileName(), "w") as file:
					file.write(self.tab.currentWidget().edit.toPlainText())
		else:
			
			with open(self.tab.currentWidget().getFileName(), "w") as file:
				file.write(self.tab.currentWidget().edit.toPlainText())

		# if self.tab.currentWidget().getFileName() not in self.openedFiles:		
		# 	self.writeRecentlyOpenedFiles()

		self.statusbar.showMessage('Saved')

	def indent(self):
		# Grab the cursor
		cursor = self.tab.currentWidget().edit.textCursor()

		if cursor.hasSelection():
			# Store the current line/block number
			temp = cursor.blockNumber()

			# Move to the selection's last line
			cursor.setPosition(cursor.selectionEnd())

			# Calculate range of selection
			diff = cursor.blockNumber() - temp

			# Iterate over lines
			for n in range(diff + 1):
				# Move to start of each line
				cursor.movePosition(QtGui.QTextCursor.StartOfLine)

				# Insert tabbing
				cursor.insertText("\t")

				# And move back up
				cursor.movePosition(QtGui.QTextCursor.Up)

		# If there is no selection, just insert a tab
		else:
			cursor.insertText("\t")

	def dedent(self):
		cursor = self.tab.currentWidget().edit.textCursor()

		if cursor.hasSelection():
			# Store the current line/block number
			temp = cursor.blockNumber()

			# Move to the selection's last line
			cursor.setPosition(cursor.selectionEnd())

			# Calculate range of selection
			diff = cursor.blockNumber() - temp

			# Iterate over lines
			for n in range(diff + 1):
				self.handleDedent(cursor)

				# Move up
				cursor.movePosition(QtGui.QTextCursor.Up)

		else:
			self.handleDedent(cursor)


	def handleDedent(self,cursor):
		cursor.movePosition(QtGui.QTextCursor.StartOfLine)

		# Grab the current line
		line = cursor.block().text()

		# If the line starts with a tab character, delete it
		if str(line).startswith("\t"):
			# Delete next character
			cursor.deleteChar()

		# Otherwise, delete all spaces until a non-space character is met
		else:
			for char in line[:8]:

				if char != " ":
					break

				cursor.deleteChar()

	def build(self):
		splitList = os.path.basename(self.tab.currentWidget().getFileName()).split(".chng")
		pyName = splitList[0] + ".py"
		self.tab.currentWidget().setPyFile(pyName)
		runString = "python2 " + self.tab.currentWidget().getPyFile()
	
		subprocess.Popen(runString,shell = True)

	def setWordWrap(self):
		if self.wordWrapAction.isChecked():
			self.tab.currentWidget().edit.setWordWrapMode(3)
		else:
			self.tab.currentWidget().edit.setWordWrapMode(0)

	def cursorPosition(self):
		cursor = self.tab.currentWidget().edit.textCursor()

		# Mortals like 1-indexed things
		line = cursor.blockNumber() + 1
		col = cursor.columnNumber()

		self.statusbar.showMessage("Line: {}, Column: {}".format(line,col))

	def incFontSize(self, fontsize):
		self.tab.currentWidget().edit.setPointSize(int(fontsize))

	def closeTab(self):
		self.listOfOpenTabs.remove(self.tab.currentWidget())		
		self.tab.removeTab(self.tab.currentIndex())

	def unsavedChanges(self):
		pass

	def closeEvent(self, event):
		self.writeCurrentTab()
		self.writeRecentlyOpenedFiles()
		self.recentFiles.close()
		self.toReadCurrentTab.close()
		exit(1)



def main():

	app = QtGui.QApplication(sys.argv)	

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
