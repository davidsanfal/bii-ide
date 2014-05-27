import webbrowser
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from bii_ide.common.style.icons import GUI_ICON_128
from bii_ide import __version__


class AboutBiiGUI(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.tr("About Bii-IDE"))
        vbox = QVBoxLayout(self)

        pixmap = QPixmap(GUI_ICON_128)
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lblIcon)

        lblTitle = QLabel(
                '<h1>Bii-IDE</h1>\n<i>Arduino IDE<i>')
        lblTitle.setTextFormat(Qt.RichText)
        lblTitle.setAlignment(Qt.AlignLeft)
        hbox.addWidget(lblTitle)
        vbox.addLayout(hbox)
        vbox.addWidget(QLabel(self.tr("""Bii-IDE: Arduino IDE with support for biicode""")))
        vbox.addWidget(QLabel(self.tr("Version: %s" % __version__)))
        link_biigui = QLabel(
            self.tr('Website: <a href="https://github.com/biicode/bii-ide"><span style=" '
                'text-decoration: underline; color:#ff9e21;">'
                'https://github.com/biicode/bii-ide</span></a>'))
        vbox.addWidget(link_biigui)
        link_source = QLabel(
            self.tr('Source Code: <a href="https://github.com/biicode/bii-ide"><span style=" '
        'text-decoration: underline; color:#ff9e21;">https://github.com/biicode/bii-ide</span></a>'))
        vbox.addWidget(link_source)

        self.connect(link_biigui, SIGNAL("linkActivated(QString)"),
            self.link_activated)
        self.connect(link_source, SIGNAL("linkActivated(QString)"),
            self.link_activated)

    def link_activated(self, link):
        webbrowser.open(str(link))
