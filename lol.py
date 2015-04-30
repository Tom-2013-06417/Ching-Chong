from PyQt4 import QtGui
import syntax

app = QtGui.QApplication([])
texter = QtGui.QPlainTextEdit()
highlight = syntax.PythonHighlighter(texter.document())
texter.show()

infile = open('syntax.py', 'r')
texter.setPlainText(infile.read())

app.exec_()