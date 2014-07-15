from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QString
from bii_ide.common.commands import execute_command
from bii_ide.common.style.icons import GUI_ICON, OPENWS, NEWWS, CANCEL_ICON, OK_ICON
from os.path import expanduser
from bii_ide.common.style.biigui_stylesheet import button_style


class DialogWorkpace(QtGui.QDialog):
    def __init__(self, gui_path, parent=None):
        super(DialogWorkpace, self).__init__(parent)
        self.gui_path = gui_path
        self.setWindowTitle('bii-IDE')
        self.createLayout()
        self.setWindowIcon(QtGui.QIcon(GUI_ICON))
        self.resize(400, 200)

        self.selected_path = ""
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.ButtonsBox)

    def createLayout(self):

        title_font = QtGui.QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        text_font = QtGui.QFont()
        text_font.setPointSize(10)
        text_font.setBold(False)

        ws_info = QtGui.QLabel('bii-ide stores your projects in a folder called a workspace.\nYou can change your workspace when you want\n')
        ws_info.setFont(text_font)
        self.selected_ws = QtGui.QLabel('  No workspace selected')
        self.selected_ws.setFont(text_font)
        selected_ws_title = QtGui.QLabel('Selected workspace:')
        selected_ws_title.setFont(title_font)
        button_select_ws = QtGui.QPushButton(
                                QtGui.QIcon(OPENWS),
                                'Select your bii-ide workspace',
                                self)
        button_select_ws.setIconSize(QtCore.QSize(40, 40))
        button_select_ws.clicked.connect(self.handleSelectWorkspace)
        button_select_ws.setStyleSheet(button_style)

        button_ok = QtGui.QPushButton(QtGui.QIcon(OK_ICON), '', self)
        button_ok.setIconSize(QtCore.QSize(40, 40))
        button_ok.clicked.connect(self.handleOk)
        button_ok.setStyleSheet(button_style)

        button_cancel = QtGui.QPushButton(QtGui.QIcon(CANCEL_ICON), '', self)
        button_cancel.setIconSize(QtCore.QSize(40, 40))
        button_cancel.clicked.connect(self.handleCancel)
        button_cancel.setStyleSheet(button_style)

        self.ButtonsBox = QtGui.QGroupBox()
        grid = QtGui.QGridLayout()
        grid.addWidget(ws_info, 0, 0, 1, 2)
        grid.addWidget(button_select_ws, 1, 0, 1, 2)
        grid.addWidget(selected_ws_title, 2, 0, 1, 2)
        grid.addWidget(self.selected_ws, 3, 0, 1, 2)
        grid.addWidget(button_ok, 4, 0)
        grid.addWidget(button_cancel, 4, 1)
        self.ButtonsBox.setLayout(grid)

    def handleSelectWorkspace(self):
        file_dialog = QtGui.QFileDialog()
        select_ws = file_dialog.getExistingDirectory(parent=None,
                                                     directory=QString(expanduser("~")),
                                                     caption=QString("Select Workspace Folder"))

        self.selected_ws.setText(select_ws)
        self.selected_path = str(select_ws)

    def handleCreateWorkspace(self):
        file_dialog = QtGui.QFileDialog()
        select_ws = file_dialog.getExistingDirectory(parent=None,
                                                     directory=QString(expanduser("~")),
                                                     caption=QString("Select the folder where create the workspace"))

        self.selected_path = str(select_ws)
        if not self.selected_path == "":
            execute_command(self.gui_path, str(self.selected_path), "init")

    def handleOk(self):
        if self.selected_path != "":
            self.close()
        else:
            QtGui.QMessageBox.about(self, "wrong folder",
                                    "Choose a bii-ide workspace or create one")

    def handleCancel(self):
        self.close()
