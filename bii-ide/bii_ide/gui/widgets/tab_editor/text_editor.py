from PyQt4 import QtGui, QtCore
from bii_ide.gui.widgets.tab_editor.highlighter import Highlighter
from PyQt4.QtCore import pyqtSlot
from bii_ide.common.style.biigui_stylesheet import editor_style


class Editor(QtGui.QTextEdit):

    def __init__(self, tab_widget):
        super(Editor, self).__init__(tab_widget)
        self.setStyleSheet(editor_style)
        self.tab = tab_widget
        self.initUI()
        self.path_file = None
        self.content_file = ""
        self.text_changed = False
        self.tab_number = None

    def initUI(self):
        self.setFont(self.font)
        self.connect(self, QtCore.SIGNAL("textChanged()"),
                     self, QtCore.SLOT("handleTextChanged()"))

        self.highlighter = Highlighter(self.document())

    @property
    def font(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
        return font

    @pyqtSlot()
    def handleTextChanged(self):
        if not self.text_changed:
            if not self.content_file == self.toPlainText():
                self.text_changed = True
                index = self.tab.indexOf(self)
                name = "* %s" % self.tab.tabText(index)
                self.tab.setTabText(index, name)
