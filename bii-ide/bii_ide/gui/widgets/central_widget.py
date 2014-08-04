from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QString, SIGNAL
import os
from bii_ide.common.bii_ide_workspace import BiiIdeWorkspace
from bii_ide.gui.widgets.popup.workspace_popup import DialogWorkpace
from bii_ide.common.commands import open_terminal, execute_command
from bii_ide.gui.widgets.tab_editor.tab_editor import TabEditor
from bii_ide.common.style.icons import (BUILD, UPLOAD, FIND, SETTINGS, TERMINAL,
                                                     MONITOR, CLEAN)
from bii_ide.common.style.biigui_stylesheet import button_style
from bii_ide.gui.widgets.combobox_event import ShowEventFilter
from bii_ide.gui.widgets.shell.shell import Shell


GUI_CONFIG = "bii_ide.txt"


class CentralWidget(QtGui.QWidget):

    def __init__(self, gui_path, parent=None):
        super(CentralWidget, self).__init__(parent)
        self.gui_path = gui_path
        self.initUI()

    def initUI(self):
        self.editor = TabEditor()
        self.shell = Shell()
        self.biiIdeWorkspace = BiiIdeWorkspace()
        self.gui_configuration_path = os.path.join(self.gui_path, GUI_CONFIG)

        self.project_selected = None
        self.block_selected = None
        self.port_selected = None
        self.firmware_selected = None
        self.board_selected = 'uno'

        self.createProjectTreeView()
        self.createBiiCommands()
        editor_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        editor_splitter.addWidget(self.editor.tab_widget)
        editor_splitter.addWidget(self.shell)

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
            if not self.biiIdeWorkspace.path:
                self.workspace_finder()
        else:
            gui_configuration = open(self.gui_configuration_path, "w")
            gui_configuration.close()
            self.workspace_finder()

    def createProjectTreeView(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import Arduino_boards
        self.port_box = QtGui.QComboBox(self)
        portEventFilter = ShowEventFilter(self._update_ports)
        self.port_box.view().installEventFilter(portEventFilter)
        self.port_box.activated[str].connect(self.handle_port_selector)

        self.firmare_box = QtGui.QComboBox(self)
        firmareEventFilter = ShowEventFilter(self._update_firmawares)
        self.firmare_box.view().installEventFilter(firmareEventFilter)
        self.firmare_box.activated[str].connect(self.handle_firmware_selector)

        self.board_box = QtGui.QComboBox(self)
        self.board_box.addItems(Arduino_boards)
        self.board_box.activated[str].connect(self.handle_board_selector)

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

        port_title = QtGui.QLabel('Port')
        board_title = QtGui.QLabel('Board')
        firmware_title = QtGui.QLabel('Firmware')

        hive_title = QtGui.QLabel('Projects')
        block_title = QtGui.QLabel('Blocks')

        hardwareBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(port_title, 1)
        hbox.addWidget(self.port_box, 4)
        hbox.addWidget(board_title, 1)
        hbox.addWidget(self.board_box, 4)
        hardwareBox.setLayout(hbox)

        firmwareBox = QtGui.QGroupBox()
        hbox = QtGui.QHBoxLayout(self)
        hbox.addWidget(firmware_title, 1)
        hbox.addWidget(self.firmare_box, 4)
        firmwareBox.setLayout(hbox)

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
        vbox.addWidget(hardwareBox)
        vbox.addWidget(firmwareBox)
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

        self.button_clean = QtGui.QPushButton(QtGui.QIcon(CLEAN),
                                                 '    clean',
                                                 self)
        self.button_clean.setIconSize(QtCore.QSize(40, 40))
        self.button_clean.clicked.connect(self.handleClean)
        self.button_clean.setStyleSheet(button_style)

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
        grid.addWidget(self.button_clean, 5, 0)
        grid.addWidget(self.button_terminal, 6, 0)

        self.biiButtonsBox = QtGui.QGroupBox("commands")
        self.biiButtonsBox.setLayout(grid)
        self.biiButtonsBox.maximumHeight()
        self.biiButtonsBox.setMaximumSize(180, self.biiButtonsBox.maximumHeight())

    def createHardwareToolBar(self, toolbar):
        toolbar.addWidget(QtGui.QLabel('  Port:  '))
        toolbar.addWidget(self.port_box)
        toolbar.addWidget(QtGui.QLabel('  Firmware:  '))
        toolbar.addWidget(self.firmare_box)

    def _update_firmawares(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import detect_firmwares
        if self.block_selected:
            firmwares = detect_firmwares(os.path.join(self.biiIdeWorkspace.path,
                                                      self.project_selected))
            self.firmare_box.clear()
            if firmwares:
                self.firmare_box.addItems(firmwares)
                self.firmware_selected = firmwares[0]
            else:
                self.firmware_selected = None
        else:
            self.firmware_selected = None

    def _update_ports(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import detect_arduino_port
        ports = detect_arduino_port()
        self.port_box.clear()
        if ports:
            self.port_box.addItems(ports)
            self.port_selected = ports[0]
        else:
            self.port_selected = None

    def item_double_clicked(self, index):
        path = self.fileSystemModel.filePath(index)
        if os.path.isfile(path):
            self.editor.openFile(path)

    def handle_hive_selector(self, text):
        self.project_selected = str(text)

        self.block_selector.clear()
        if self.project_selected:
            default_blocks = self.biiIdeWorkspace.hive_blocks(self.project_selected)
            self.block_selector.addItems(default_blocks)
            self.block_selected = ""
            if default_blocks:
                self.block_selected = default_blocks[0]
        else:
            self.block_selected = ""
        self._update_path_workspace_info()

    def handle_block_selector(self, text):
        self.block_selected = str(text)
        self._update_path_workspace_info()

    def handle_firmware_selector(self, text):
        self.firmware_selected = str(text)

    def handle_port_selector(self, text):
        self.port_selected = str(text)

    def handle_board_selector(self, text):
        self.board_selected = str(text)

    def _update_path_workspace_info(self):
        self.block_path = os.path.join(self.biiIdeWorkspace.path,
                                 self.project_selected,
                                 "blocks",
                                 self.block_selected)
        os.chdir(self.block_path)
        self._update_firmawares()
        self.view.setRootIndex(self.fileSystemModel.setRootPath(self.block_path))

    def createWorkspace(self):
        file_dialog = QtGui.QFileDialog()
        select_path = file_dialog.getExistingDirectory(parent=None,
                                caption=QString("Select the folder where create the workspace"))
        if not str(select_path) == "":
            if not os.path.exists(str(select_path)):
                os.mkdir(str(select_path))
            self._update_treeview_info(str(select_path))
            if self.biiIdeWorkspace.path:
                self._update_gui_config_file(self.biiIdeWorkspace.path)

    def newProject(self):
        if self.biiIdeWorkspace.path:
            execute_command(self.gui_path, self.biiIdeWorkspace.path, "init")
        else:
            QtGui.QMessageBox.about(self, "There are any workspace", "Create a workspace first")
            self.workspace_finder()

    def handleTerminal(self):
        if self.biiIdeWorkspace.path:
            os.chdir(self.biiIdeWorkspace.path)
        open_terminal()

    def handleBuild(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import build
        self.execute_bii_command(build, self.block_path)

    def handleUpload(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import upload
        self.execute_bii_command(upload, self.block_path, self.firmware_selected)

    def handleFind(self):
        from bii_ide.common.biicode.dev.biicode_tool_chain import find
        self.execute_bii_command(find, self.block_path)

    def handleClean(self):
        from bii_ide.common.biicode.dev.biicode_tool_chain import clean
        self.execute_bii_command(clean, self.block_path)

    def handleSettings(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import settings
        self.execute_bii_command(settings,
                                 self.block_path,
                                 self.board_selected,
                                 self.port_selected)

    def handleSetup(self):
        from bii_ide.common.biicode.dev.biicode_tool_chain import setup
        self.execute_bii_command(setup, self.biiIdeWorkspace.path)

    def handleMonitor(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import monitor
        self.execute_bii_command(monitor, self.block_path)

    def refresh_info(self):
        self._refresh_workspace_info()

    def select_folder(self):
        file_dialog = QtGui.QFileDialog()
        select_ws = file_dialog.getExistingDirectory(parent=None,
                                caption=QString("Select Workspace Folder"))

        self._update_treeview_info(str(select_ws))
        if self.biiIdeWorkspace.path:
            self._update_gui_config_file(self.biiIdeWorkspace.path)

    def _update_treeview_info(self, workspace_path):
        if workspace_path != "":
            self.biiIdeWorkspace.setPath(workspace_path)
            self._refresh_workspace_info()

        elif not workspace_path == "":
            QtGui.QMessageBox.about(self, "wrong folder", "Choose a biicode workspace")
            self.select_folder()

        elif not self.biiIdeWorkspace.path:
            self.view.hideColumn(0)
            self.hive_selector.clear()
            self.block_selector.clear()
            self.project_selected = None
            self.block_selected = None
            self.view.setRootIndex(self.fileSystemModel.setRootPath(""))

    def _refresh_workspace_info(self):
        self._update_ports()
        if self.biiIdeWorkspace.path and self.biiIdeWorkspace.hives:
            self._update_firmawares()
            self.view.showColumn(0)
            self.hive_selector.clear()
            self.hive_selector.addItems(self.biiIdeWorkspace.hives)
            if self.project_selected in self.biiIdeWorkspace.hives:
                project_index = self.biiIdeWorkspace.hives.index(self.project_selected)
                self.hive_selector.setCurrentIndex(project_index)
            else:
                self.project_selected = self.biiIdeWorkspace.hives[0]

            self.block_selector.clear()
            default_blocks = self.biiIdeWorkspace.hive_blocks(self.project_selected)
            self.block_selector.addItems(default_blocks)
            if self.block_selected in default_blocks:
                self.block_selector.setCurrentIndex(default_blocks.index(self.block_selected))
            else:
                self.block_selected = default_blocks[0] if len(default_blocks) > 0 else ""

            self._update_path_workspace_info()
        else:
            self.view.hideColumn(0)
            self.firmare_box.clear()
            self.hive_selector.clear()
            self.block_selector.clear()
            self.project_selected = None
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
        if self.biiIdeWorkspace.path:
            self._update_gui_config_file(self.biiIdeWorkspace.path)

    def execute_bii_command(self, function, exe_folder, *args, **kwargs):
        if self.project_selected:
            self.shell.setText("%s\n\n" % function.__doc__)
            error, out = function(self.shell.addText, exe_folder, *args, **kwargs)
            if error:
                if out == 'Permission denied':
                    self.shell.setText('Has been an error with the permission of your OS, a terminal was open to solve this problem.')
                else:
                    self.shell.addText("unexpected error occured\n\n")
            elif not out:
                self.shell.addText("Finished\n\n")
        elif self.biiIdeWorkspace.path:
            QtGui.QMessageBox.about(self, "There are any project", "Create a project first")
        else:
            QtGui.QMessageBox.about(self, "There are any workspace", "Select a workspace first")
            self.workspace_finder()
