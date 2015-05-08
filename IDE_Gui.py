import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QRegExp



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
	'keyword': format('blue'),
	'operator': format('red'),
	'brace': format('darkGray'),
	'defclass': format('black', 'bold'),
	'string': format('#A8CD3A'),
	'string2': format('#A8CD3A'), #Comments
	'comment': format('gray'),
	'self': format('black', 'italic'),
	'numbers': format('brown'),
	'terminator': format('green'),
	'loops': format('orange'),
	'startingline': format('orange'),
	'senderclass': format('red', 'bold')
}



class PythonHighlighter (QtGui.QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	keywords = [
		'and', 'assert', 'break', 'class', 'continue', 'Homework', 'Finish homework',
		'del', 'Diary', 'Else if', 'Else', 'except', 'exec', 'finally',
		'for', 'from', 'From', 'global', 'Get me', 'get me', 'If', 'import', 'in', 
		'lambda', 'not', 'or', 'pass', 'Showme',
		'raise', 'return', 'then', 'try', 'while', 'with', 'yield',
		'None', 'own', 'disown',
	]

	# Python operators
	operators = [
		'is',
		# Comparison
		'!=', '<', '<=', '>', '>=',
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
			(r'\bDear\b', 0, STYLES['keyword']),
			(r'\bDear\b\s*(\w+)\,', 1, STYLES['defclass']),

			# From '#' until a newline
			(r'-.-[^\n]*', 0, STYLES['comment']),
			(r'lah.', 0, STYLES['terminator']),
			(r'Do your chores', 0, STYLES['loops']),
			(r'End chores', 0, STYLES['loops']),

			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
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



class Editor(QtGui.QPlainTextEdit):
	
	def __init__(self, parent=None):

		super(Editor, self).__init__(parent)
		QtGui.QPlainTextEdit.__init__(self)

		self.filename = ''

		self.font = QtGui.QFont()
		self.font.setFamily("Consolas")
		self.font.setPointSize(10.5)

		self.setFont(self.font)
		self.setTabStopWidth(33)

		self.setFrameShape(QtGui.QFrame.NoFrame)

		self.highlight = PythonHighlighter(self.document())

	def setFileName(self, name):
		self.filename = name

	def getFileName(self):
		return self.filename


		
class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		
		# super(Main, self).__init__(parent)
		QtGui.QMainWindow.__init__(self, parent)				

		self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

<<<<<<< HEAD
		try:			
			self.readRecentFiles = open('saved', 'r+')			
			
			self.readCurrentTab = open('currTab', 'r+')	

		except IOError:
			self.writeRecentFiles = open('saved', 'w')
			self.readCurrentTab = open('currTab', 'w')

		readRecentTab = self.readCurrentTab.read()
=======
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
>>>>>>> f7aa6b05d14844c73b34e5c4357f228d6d200fb7

		self.listOfOpenTabs = []

		self.openedFiles = self.readRecentFiles.read().split('\n')

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
							self.listOfOpenTabs[counter].setPlainText(file.read())

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
		a = Editor()
		a.setFileName(files)
		self.listOfOpenTabs.append(a)
		
		if files == "":
			self.tab.addTab(a, 'Untitled')
		else:
			self.tab.addTab(a, os.path.basename(files))

		a.cursorPositionChanged.connect(self.cursorPosition)

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
		self.cutAction.triggered.connect(self.tab.currentWidget().cut)

		self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)
		self.copyAction.setStatusTip("Copy text to clipboard")
		self.copyAction.setShortcut("Ctrl+C")
		self.copyAction.triggered.connect(self.tab.currentWidget().copy)

		self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste",self)
		self.pasteAction.setStatusTip("Paste text from clipboard")
		self.pasteAction.setShortcut("Ctrl+V")
		self.pasteAction.triggered.connect(self.tab.currentWidget().paste)

		self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)
		self.undoAction.setStatusTip("Undo last action")
		self.undoAction.setShortcut("Ctrl+Z")
		self.undoAction.triggered.connect(self.tab.currentWidget().undo)

		self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)
		self.redoAction.setStatusTip("Redo last undone thing")
		self.redoAction.setShortcut("Ctrl+Y")
		self.redoAction.triggered.connect(self.tab.currentWidget().redo)

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

		# view.addAction(self.setFontSize)

	def new(self):
		a = Editor()		
		self.listOfOpenTabs.append(a)		
		self.tab.insertTab(self.tab.currentIndex()+1, a, "Untitled")
		self.tab.setCurrentWidget(a)
		a.cursorPositionChanged.connect(self.cursorPosition)
		a.setFocus()

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
				a = Editor()
				a.setPlainText(file.read())
				self.listOfOpenTabs.append(a)
				self.tab.insertTab(self.tab.currentIndex()+1, a, os.path.basename(filename))
				
				a.filename = filename
				self.tab.setCurrentWidget(a)
				a.cursorPositionChanged.connect(self.cursorPosition)
				a.setFocus()

		# if filename not in self.openedFiles:		
		# 	self.writeRecentlyOpenedFiles()

	def save(self):
		if not self.tab.currentWidget().getFileName():
			self.tab.currentWidget().setFileName(QtGui.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.chng)"))
			
			if self.tab.currentWidget().getFileName() != "":
				self.tab.setTabText(self.tab.currentIndex(), self.tab.currentWidget().getFileName().split('/')[-1])

				with open(self.tab.currentWidget().getFileName(), "w") as file:
					file.write(self.tab.currentWidget().toPlainText())
		else:
			
			with open(self.tab.currentWidget().getFileName(), "w") as file:
				file.write(self.tab.currentWidget().toPlainText())

		# if self.tab.currentWidget().getFileName() not in self.openedFiles:		
		# 	self.writeRecentlyOpenedFiles()

		self.statusbar.showMessage('Saved')

	def cursorPosition(self):
		cursor = self.tab.currentWidget().textCursor()

		# Mortals like 1-indexed things
		line = cursor.blockNumber() + 1
		col = cursor.columnNumber()

		self.statusbar.showMessage("Line: {}, Column: {}".format(line,col))

	def incFontSize(self, fontsize):
		self.tab.currentWidget().setPointSize(int(fontsize))

	def closeTab(self):
		print self.tab.current
		self.listOfOpenTabs.remove(self.tab.currentWidget())		
		self.tab.removeTab(self.tab.currentIndex())

	def unsavedChanges(self):
		pass

	def closeEvent(self, event):
		self.writeCurrentTab()
		self.writeRecentlyOpenedFiles()
		self.readRecentFiles.close()
		self.readCurrentTab.close()
		exit(1)



def main():

	app = QtGui.QApplication(sys.argv)	

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
