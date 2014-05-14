from PyQt4 import QtCore, QtGui, QtWebKit
from bii_ide.common.style.biigui_stylesheet import browser_style


class BrowserWidget(QtGui.QWidget):

    def __init__(self, url="http://docs.biicode.com/arduino.html", parent=None):
        super(BrowserWidget, self).__init__(parent)
        self.initUI(url)

    def initUI(self, url):
        vbox = QtGui.QVBoxLayout(self)
        #Web Frame
        self.webFrame = QtWebKit.QWebView(self)
        self.webFrame.setStyleSheet(browser_style)
        self.webFrame.setAcceptDrops(False)
        self.webFrame.load(QtCore.QUrl(url))
        vbox.addWidget(self.webFrame)
        self.webFrame.page().currentFrame().setScrollBarPolicy(
            QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAsNeeded)
        self.webFrame.page().currentFrame().setScrollBarPolicy(
            QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAsNeeded)
