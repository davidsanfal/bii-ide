from PyQt4 import QtGui, QtCore
import os
from bii_ide.gui.widgets.tab_editor.text_editor import Editor
from PyQt4.QtCore import pyqtSlot
from bii_ide.gui.widgets.tab_editor.browser import BrowserWidget
from bii_ide.common.style.biigui_stylesheet import tab_style


class TabEditor(QtGui.QTabWidget):

    def __init__(self):
        super(TabEditor, self).__init__()
        self.worfpace_path = None
        self.tab_selected = None
        self.files_open = []
        self.docs_browser = None
        self.biicode_browser = None
        self.initUI()

    @pyqtSlot(int)
    def tabChangedSlot(self, argTabIndex):
        self.tab_selected = argTabIndex

    def initUI(self):
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.setStyleSheet(tab_style)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.connect(self.tab_widget, QtCore.SIGNAL("currentChanged(int)"),
                                self, QtCore.SLOT("tabChangedSlot(int)"))

        self.connect(self.tab_widget, QtCore.SIGNAL('tabCloseRequested(int)'),
                     self, QtCore.SLOT('closeTab(int)'))
        self.openBiiArduinoDocs()

    def openBiiArduinoDocs(self):
        if not self.docs_browser:
            self.docs_browser = BrowserWidget()
            self.tab_selected = self.tab_widget.addTab(self.docs_browser, "Arduino docs")
            self.tab_widget.setCurrentIndex(self.tab_selected)
        else:
            self.tab_selected = self.tab_widget.indexOf(self.docs_browser)
            self.tab_widget.setCurrentIndex(self.tab_selected)

    def openBiicoode(self):
        if not self.biicode_browser:
            self.biicode_browser = BrowserWidget("https://www.biicode.com/")
            self.tab_selected = self.tab_widget.addTab(self.biicode_browser, "biicode")
            self.tab_widget.setCurrentIndex(self.tab_selected)
        else:
            self.tab_selected = self.tab_widget.indexOf(self.biicode_browser)
            self.tab_widget.setCurrentIndex(self.tab_selected)

    @pyqtSlot(int)
    def closeTab(self, argTabIndex):
        editor = self.tab_widget.widget(argTabIndex)
        if editor == self.biicode_browser:
            self.biicode_browser = None
        elif editor == self.docs_browser:
                self.docs_browser = None
        elif editor.text_changed:
            name = self.tab_widget.tabText(argTabIndex).replace('* ', '')
            reply = QtGui.QMessageBox.question(self, 'Close file',
                ("\n%s file has been modified\nSave changes?\n" % name),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel)

            if reply == QtGui.QMessageBox.Cancel:
                return
            elif reply == QtGui.QMessageBox.Yes:
                self.saveFile(argTabIndex)
        self.tab_widget.removeTab(argTabIndex)

        for editor_info in self.files_open:
            _filename, _editor = editor_info
            if editor == _editor:
                self.files_open.remove([_filename, _editor])
                break

    def close_all_tabs(self):
        for x in reversed(range(0, self.tab_widget.count())):
            self.closeTab(x)

    def newFile(self, hive_path=None):
        if hive_path:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'New File', hive_path)
        else:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'New File')
        if not str(filename) == "":
            f = open(filename, 'w')
            f.close()
            self.openFile(filename)

    def saveAsFile(self):
        if self.tab_selected >= 0:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
            f = open(filename, 'w')
            filedata = self.editor.toPlainText()
            f.write(filedata)
            f.close()

    def saveFile(self, tab_to_save=None):
        if not tab_to_save:
            tab_to_save = self.tab_selected
        if  tab_to_save >= 0:
            editor = self.tab_widget.widget(self.tab_selected)
            if editor == self.biicode_browser or editor == self.docs_browser:
                return
            filename = editor.path_file
            if not filename:
                filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
            f = open(filename, 'w')
            filedata = editor.toPlainText()
            f.write(filedata)
            f.close()
            editor.text_changed = False
            name = self.tab_widget.tabText(tab_to_save).replace('* ', '')
            self.tab_widget.setTabText(tab_to_save, name)

    def openFile(self, filename=None):
        if not filename:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        if not str(filename) == "":
            for editor_info in self.files_open:
                _filename, _editor = editor_info
                if filename == _filename:
                    self.tab_selected = self.tab_widget.indexOf(_editor)
                    self.tab_widget.setCurrentIndex(self.tab_selected)
                    return
            with open(filename, 'r') as f:
                filedata = f.read()
                text_widget = Editor(self.tab_widget)
                text_widget.content_file = filedata
                text_widget.path_file = str(filename)
                text_widget.setText(filedata)
                self.tab_selected = self.tab_widget.addTab(text_widget, os.path.basename(str(filename)))
                self.files_open.append([filename, text_widget])
                self.tab_widget.setCurrentIndex(self.tab_selected)
