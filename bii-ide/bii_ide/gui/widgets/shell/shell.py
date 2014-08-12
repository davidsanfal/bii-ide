from PyQt4 import QtGui
from bii_ide.common.style.biigui_stylesheet import shell_style


class Shell(QtGui.QTextBrowser):

    def __init__(self):
        super(Shell, self).__init__()
        self.setStyleSheet(shell_style)
        self.initUI()

    def initUI(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setText("bii-IDE Shell")

    def addText(self, data):
        data = self.toPlainText() + data
        self.setText(data)
        self.moveCursor(QtGui.QTextCursor.End)
