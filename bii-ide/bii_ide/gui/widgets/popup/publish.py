from PyQt4 import QtGui, QtCore
from bii_ide.common.style.biigui_stylesheet import button_style
from bii_ide.common.style.icons import OK_ICON, CANCEL_ICON


Tags = ["DEV", "ALPHA", "BETA", "STABLE"]


class BiiPublish(QtGui.QDialog):
    def __init__(self, blocks):
        QtGui.QDialog.__init__(self)
        self.request = ""
        self.tag_selected = "Dev"
        self.block_selected = blocks[0]
        self.createLayout(blocks)

    def createLayout(self, blocks):

        block_title = QtGui.QLabel('Block')
        block_selector = QtGui.QComboBox(self)
        block_selector.addItems(blocks)
        block_selector.activated[str].connect(self.handle_block_selector)

        tag_title = QtGui.QLabel('Tag')
        tag_box = QtGui.QComboBox(self)
        tag_box.addItems(Tags)
        tag_box.activated[str].connect(self.handle_tag_selector)

        msg_title = QtGui.QLabel('Message')
        self.msg = QtGui.QLineEdit(self)
        branch_title = QtGui.QLabel('Branch')
        self.branch = QtGui.QLineEdit(self)

        button_ok = QtGui.QPushButton(QtGui.QIcon(OK_ICON), '', self)
        button_ok.setIconSize(QtCore.QSize(40, 40))
        button_ok.clicked.connect(self.handleOk)
        button_ok.setStyleSheet(button_style)

        button_cancel = QtGui.QPushButton(QtGui.QIcon(CANCEL_ICON), '', self)
        button_cancel.setIconSize(QtCore.QSize(40, 40))
        button_cancel.clicked.connect(self.handleCancel)
        button_cancel.setStyleSheet(button_style)

        blockBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(block_title, 1)
        hbox.addWidget(block_selector, 4)
        blockBox.setLayout(hbox)

        tagBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(tag_title, 1)
        hbox.addWidget(tag_box, 4)
        tagBox.setLayout(hbox)

        msgBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(msg_title, 1)
        hbox.addWidget(self.msg, 4)
        msgBox.setLayout(hbox)

        branchBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(branch_title, 1)
        hbox.addWidget(self.branch, 4)
        branchBox.setLayout(hbox)

        okCancelBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(button_ok)
        hbox.addWidget(button_cancel)
        okCancelBox.setLayout(hbox)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(blockBox)
        vbox.addWidget(tagBox)
        vbox.addWidget(msgBox)
        vbox.addWidget(branchBox)
        vbox.addWidget(okCancelBox)

        self.setLayout(vbox)

    def handle_block_selector(self, text):
        self.block_selected = str(text)

    def handle_tag_selector(self, text):
        self.tag_selected = str(text)

    def handleOk(self):
        reply = QtGui.QMessageBox.question(self, 'Publish info',
            "\nAre you sure to publish %s?\n" % self.block_selected,
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self._create_request()
            self.close()

    def handleCancel(self):
        self.close()

    def _create_request(self):
        self.request = 'publish %s --tag=%s' % (self.block_selected, self.tag_selected)
        if self.msg.text():
            self.request = '%s --msg="%s"' % (self.request, str(self.msg.text()))
        if self.branch.text():
            self.request = '%s --branch="%s"' % (self.request, str(self.branch.text()))
