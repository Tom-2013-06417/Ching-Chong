import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt



class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self,parent)

		self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

		self.filename = ""
		self.font = QtGui.QFont()
		self.font.setFamily("Consolas")
		self.font.setPointSize(11)
		
		self.initUI()

	def initUI(self):
		self.text = QtGui.QPlainTextEdit(self)									# Initialize the TEXTBOX EDITOR
		self.setCentralWidget(self.text)										# Set it as the central widget
		self.text.setFont(self.font)
		self.text.setTabStopWidth(33)

		self.text.cursorPositionChanged.connect(self.cursorPosition)

		self.initToolbar()														# Initialize the bars
		# self.initFormatbar()
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

	def open(self):

		# Get filename and show only .writer files
		self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.chng)"))

		if self.filename:
			with open(self.filename,"rt") as file:
				self.text.setPlainText(file.read())

	def save(self):
		self.statusbar.showMessage('Saved')

		if not self.filename:
			self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.chng)")

		# if not self.filename.endswith(".chng"):
			# self.filename += ".chng"

		with open(self.filename,"wt") as file:
			file.write(self.text.toPlainText())

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
