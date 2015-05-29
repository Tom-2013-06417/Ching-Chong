import sys, os
import subprocess

from PyQt4 import QtGui, QtCore																		# PyQt is our GUI platform, as it is more efficient and client ready
from PyQt4.QtCore import Qt, QRegExp
from PyQt4.Qt import QWidget
from PyQt4.Qt import QTextFormat
from PyQt4.Qt import QVariant
from PyQt4.Qt import QPainter
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QRect

from ext import *



def format(color, style=''):																		# Everything related to the syntax highlighter is retrieved from											
	"""Return a QTextCharFormat with the given attributes.
	"""																								# https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
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
STYLES = {																							# These are the styling tuples, slightly modifided
	'keyword': format('#2B43BA'),																	# to meet our IDE's needs (color schemes)
	'operator': format('#F51462'),
	'brace': format('#14A6F5'),
	'defclass': format('black', 'bold'),
	'mainclass': format('#2B43BA', 'bold'),
	'string': format('#87AF10'),				# Strings
	'comment': format('#777777', 'italic'),		# All comments are italicized
	'numbers': format('brown'),
	'terminator': format('green'),
	'loops': format('#FF7E00'),
	'startingline': format('#FF7E00'),			# Salutatory greetings (Hi, I am <NAME>.)
	'senderclass': format('#CD4422', 'bold'),	# Name of sender
	'defname': format('#FF7E00'),				# Function salutatory greetings
	'boolean': format('#C332CD'),				# Boolean colors are different
}



