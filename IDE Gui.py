import sys
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
	'string': format('magenta'),
	'string2': format('gray'),
	'comment': format('gray'),
	'self': format('black', 'italic'),
	'numbers': format('brown'),
}



class PythonHighlighter (QtGui.QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	keywords = [
		'and', 'assert', 'break', 'class', 'continue', 'Homework', 'Finish homework',
		'del', 'Else if', 'Else', 'except', 'exec', 'finally',
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
		# self.tri_double = (QRegExp('-_-'), 2, STYLES['string2'])

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
			# Single-quoted string, possibly containing escape sequences
			(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

			# 'def' followed by an identifier
			(r'\bHomework\b\s*(\w+)', 1, STYLES['defclass']),
			# 'class' followed by an identifier
			(r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

			# From '#' until a newline
			(r'-.-[^\n]*', 0, STYLES['comment']),

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



class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self,parent)				

		self.setWindowIcon(QtGui.QIcon("icons/icon.png"))		

		self.font = QtGui.QFont()
		self.font.setFamily("Consolas")
		self.font.setPointSize(10.5)
		
		self.initUI()

		self.recentFile = open('saved.txt', 'r')
		self.recentFile2 = open('saved.txt', 'a')

		self.openedFiles = self.recentFile.read().split('\n')

		try:
			self.filename = self.openedFiles[-2].rstrip()
		
			if self.filename != '':
				with open(self.filename,"rt") as file:
					self.text.setPlainText(file.read())

			else:
				self.filename = ''	

		except:
			self.filename = ''
			if self.filename != '':
				self.openedFiles.remove(self.filename)

		self.highlight = PythonHighlighter(self.text.document())
		self.text.show()

	def recentlyOpened(self):

		self.recentFile2.write(str(self.filename) + '\n')

	def initUI(self):
		self.text = QtGui.QPlainTextEdit(self)									# Initialize the TEXTBOX EDITOR
		self.setCentralWidget(self.text)										# Set it as the central widget
		self.text.setFont(self.font)
		self.text.setTabStopWidth(33)

		self.text.cursorPositionChanged.connect(self.cursorPosition)

		self.initToolbar()														# Initialize the bars
		self.initMenubar()
		
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
		self.cutAction.triggered.connect(self.text.cut)

		self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)
		self.copyAction.setStatusTip("Copy text to clipboard")
		self.copyAction.setShortcut("Ctrl+C")
		self.copyAction.triggered.connect(self.text.copy)

		self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste",self)
		self.pasteAction.setStatusTip("Paste text from clipboard")
		self.pasteAction.setShortcut("Ctrl+V")
		self.pasteAction.triggered.connect(self.text.paste)

		self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)
		self.undoAction.setStatusTip("Undo last action")
		self.undoAction.setShortcut("Ctrl+Z")
		self.undoAction.triggered.connect(self.text.undo)

		self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)
		self.redoAction.setStatusTip("Redo last undone thing")
		self.redoAction.setShortcut("Ctrl+Y")
		self.redoAction.triggered.connect(self.text.redo)

		self.exitAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"), "Exit", self)
		self.exitAction.setShortcut("Ctrl+W")
		self.exitAction.triggered.connect(self.exit)

		# self.toolbar.addAction(self.newAction)
		# self.toolbar.addAction(self.openAction)

		# self.addToolBarBreak()												# Makes the next toolbar appear underneath this one

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

	def new(self):
		spawn = Main(self)
		spawn.show()
		spawn.filename = ''
		spawn.text.setPlainText('')

	def open(self):

		# Get filename and show only .writer files
		self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.chng)"))

		if self.filename:
			with open(self.filename,"rt") as file:
				self.text.setPlainText(file.read())

		if self.filename not in self.openedFiles:		
			self.recentlyOpened()	

	def save(self):
		self.statusbar.showMessage('Saved')

		if not self.filename:
			self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.chng)")

		# if not self.filename.endswith(".chng"):
			# self.filename += ".chng"

		with open(self.filename,"wt") as file:
			file.write(self.text.toPlainText())	

		if self.filename not in self.openedFiles:		
			self.recentlyOpened()		

	def cursorPosition(self):
		cursor = self.text.textCursor()

		# Mortals like 1-indexed things
		line = cursor.blockNumber() + 1
		col = cursor.columnNumber()

		self.statusbar.showMessage("Line: {}, Column: {}".format(line,col))

	def exit(self):
		exit(1)



def main():

	app = QtGui.QApplication(sys.argv)

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
