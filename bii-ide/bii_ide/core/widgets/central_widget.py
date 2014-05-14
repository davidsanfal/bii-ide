from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QString, SIGNAL
import os
from bii_ide.common.biicode.biicode_workspace import BiicodeWorkspace, isBiiWorkspace
from bii_ide.core.widgets.popup.workspace_popup import DialogWorkpace
from bii_ide.common.commands import open_terminal, execute_command
from bii_ide.core.widgets.tab_editor.tab_editor import TabEditor
from bii_ide.common.style.icons import (BUILD, UPLOAD, FIND, SETTINGS, TERMINAL,
                                                     MONITOR)
from bii_ide.common.style.biigui_stylesheet import button_style

GUI_CONFIG = "bii_ide.txt"


class CentralWidget(QtGui.QWidget):

    def __init__(self, gui_path, parent=None):
        super(CentralWidget, self).__init__(parent)
        self.gui_path = gui_path
        self.initUI()

    def initUI(self):
        self.editor = TabEditor()
        self.biicodeWorkspace = BiicodeWorkspace()
        self.gui_configuration_path = os.path.join(self.gui_path, GUI_CONFIG)

        self.hive_selected = None
        self.block_selected = None

        self.createHiveTreeView()
        self.createBiiCommands()
        editor_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        editor_splitter.addWidget(self.editor.tab_widget)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.treeViewBox)
        splitter.addWidget(editor_splitter)
        splitter.addWidget(self.biiButtonsBox)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        if os.path.exists(self.gui_configuration_path):
            gui_configuration = open(self.gui_configuration_path, "r")
            ws_path = gui_configuration.readline()
            gui_configuration.close()
            if ws_path:
                self._update_treeview_info(ws_path)
            if not self.biicodeWorkspace.path:
                self.workspace_finder()
        else:
            gui_configuration = open(self.gui_configuration_path, "w")
            gui_configuration.close()
            self.workspace_finder()

    def createHiveTreeView(self):
        self.hive_selector = QtGui.QComboBox(self)
        self.hive_selector.activated[str].connect(self.handle_hive_selector)

        self.block_selector = QtGui.QComboBox(self)
        self.block_selector.activated[str].connect(self.handle_block_selector)

        self.view = QtGui.QTreeView()
        self.fileSystemModel = QtGui.QFileSystemModel(self.view)

        self.view.setModel(self.fileSystemModel)
        self.view.setRootIndex(self.fileSystemModel.setRootPath(""))
        self.view.hideColumn(0)
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.hideColumn(3)

        self.connect(self.view, SIGNAL("doubleClicked(const QModelIndex&)"),
                self.item_double_clicked)

        hive_title = QtGui.QLabel('Projects')
        block_title = QtGui.QLabel('Blocks')

        hiveBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(hive_title, 1)
        hbox.addWidget(self.hive_selector, 4)
        hiveBox.setLayout(hbox)

        blockBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(block_title, 1)
        hbox.addWidget(self.block_selector, 4)
        blockBox.setLayout(hbox)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(hiveBox)
        vbox.addWidget(blockBox)
        vbox.addWidget(self.view)
        self.treeViewBox = QtGui.QGroupBox("Workspace info")
        self.treeViewBox.setLayout(vbox)

    def createBiiCommands(self):
        self.button_build = QtGui.QPushButton(QtGui.QIcon(BUILD),
                                              '    build',
                                              self)
        self.button_build.setIconSize(QtCore.QSize(40, 40))
        self.button_build.clicked.connect(self.handleBuild)
        self.button_build.setStyleSheet(button_style)

        self.button_upload = QtGui.QPushButton(QtGui.QIcon(UPLOAD),
                                               '    upload',
                                               self)
        self.button_upload.setIconSize(QtCore.QSize(40, 40))
        self.button_upload.clicked.connect(self.handleUpload)
        self.button_upload.setStyleSheet(button_style)

        self.button_find = QtGui.QPushButton(QtGui.QIcon(FIND),
                                             '    find',
                                             self)
        self.button_find.setIconSize(QtCore.QSize(40, 40))
        self.button_find.clicked.connect(self.handleFind)
        self.button_find.setStyleSheet(button_style)

        self.button_settings = QtGui.QPushButton(QtGui.QIcon(SETTINGS),
                                                 '    settings',
                                                 self)
        self.button_settings.setIconSize(QtCore.QSize(40, 40))
        self.button_settings.clicked.connect(self.handleSettings)
        self.button_settings.setStyleSheet(button_style)

        self.button_monitor = QtGui.QPushButton(QtGui.QIcon(MONITOR),
                                                 '    monitor',
                                                 self)
        self.button_monitor.setIconSize(QtCore.QSize(40, 40))
        self.button_monitor.clicked.connect(self.handleMonitor)
        self.button_monitor.setStyleSheet(button_style)

        self.button_terminal = QtGui.QPushButton(QtGui.QIcon(TERMINAL),
                                                     '    Terminal',
                                                     self)
        self.button_terminal.setIconSize(QtCore.QSize(40, 40))
        self.button_terminal.clicked.connect(self.handleTerminal)
        self.button_terminal.setStyleSheet(button_style)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.button_settings, 0, 0)
        grid.addWidget(self.button_find, 1, 0)
        grid.addWidget(self.button_build, 2, 0)
        grid.addWidget(self.button_upload, 3, 0)
        grid.addWidget(self.button_monitor, 4, 0)
        grid.addWidget(self.button_terminal, 5, 0)

        self.biiButtonsBox = QtGui.QGroupBox("commands")
        self.biiButtonsBox.setLayout(grid)
        self.biiButtonsBox.maximumHeight()
        self.biiButtonsBox.setMaximumSize(180, self.biiButtonsBox.maximumHeight())

    def item_double_clicked(self, index):
        path = self.fileSystemModel.filePath(index)
        if os.path.isfile(path):
            self.editor.openFile(path)

    def handle_hive_selector(self, text):
        self.hive_selected = str(text)

        self.block_selector.clear()
        if self.hive_selected:
            default_blocks = self.biicodeWorkspace.hive_blocks(self.hive_selected)
            self.block_selector.addItems(default_blocks)
            if default_blocks:
                self.block_selected = default_blocks[0]
        else:
            self.block_selected = ""
        self._update_path_workspace_info()

    def handle_block_selector(self, text):
        self.block_selected = str(text)
        self._update_path_workspace_info()

    def _update_path_workspace_info(self):
        self.block_path = os.path.join(self.biicodeWorkspace.path,
                                 self.hive_selected,
                                 "blocks",
                                 self.block_selected)
        os.chdir(self.block_path)
        self.view.setRootIndex(self.fileSystemModel.setRootPath(self.block_path))

    def createBiiWorkspace(self):
        file_dialog = QtGui.QFileDialog()
        select_path = file_dialog.getExistingDirectory(parent=None,
                                caption=QString("Select the folder where create the workspace"))
        if not str(select_path) == "" and os.path.exists(str(select_path)):
            execute_command(self.gui_path, str(select_path), "init")

    def handleTerminal(self):
        if self.biicodeWorkspace.path:
            os.chdir(self.biicodeWorkspace.path)
        open_terminal()

    def handleBuild(self):
        self.execute_bii_command("build")

    def newProject(self):
        if self.biicodeWorkspace.path:
            execute_command(self.gui_path, self.biicodeWorkspace.path, "new")
        else:
            QtGui.QMessageBox.about(self, "There are any workspace", "Create a workspace first")
            self.workspace_finder()

    def handleUpload(self):
        self.execute_bii_command("upload")

    def handleFind(self):
        self.execute_bii_command("find")

    def handleSettings(self):
        self.execute_bii_command("settings")

    def handleSetup(self):
        self.execute_bii_command("setup", self.biicodeWorkspace.path)

    def handleMonitor(self):
        self.execute_bii_command("monitor")

    def handleClear(self):
        self.console.clear()

    def refresh_info(self):
        self._refresh_workspace_info()

    def select_folder(self):
        file_dialog = QtGui.QFileDialog()
        select_ws = file_dialog.getExistingDirectory(parent=None,
                                caption=QString("Select Workspace Folder"))

        self._update_treeview_info(str(select_ws))
        if self.biicodeWorkspace.path:
            self._update_gui_config_file(self.biicodeWorkspace.path)

    def _update_treeview_info(self, workspace_path):
        if isBiiWorkspace(workspace_path):
            self.biicodeWorkspace.setPath(workspace_path)
            self._refresh_workspace_info()

        elif not workspace_path == "":
            QtGui.QMessageBox.about(self, "wrong folder", "Choose a biicode workspace")
            self.select_folder()

        elif not self.biicodeWorkspace.path:
            self.view.hideColumn(0)
            self.hive_selector.clear()
            self.block_selector.clear()
            self.hive_selected = None
            self.block_selected = None
            self.view.setRootIndex(self.fileSystemModel.setRootPath(""))

    def _refresh_workspace_info(self):
        if self.biicodeWorkspace.path and self.biicodeWorkspace.hives:
            self.view.showColumn(0)
            self.hive_selector.clear()
            self.hive_selector.addItems(self.biicodeWorkspace.hives)
            self.hive_selected = self.biicodeWorkspace.hives[0]

            self.block_selector.clear()
            default_blocks = self.biicodeWorkspace.hive_blocks(self.hive_selected)
            self.block_selector.addItems(default_blocks)
            self.block_selected = default_blocks[0]

            self._update_path_workspace_info()
        else:
            self.view.hideColumn(0)
            self.hive_selector.clear()
            self.block_selector.clear()
            self.hive_selected = None
            self.block_selected = None
            self.view.setRootIndex(self.fileSystemModel.setRootPath(""))

    def _update_gui_config_file(self, ws_path):
        gui_configuration = open(self.gui_configuration_path, "w")
        gui_configuration.write(ws_path)
        gui_configuration.close()

    def workspace_finder(self):
        init_popup = DialogWorkpace(self.gui_path)
        init_popup.exec_()
        self._update_treeview_info(init_popup.selected_path)
        if self.biicodeWorkspace.path:
            self._update_gui_config_file(self.biicodeWorkspace.path)

    def execute_bii_command(self, command, exe_folder=None):
        if self.hive_selected:
            if not exe_folder:
                exe_folder = self.block_path
            execute_command(self.gui_path, exe_folder, command)
        elif self.biicodeWorkspace.path:
            QtGui.QMessageBox.about(self, "There are any project", "Create a project first")
        else:
            QtGui.QMessageBox.about(self, "There are any workspace", "Create a workspace first")
            self.workspace_finder()