class ChingChongHighlighter (QtGui.QSyntaxHighlighter):												# Again, this code block is retrieved from https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
	"""Syntax highlighter for the Python language.
	"""																								# And is modified by adding rules and words to meet Ching Chong needs
	# Keywords
	keywords = [																					# Some one word keywords for the language	
		'and', 'again', 'ask', 'Diary', 'from', 'From', 'if', 'in', 'is', 'of', 'oclock',
		'not', 'or', 'pass', 'while', 'with', 'GWA', 'Score', 'Essay', 'Honor', 'ReportCard', 'okay', 'LetterGrade', 'Teacher', 'adds', 'to', 'gets',
		'Father', 'counts', 'entries'
	]

	boolean = ['Own', 'Disown']																		# Additional boolean words are separate, as they are of a different color

	# Operators
	operators = [																					# Operators too are of a different color; Relational operators are textual and not symbolic	
		# Comparison
		'more lesser to', 'more greaterer to', 'same to', 'not same to', 'greaterer to', 'lesser to',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*', '=',
	]

	# Braces
	braces = [																						# Braces for miscellaneous syntax
		'\{', '\}', '\(', '\)', '\[', '\]',
	]
	def __init__(self, document):
		QtGui.QSyntaxHighlighter.__init__(self, document)

		rules = []																					# Rules that are of the Regular Expression form (CS 133)

		# Keyword, operator, and brace rules
		rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in ChingChongHighlighter.keywords]
		rules += [(r'%s' % o, 0, STYLES['operator']) for o in ChingChongHighlighter.operators]		
		rules += [(r'%s' % b, 0, STYLES['brace']) for b in ChingChongHighlighter.braces]
		rules += [(r'\b%s\b' % w, 0, STYLES['boolean']) for w in ChingChongHighlighter.boolean]

		# All other rules
		rules += [
			# 'self'
			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),										# These are some of the additional rules for the 'reserved phrases' of Ching Chong					

			# 'def' followed by an identifier
			(r'\bHi, I am\b\s*(\w+)\.', 1, STYLES['senderclass']),									# The number 1 signifies that the 2nd word should be the target of the applied color
			(r'\bHi, I am\b', 0, STYLES['startingline']),											# The number 0 signifies that the first word boundaries should be the target too
			(r'Sincerely,\s*(\w+)\.', 1, STYLES['senderclass']),									# Starting and ending line
			(r'Sincerely,', 0, STYLES['startingline']),

			(r'\bDear\b', 0, STYLES['defname']),													# Salutation phrases
			(r'\bDear\b\s*(\w+)\,', 1, STYLES['defclass']),
			(r'Diary', 0, STYLES['mainclass']),														# The Diary is a reserved word

			(r'lah.', 0, STYLES['terminator']),														# Terminators
			
			(r'desu.', 0, STYLES['terminator']),													# and easter eggs
			(r'DABEST SI MAM RAE!', 0, STYLES['senderclass']),
			
			(r'I show Father', 0, STYLES['keyword']),												# Print and Read
			(r'I give Father', 0, STYLES['keyword']),

			(r'of A\+ in', 0, STYLES['keyword']),													# Reserved phrase for the list

			(r'Father wants', 0, STYLES['keyword']),												# Reserved phrase for the raw_input of python

			(r'I write to', 0, STYLES['keyword']),													# Calling a function

			(r'I get', 0, STYLES['keyword']),														# Calling a function and getting a return variable		

			(r'Father surprise quiz:', 0, STYLES['keyword']),										# Arithmetic blocks
			(r'Father surprise long quiz:', 0, STYLES['keyword']),
			
			(r'Father say make repeat', 0, STYLES['keyword']),										# Loop blocks
			(r'\bFather say make repeat\b\s*([A-Z]+)', 1, STYLES['senderclass']),

			(r'to become doctor', 0, STYLES['keyword']),											# Ending statements for function variable block
			(r'Father says that I need', 0, STYLES['keyword']),										# Starting statement for function variable block
			
			(r'Must do', 0, STYLES['keyword']),														# Additional loop blocks
			(r'\bMust do\b\s*([A-Z]+)\s*\bwhile\b', 1, STYLES['senderclass']),

			(r'Must repeat', 0, STYLES['keyword']),
			(r'\bMust repeat\b\s*([A-Z]+)\s*\bwhile\b', 1, STYLES['senderclass']),
			
			(r'I\'m done with', 0, STYLES['keyword']),												# End of the loop block
			(r'\bI\'m done with\b\s*([A-Z]+)', 1, STYLES['senderclass']),
			
			(r'Father ask', 0, STYLES['keyword']),													# The if statement
			(r'\bFather ask\b\s*([A-Z]+)', 1, STYLES['senderclass']),

			(r'Father ask again', 0, STYLES['keyword']),											# The else if statement
			(r'\bFather ask again\b\s*([A-Z]+)', 1, STYLES['senderclass']),

			(r'Father stop asking', 0, STYLES['keyword']),											# The else statement
			(r'\bFather stop asking\b\s*([A-Z]+)', 1, STYLES['senderclass']),

			(r'I double confirm', 0, STYLES['keyword']),											# The ending line of the if and else if statements
			(r'\bI double confirm\b\s*([A-Z]+)', 1, STYLES['senderclass']),		
			
			(r'Father ashamed of son for not answer', 0, STYLES['keyword']),						# The ending line of the else statement
			(r'\bFather ashamed of son for not answer\b\s*([A-Z]+)', 1, STYLES['senderclass']),
			
			(r'I want dumplings and', 0, STYLES['keyword']),										# Line for acception function parameters
			(r'I send shrimp fried rice to all:', 0, STYLES['keyword']),							# Line for instantiating global variables (the main)
			(r'I did not know', 0, STYLES['keyword']),												# End statement for arithmetic block
			(r'I give you sum', 0, STYLES['keyword']),												# Return statement of functions
			
			(r'I am tired', 0, STYLES['keyword']),					 								# Break
			(r'Father brought out belt', 0, STYLES['keyword']),										# Continue
			

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


class NumberBar(QWidget):																			# Code block retrieved from https://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/

	def __init__(self, edit):																		# This code block adds a number bar to the GUI
		QWidget.__init__(self, edit)

		self.edit = edit
		self.adjustWidth(1)

		self.font = QtGui.QFont()																	# Set the font to Consolas 10
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

			self.update()



