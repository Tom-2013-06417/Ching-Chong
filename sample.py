import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt



class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self,parent)

		self.filename = ""
		self.font = QtGui.QFont()
		self.font.setFamily("Consolas")
		self.font.setPointSize(11)
		
		self.initUI()

	def initUI(self):
		self.text = QtGui.QPlainTextEdit(self)									# Initialize the TEXTBOX EDITOR
		self.setCentralWidget(self.text)										# Set it as the central widget
		self.text.setFont(self.font)
		self.text.setTabStopWidth(40)

		self.initToolbar()														# Initialize the bars
		# self.initFormatbar()
		self.initMenubar()
		
		self.statusbar = self.statusBar()										# Initialize a statusbar for the window
		self.statusbar.showMessage('KEK')										# Show the message
		
		self.setGeometry(180,100,1030,600)										# x and y coordinates on the screen, width, height
		self.setWindowTitle("Ching Chong IDE")

	def initToolbar(self):
		# self.toolbar = self.addToolBar("Options")								# Initialize the OPTIONS toolbar

		self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
		self.newAction.setStatusTip("Create a new document from scratch.")
		self.newAction.setShortcut("Ctrl+N")
		self.newAction.triggered.connect(self.new)

		self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open filez",self)
		self.openAction.setStatusTip("Open existing document")
		self.openAction.setShortcut("Ctrl+O")
		self.openAction.triggered.connect(self.open)

		self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
		self.saveAction.setStatusTip("Save document")
		self.saveAction.setShortcut("Ctrl+S")
		self.saveAction.triggered.connect(self.save)

		# self.toolbar.addAction(self.newAction)
		# self.toolbar.addAction(self.openAction)

		# self.addToolBarBreak()													# Makes the next toolbar appear underneath this one

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

	def new(self):
		spawn = Main(self)
		spawn.show()

	def open(self):

		# Get filename and show only .writer files
		self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.chng)"))

		if self.filename:
			with open(self.filename,"rt") as file:
				self.text.setPlainText(file.read())

	def save(self):
		# Only open dialog if there is no filename yet
		self.statusbar.showMessage('Saved')

		if not self.filename:
			self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

		# Append extension if not there yet
		if not self.filename.endswith(".chng"):
			self.filename += ".chng"

		# We just store the contents of the text file along with the
		# format in html, which Qt does in a very nice way for us
		with open(self.filename,"wt") as file:
			file.write(self.text.toPlainText())



def main():

	app = QtGui.QApplication(sys.argv)

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
