import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):

	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self,parent)

		self.initUI()

	def initUI(self):

		self.text = QtGui.QTextEdit(self)
		self.setCentralWidget(self.text)

		self.initToolbar()
		self.initFormatbar()
		self.initMenubar()

		# Initialize a statusbar for the window
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('LOL')

		# x and y coordinates on the screen, width, height
		self.setGeometry(180,100,1030,600)

		self.setWindowTitle("Ching Chong IDE")

	def initToolbar(self):

		self.toolbar = self.addToolBar("Options")

		# Makes the next toolbar appear underneath this one
		self.addToolBarBreak()

	def initFormatbar(self):

		self.formatbar = self.addToolBar("Format")

	def initMenubar(self):

		menubar = self.menuBar()

		file = menubar.addMenu("File")
		edit = menubar.addMenu("Edit")
		view = menubar.addMenu("View")
		tools = menubar.addMenu("Tools")



def main():

	app = QtGui.QApplication(sys.argv)

	main = Main()
	main.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()