class Editor(QtGui.QPlainTextEdit):																	# The overrided class of the PLain Text Editor given by PyQt
	
	def __init__(self, parent=None):
		
		QtGui.QPlainTextEdit.__init__(self)
		QtGui.QFrame.__init__(self)	

		self.filename = ''																			# For every editor, maintain a string called the filename

		self.textChanged.connect(self.changed)														# For times that the document is modified / changed, connect to the self.changed 

		self.font = QtGui.QFont()																	# Set default fonts to Consolas 10
		self.font.setFamily("Consolas")
		self.font.setPointSize(10)

		self.fontSizeIndex = 2										 								# From the list of fonts, defaul size is located at index 2

		self.setFont(self.font)
		self.setTabStopWidth(33)																	# Set tab width to 33 (four spaces)

		self.setFrameShape(QtGui.QFrame.NoFrame)													# Remove the border of the frame

		self.highlight = ChingChongHighlighter(self.document())										# Instantiate the Ching Chong Syntax highlighter

		self.cursorPositionChanged.connect(self.highlightline)										# Every time the cursor position changes, change the hightlight line's postion

		self.setWordWrapMode(0)																		# There is initially no wordwrapping

		pal = QtGui.QPalette()																		# Set the colors of the default foreground text
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
		self.setStyleSheet(scrollbarStyleSheet)														# Change the style of the scrollbar (Make it look thinner; remove the arrows)
		self.changesSaved = True

	def highlightline(self):																		# Method to highlight the current line
		hi_selection = QtGui.QTextEdit.ExtraSelection()

		hi_selection.format.setBackground(QtGui.QColor("#FFFFDA"))
		hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
		hi_selection.cursor = self.textCursor()
		hi_selection.cursor.clearSelection()

		self.setExtraSelections([hi_selection])

	def removeHightlightline(self):																	# A fork of the above method to remove the current line
		hi_selection = QtGui.QTextEdit.ExtraSelection()

		hi_selection.format.setBackground(QtGui.QColor("#FFFFFF"))
		hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
		hi_selection.cursor = self.textCursor()
		hi_selection.cursor.clearSelection()

		self.setExtraSelections([hi_selection])

	def numberbarPaint(self, number_bar, event):													# Combines data from the text editor to the numberbar so that the numberbar may have numbers
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
				font.setBold(True)
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

	def changed(self):
		self.changesSaved = False



class LNTextEdit(QtGui.QFrame):																		# A facade class that combindes the numberbar and texteditor into one class (easy)
	
	def __init__(self, *args):
		QtGui.QFrame.__init__(self, *args)		

		self.edit = Editor()
		self.pyFile = ""
		self.number_bar = NumberBar(self.edit)

		hbox = QHBoxLayout(self)																	# Pack the number bar, then pack the editor
		hbox.setSpacing(10)
		hbox.setContentsMargins(10,0,0,0)
		hbox.addWidget(self.number_bar)
		hbox.addWidget(self.edit)

		self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
		self.edit.updateRequest.connect(self.number_bar.updateContents)

	def setFileName(self, name):																	# set file name for the class
		self.edit.filename = name

	def getFileName(self):																			# Wrapper functions for getting and setting the filename of editor class
		return self.edit.filename
		
	def setPyFile(self,name):																		# Set the filename of the translated ching chong file
		self.pyFile = name
	
	def getPyFile(self):
		return self.pyFile


		
class Main(QtGui.QMainWindow):																		# The Facade of interfaces that combines everything (Retrieved from https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143)

	def __init__(self, parent = None):																# Of course, the whole class is modified (added more functions) so that it meets the needs of the IDE
		
		# super(Main, self).__init__(parent)
		QtGui.QMainWindow.__init__(self, parent)				

		self.setWindowIcon(QtGui.QIcon("icons/icon.png"))											# Set the Ching Chong icon -_-

		try:																						# Try opening the recentFiles file and the writeRecentFiles file
			self.recentFiles = open('saved', 'r+')
		
		except IOError:																				# If it doesn't exist, create a new file instead
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
		
		readRecentTab = self.toReadCurrentTab.read()												# Set the current tab as the recently active tab

		self.listOfOpenTabs = []																	# Instantiate the reference list of editor objects

		self.openedFiles = self.recentFiles.read().split('\n')										# Reopen the recently open tabs to the editor

		if self.openedFiles[0] == '':																# If the list of opened files is empty, then just instantiate an empty unsaved editor
			self.initUI()
			self.initEditor("")
			self.initToolbar()
			self.initMenubar()																		# Initialize the bars	

		else:
			self.initUI()																			# Else if it isn't empty, then immediately,

			counter = 0
			
			for files in self.openedFiles:															# Open an editor per file, then copy the contents of the file to the editor screen
				
				if files != '':
					self.initEditor(files)

					try:					
						with open(files,"rt") as file:
							self.listOfOpenTabs[counter].edit.setPlainText(file.read())
							self.listOfOpenTabs[counter].edit.changesSaved = True

					except:
						pass

				counter += 1

				if readRecentTab == files:															# If one of the tabs is the recently used tab, then set focus to it
					self.tab.setCurrentWidget(self.listOfOpenTabs[-1])

			self.initToolbar()																		# Initialize the rest of the interface (Statusbar, Menus, Actions)
			self.initMenubar()
			self.readPreferences()																	# Read from a file containing boolean values (Toggles status bar, word wrap, and highlight line on or off)

	def writeRecentlyOpenedFiles(self):																# Function to be called as the program exits
		self.writeRecentFiles = open('saved', 'w')
		
		for files in self.listOfOpenTabs:															# For every open tab in the program, list down their filenames, then write them down in a file
			if files.getFileName():
				self.writeRecentFiles.write(str(files.getFileName()) + '\n')
		
		self.writeRecentFiles.close()

	def writeCurrentTab(self):																		# As the program exits, write the recently active tab to a file
		try:
			self.toWriteCurrentTab = open('currTab', 'w')
			self.toWriteCurrentTab.write(self.tab.currentWidget().getFileName())
			self.toWriteCurrentTab.close()
		except:
			pass

	def writePreferences(self):																		# As the program exits too, write the current preferences of the View menu (If on or off of some commands)
		temp = open('preferences', 'w')
		
		temp.write(str(self.showStatusBarAction.isChecked())+'\n')
		temp.write(str(self.wordWrapAction.isChecked())+'\n')
		temp.write(str(self.showHighlightlineAction.isChecked())+'\n')

		temp.close()

	def readPreferences(self):																		# Sets the recently modified preference values to On of Off (Read from the database file, then set values to true or false)
		try:
			temp = open('preferences', 'r+')
			
			if temp.readline().rstrip() == "True":													# Status bar Mode: If true, show the status bar
				self.statusbar.show()
				self.showStatusBarAction.setChecked(True)
			else:																					# Else, hide the status bar
				self.statusbar.hide()
				self.showStatusBarAction.setChecked(False)

			if temp.readline().rstrip() == "True":													# Word wrap mode; if True, enable word wrap. Else, do not.
				for tab in self.listOfOpenTabs:
					tab.edit.setWordWrapMode(3)
				self.wordWrapAction.setChecked(True)
			else:
				for tab in self.listOfOpenTabs:
					tab.edit.setWordWrapMode(0)
				self.wordWrapAction.setChecked(False)

			if temp.readline().rstrip() == "False":													# Toggle highlight word; if True, enable highlight line; else, do not
				for tab in self.listOfOpenTabs:
					tab.edit.cursorPositionChanged.connect(tab.edit.removeHightlightline)				
					tab.edit.removeHightlightline()
				self.showHighlightlineAction.setChecked(False)
			else:
				for tab in self.listOfOpenTabs:	
					tab.edit.cursorPositionChanged.connect(tab.edit.highlightline)				
					tab.edit.highlightline()
				self.showHighlightlineAction.setChecked(True)

			temp.close()

		except Exception, e:
			print e

	def initEditor(self, files):																	# The method that actually instantiates the Editor object

		a = LNTextEdit()

		a.setFileName(files)																		# It accepts the name of the open files, for it to be opened AND renamed as the tab title
		self.listOfOpenTabs.append(a)
		
		if files == "":
			self.tab.addTab(a, 'Untitled')
		else:
			self.tab.addTab(a, os.path.basename(files))

		a.edit.cursorPositionChanged.connect(self.cursorPosition)									# Every time the program is instantiated, connect the cursor to the status bar widget display for column / line number information

	def initUI(self):																				# The initial method from the retrieved online link.																

		self.tab = QtGui.QTabWidget(self)															# It only adds the tab widget and sets necessary preferences, such as set movable tabs
		self.tab.setMovable(True)
		self.tab.setTabsClosable(True)
		self.setCentralWidget(self.tab)																# Set the tab widget as the center of the interface
		self.tab.tabCloseRequested.connect(self.closeTab)

		self.statusbar = self.statusBar()															# Initialize a statusbar for the window			
		
		self.setGeometry(180,100,1030,600)															# x and y coordinates on the screen, width, height
		self.setWindowTitle("Ching Chong IDE")														# The title name to be displayed (CHING CHONG IDE)

	def initToolbar(self):																			# The actions to be initialized (in the original online reference, the author included icons in the toolbar)																		

		self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New File",self)				# Because this project intends to be minimalist, toolbars are omitted
		self.newAction.setStatusTip("Create a new document from scratch.")							# Set the New action
		self.newAction.setShortcut("Ctrl+N")
		self.newAction.triggered.connect(self.new)

		self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open File",self)				# Set the Open action
		self.openAction.setStatusTip("Open existing document")
		self.openAction.setShortcut("Ctrl+O")
		self.openAction.triggered.connect(self.open)

		self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)					# Set the Save action
		self.saveAction.setStatusTip("Save document")
		self.saveAction.setShortcut("Ctrl+S")
		self.saveAction.triggered.connect(self.save)

		self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut",self)						# Set the Cut action
		self.cutAction.setStatusTip("Delete and copy text to clipboard")
		self.cutAction.setShortcut("Ctrl+X")
		self.cutAction.triggered.connect(self.tab.currentWidget().edit.cut)

		self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)					# Set the Copy action
		self.copyAction.setStatusTip("Copy text to clipboard")
		self.copyAction.setShortcut("Ctrl+C")
		self.copyAction.triggered.connect(self.tab.currentWidget().edit.copy)

		self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste",self)				# Set the Paste action
		self.pasteAction.setStatusTip("Paste text from clipboard")
		self.pasteAction.setShortcut("Ctrl+V")
		self.pasteAction.triggered.connect(self.tab.currentWidget().edit.paste)

		self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)					# Set the Undo action
		self.undoAction.setStatusTip("Undo last action")
		self.undoAction.setShortcut("Ctrl+Z")
		self.undoAction.triggered.connect(self.tab.currentWidget().edit.undo)

		self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)					# Set the Redo function
		self.redoAction.setStatusTip("Redo last undone thing")
		self.redoAction.setShortcut("Ctrl+Y")
		self.redoAction.triggered.connect(self.tab.currentWidget().edit.redo)

		self.indentAction = QtGui.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)		# Indent area function
		self.indentAction.setShortcut("Ctrl+Tab")
		self.indentAction.triggered.connect(self.indent)

		self.dedentAction = QtGui.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)		# Dedent area function
		self.dedentAction.setShortcut("Shift+Tab")
		self.dedentAction.triggered.connect(self.dedent)

		self.findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"),"Find and Replace",self)		# Find and replace function
		self.findAction.setStatusTip("Find and replace words in your document")
		self.findAction.setShortcut("Ctrl+F")
		self.findAction.triggered.connect(find.Find(self).show)

		self.buildAction = QtGui.QAction(QtGui.QIcon("icons/build.png"),"Build", self)				# Build action (parse, interpret, then run)
		self.buildAction.setStatusTip("Compile then run the program")
		self.buildAction.setShortcut("Ctrl+B")
		self.buildAction.triggered.connect(self.build)

		self.wordWrapAction = QtGui.QAction("Word Wrap", self, checkable = True)					# View action to set word wrap mode
		self.wordWrapAction.setStatusTip("Set a word wrap")
		self.wordWrapAction.triggered.connect(self.setWordWrap)

		self.showStatusBarAction = QtGui.QAction("Status Bar", self, checkable = True)				# View action to toggle status bar
		self.showStatusBarAction.setStatusTip("Show or hide the status bar")
		self.showStatusBarAction.triggered.connect(self.displayStatusBar)
		self.showStatusBarAction.setChecked(True)

		self.showHighlightlineAction = QtGui.QAction("Highlight Current Line", self, checkable = True)	# View action to toggle highlight line
		self.showHighlightlineAction.setStatusTip("Show or hide the highlight line")
		self.showHighlightlineAction.triggered.connect(self.toggleHighlightLine)
		self.showHighlightlineAction.setChecked(True)

		self.incFontSizeAction = QtGui.QAction("Increment Font Size", self)							# View action to increase font size
		self.incFontSizeAction.setShortcut("Ctrl+=")
		self.incFontSizeAction.triggered.connect(self.incFontSize)

		self.decFontSizeAction = QtGui.QAction("Decrement Font Size", self)							# View action to decrease font size
		self.decFontSizeAction.setShortcut("Ctrl+-")
		self.decFontSizeAction.triggered.connect(self.decFontSize)

		self.exitAction = QtGui.QAction("Exit", self)												# Exit the program
		self.exitAction.setShortcut("Ctrl+W")
		self.exitAction.triggered.connect(self.closeEvent)

		self.fontSizes = [8,9,10,11,12,13,14,														# Set the allowed font sizes for this program
			 15,16,18,20,22,24,26,28,
			 32,36,40,44,48,54,60,66,
			 72,80,88,96]

	def initMenubar(self):																			# Initialize the elements of the MENU bar
		menubar = self.menuBar()

		file = menubar.addMenu("File")																# Add the menus to the bar
		edit = menubar.addMenu("Edit")
		view = menubar.addMenu("View")
		tools = menubar.addMenu("Tools")

		file.addAction(self.newAction)																# Add the actions per menu + separators
		file.addAction(self.openAction)
		file.addAction(self.saveAction)
		file.addAction(self.exitAction)

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

		view.addAction(self.showStatusBarAction)
		view.addSeparator()
		view.addAction(self.wordWrapAction)
		view.addAction(self.showHighlightlineAction)
		view.addSeparator()
		view.addAction(self.incFontSizeAction)
		view.addAction(self.decFontSizeAction)

		tools.addAction(self.buildAction)

	def something(self):																			# Start a random terminal (easter egg)
		subprocess.Popen("start", shell=True)

	def new(self):																					# The New action: Create a new instance of an editor
		a = LNTextEdit()			
		self.tab.insertTab(self.tab.currentIndex()+1, a, "Untitled.chng")							# Insert the new tab right after the current tab, then set the name to "Untitled.chng"
		self.tab.setCurrentWidget(a)																# Set focus to the tab
		a.edit.cursorPositionChanged.connect(self.cursorPosition)									# Connect necessary events
		a.edit.setFocus()		
		self.listOfOpenTabs.append(a)																# Do not forget to add that new tab to the list of open tabs

	def open(self):																					# The Open action
		fileAlreadyOpen = False																		# Set a lock

		filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.chng)"))		# Open the dialog box 

		for files in self.listOfOpenTabs:															# If the opened file from the dialog box is already an active tab in the program, then just set focus to that active tab instead
			if files.getFileName() == filename:
				self.tab.setCurrentWidget(files)
				fileAlreadyOpen = True
				break

		if filename and not fileAlreadyOpen:														# Else if it isn't open
			with open(filename,"r") as file:														# Then instantiate a new editor ojbect
				a = LNTextEdit()
				a.edit.setPlainText(file.read())													# Copy the contents of that file into the editor screen
				a.edit.changesSaved = True 															# Set saved changes to true (it is a fact)
				self.listOfOpenTabs.append(a)
				self.tab.insertTab(self.tab.currentIndex()+1, a, os.path.basename(filename))		# Append the tab object to list of tabs then set the tab title to be the filename
				
				a.setFileName(filename)																# Set that object's name as the filename, then connect necessary functions, then set focus to it.
				self.tab.setCurrentWidget(a)
				a.edit.cursorPositionChanged.connect(self.cursorPosition)
				a.edit.setFocus()

		# if filename not in self.openedFiles:		
		# 	self.writeRecentlyOpenedFiles()

	def save(self):																					# The Save action
		if not self.tab.currentWidget().getFileName():												# If the file is new (not yet saved to a directory),
			self.tab.currentWidget().setFileName(QtGui.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.chng)"))		#Open a dialog box
			
			if self.tab.currentWidget().getFileName() != "":										# If the save dialog box wasn't canceled, 
				self.tab.setTabText(self.tab.currentIndex(), self.tab.currentWidget().getFileName().split('/')[-1])

				with open(self.tab.currentWidget().getFileName(), "w") as file:						# Then write to the file
					file.write(self.tab.currentWidget().edit.toPlainText())

				self.tab.currentWidget().edit.changesSaved = True									# Then it is saved as well
		
		else:																						# Else if the file exists already in a directory
			with open(self.tab.currentWidget().getFileName(), "w") as file:
				file.write(self.tab.currentWidget().edit.toPlainText())								# Just overwrite the original file, then set the savedChanges boolean to True
				self.tab.currentWidget().edit.changesSaved = True

		self.statusbar.showMessage('Saved')															# Send a message to the task bar.	

	def indent(self):																				# The Indent function (retrieved from https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143)
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
			for n in xrange(diff + 1):
				# Move to start of each line
				cursor.movePosition(QtGui.QTextCursor.StartOfLine)

				# Insert tabbing
				cursor.insertText("\t")

				# And move back up
				cursor.movePosition(QtGui.QTextCursor.Up)

		# If there is no selection, just insert a tab
		else:
			cursor.insertText("\t")

	def dedent(self):																				# The Dedent function from the same source https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143						
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

	def handleDedent(self,cursor):																	# A part of this resource: https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143
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

	def build(self):																				# Connects from the interpreter classes. Executes the function
		self.save()
		splitList = os.path.basename(self.tab.currentWidget().getFileName()).split(".chng")
		pyName = splitList[0] + ".py"
		self.tab.currentWidget().setPyFile(pyName)
		runString = "python " + self.tab.currentWidget().getPyFile()
	
		subprocess.Popen(runString, shell = True)

	def setWordWrap(self):																			# Sets the word wrap mode
		if self.wordWrapAction.isChecked():															# If checkbox is checked, then set the wordwrap
			for tab in self.listOfOpenTabs:
				tab.edit.setWordWrapMode(3)
		else:																						# Else do not show word wrap
			for tab in self.listOfOpenTabs:
				tab.edit.setWordWrapMode(0)

	def displayStatusBar(self):																		# Same function pattern as above. Set true if false; else true
		if not self.showStatusBarAction.isChecked():
			self.statusbar.hide()
		else:
			self.statusbar.show()

	def toggleHighlightLine(self):																	# Same function as above too.
		if not self.showHighlightlineAction.isChecked():
			for tab in self.listOfOpenTabs:
				tab.edit.cursorPositionChanged.connect(tab.edit.removeHightlightline)				
				tab.edit.removeHightlightline()

		else:
			for tab in self.listOfOpenTabs:	
				tab.edit.cursorPositionChanged.connect(tab.edit.highlightline)				
				tab.edit.highlightline()

	def cursorPosition(self):																		# From the resource https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143. 
		cursor = self.tab.currentWidget().edit.textCursor()											# After every cursor move, change message, then update to the status bar

		# Mortals like 1-indexed things
		line = cursor.blockNumber() + 1
		col = cursor.columnNumber()

		self.statusbar.showMessage("Line: {}, Column: {}".format(line,col))

	def incFontSize(self):																			# Increment the font size action

		if self.tab.currentWidget().edit.fontSizeIndex > 29:
			self.tab.currentWidget().edit.fontSizeIndex = 28										# Makes sure that it doesn't go overboard the list of allowed font sizes

		self.tab.currentWidget().edit.fontSizeIndex += 1			

		try:
			self.tab.currentWidget().edit.font.setPointSize(self.fontSizes[self.tab.currentWidget().edit.fontSizeIndex])			
		except IndexError:
			pass

		self.tab.currentWidget().edit.setFont(self.tab.currentWidget().edit.font)

	def decFontSize(self):																			# Decrement the font size action (same as above function but opposite)

		if self.tab.currentWidget().edit.fontSizeIndex == 0:
			self.tab.currentWidget().edit.fontSizeIndex = 1

		self.tab.currentWidget().edit.fontSizeIndex -= 1

		try:
			self.tab.currentWidget().edit.font.setPointSize(self.fontSizes[self.tab.currentWidget().edit.fontSizeIndex])
		except IndexError:
			pass				

		self.tab.currentWidget().edit.setFont(self.tab.currentWidget().edit.font)

	def closeTab(self):																				# Close only one tab. Check if it is saved. If yes, proceed to close the tab.
		if self.tab.currentWidget().edit.changesSaved == False:										# Else no, output a dialog box (from the same resource too https://www.binpress.com/tutorial/building-a-text-editor-with-pyqt-part-one/143)
			popup = QtGui.QMessageBox(self)															# If user ignores the dialog box, do nothing
			popup.setIcon(QtGui.QMessageBox.Warning)
			popup.setWindowTitle("Ching Chong Warning")

			if self.tab.currentWidget().getFileName() != '':
				popup.setText("%s isn't saved lah." % (os.path.basename(self.tab.currentWidget().getFileName())))
			else:
				popup.setText("Untitled.chng isn't saved lah.")

			popup.setInformativeText("Do you want save?")
			popup.setStandardButtons(QtGui.QMessageBox.Save|QtGui.QMessageBox.Cancel|QtGui.QMessageBox.Discard)
			popup.setDefaultButton(QtGui.QMessageBox.Save)
			answer = popup.exec_()

			if answer == QtGui.QMessageBox.Save:
				self.save()
				if self.tab.currentWidget().getFileName() != "":
					self.listOfOpenTabs.remove(self.tab.currentWidget())
					self.tab.removeTab(self.tab.currentIndex())

			elif answer == QtGui.QMessageBox.Discard:
				self.listOfOpenTabs.remove(self.tab.currentWidget())		
				self.tab.removeTab(self.tab.currentIndex())	

		else:
			self.listOfOpenTabs.remove(self.tab.currentWidget())
			self.tab.removeTab(self.tab.currentIndex())


	def closeEvent(self, event):																	# Close the program itself (overridden function event)
		checker = True

		for tab in self.listOfOpenTabs:																# Check for every open tab.
			
			if tab.edit.changesSaved == False:														# If it is saved, do nothing. Else, confirm first if user wants to save.
				popup = QtGui.QMessageBox(self)
				popup.setIcon(QtGui.QMessageBox.Warning)
				popup.setWindowTitle("Ching Chong Warning")

				if tab.getFileName() != '':
					popup.setText("%s isn't saved lah." % (os.path.basename(tab.getFileName())))
				else:
					popup.setText("Untitled.chng isn't saved lah.")
				
				popup.setInformativeText("Do you want save?")
				popup.setStandardButtons(QtGui.QMessageBox.Save|QtGui.QMessageBox.Cancel|QtGui.QMessageBox.Discard)
				popup.setDefaultButton(QtGui.QMessageBox.Save)
				answer = popup.exec_()

				if answer == QtGui.QMessageBox.Save:
					self.save()
					if tab.getFileName() == '':
						try:
							event.ignore()
						except:
							pass

						checker = False
				
				elif answer == QtGui.QMessageBox.Discard:
					pass

				else:																				# If user does not want to save, then ignore changes (but allows access for next open)
					try:
						event.ignore()
					except:
						pass

					checker = False
					break

		if checker == True:																			# After everything else has been processed,
			self.writePreferences()																	# Write the current preferences.
			self.writeCurrentTab()																	# Write the current tab
			self.writeRecentlyOpenedFiles()															# Write the recently opened tabs
			self.recentFiles.close()																# Close the corresponding file pointers
			self.toReadCurrentTab.close()
			exit(1)																					# Then exit gracefully.



def main():																							# Main function

	app = QtGui.QApplication(sys.argv)																# Instantiate the interface in the main

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":																			# Run the main.
	main()
