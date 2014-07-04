from PyQt4 import QtGui
from bii_ide.core.widgets.central_widget import CentralWidget
import os
from bii_ide.common.style.icons import (GUI_ICON, REFRESHWS, OPENWS, NEWWS,
    SETTINGS, FIND, BUILD, UPLOAD, QT_ICON, ARDUINO_GREY, BII_GREY, NEWFILE,
    SAVEFILE, OPENFILE, EXIT_ICON, TERMINAL, SETUP, MONITOR, NEWPROJECT, CLEAN)
from bii_ide.core.widgets.about.about_biigui import AboutBiiGUI
from bii_ide.common.biicode.biicode_dependencies import dependencies_finder
import sys


class biiGUI(QtGui.QMainWindow):

    def __init__(self):
        super(biiGUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon(GUI_ICON))
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('bii-IDE')
        if not dependencies_finder():
            QtGui.QMessageBox.question(self, "Missing dependencies",
                                       "Missing the following tools:\n-> biicode",
                                       QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            sys.exit()
        self.gui_path = os.getcwd()
        if not os.path.exists(os.path.join(self.gui_path, 'resources')):
            # PyInstaller route
            self.gui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        self.centralWidget = CentralWidget(self.gui_path)
        self.menubar = self.menuBar()
        self.CreateFileMenu()
        self.createWorkspaceMenu()
        self.createBiicodeMenu()
        self.createAboutMenu()
        self.setCentralWidget(self.centralWidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Exit',
            "\nAre you sure to quit?\n", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        self.centralWidget.editor.close_all_tabs()
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def createWorkspaceMenu(self):
        refresh = QtGui.QAction(QtGui.QIcon(REFRESHWS),
                                'Refresh workspace info', self)
        refresh.setShortcut('F5')
        refresh.setStatusTip('Refresh workspace info')
        refresh.triggered.connect(self.centralWidget.refresh_info)

        openWS = QtGui.QAction(QtGui.QIcon(OPENWS),
                               'Open workspace', self)

        openWS.setStatusTip('Open a workspace')
        openWS.triggered.connect(self.centralWidget.select_folder)

        newWS = QtGui.QAction(QtGui.QIcon(NEWWS),
                              'New workspace', self)

        newWS.setStatusTip('New workspace')
        newWS.triggered.connect(self.centralWidget.createWorkspace)

        workspaceMenu = self.menubar.addMenu('&Workspace')
        workspaceMenu.addAction(newWS)
        workspaceMenu.addAction(openWS)
        workspaceMenu.addAction(refresh)

        workspacToolbar = self.addToolBar('workspace')
        workspacToolbar.addAction(refresh)
        workspacToolbar.addAction(newWS)
        workspacToolbar.addAction(openWS)

    def createBiicodeMenu(self):
        settings = QtGui.QAction(QtGui.QIcon(SETTINGS),
                                 'bii arduino:settings', self)
        settings.setStatusTip('Settings')
        settings.triggered.connect(self.centralWidget.handleSettings)

        find = QtGui.QAction(QtGui.QIcon(FIND),
                             'bii find', self)
        find.setStatusTip('Find')
        find.triggered.connect(self.centralWidget.handleFind)

        build = QtGui.QAction(QtGui.QIcon(BUILD),
                              'bii arduino:build', self)
        build.setStatusTip('Build')
        build.triggered.connect(self.centralWidget.handleBuild)

        upload = QtGui.QAction(QtGui.QIcon(UPLOAD),
                               'bii arduino:upload', self)
        upload.setStatusTip('Upload')
        upload.triggered.connect(self.centralWidget.handleUpload)

        terminal = QtGui.QAction(QtGui.QIcon(TERMINAL),
                               'open a terminal', self)
        terminal.setStatusTip('Terminal')
        terminal.triggered.connect(self.centralWidget.handleTerminal)

        setup = QtGui.QAction(QtGui.QIcon(SETUP),
                               'bii setup:arduino', self)
        setup.setStatusTip('Setup tool')
        setup.triggered.connect(self.centralWidget.handleSetup)

        clean = QtGui.QAction(QtGui.QIcon(CLEAN),
                               'bii clean', self)
        clean.setStatusTip('Clean biicode project')
        clean.triggered.connect(self.centralWidget.handleClean)

        monitor = QtGui.QAction(QtGui.QIcon(MONITOR),
                               'bii arduino:monitor', self)
        monitor.setStatusTip('Serial monitor')
        monitor.triggered.connect(self.centralWidget.handleMonitor)

        biiMenu = self.menubar.addMenu('&commands')
        biiMenu.addAction(settings)
        biiMenu.addAction(find)
        biiMenu.addAction(build)
        biiMenu.addAction(upload)
        biiMenu.addAction(monitor)
        biiMenu.addAction(clean)
        biiMenu.addAction(setup)
        biiMenu.addAction(terminal)

        biiToolbar = self.addToolBar('biicode')
        biiToolbar.addAction(settings)
        biiToolbar.addAction(find)
        biiToolbar.addAction(build)
        biiToolbar.addAction(upload)
        biiToolbar.addAction(monitor)
        biiToolbar.addAction(clean)

    def createAboutMenu(self):
        about_qt = QtGui.QAction('About Qt', self)
        about_qt.setIcon(QtGui.QIcon(QT_ICON))
        about_qt.setStatusTip('Refresh workspace info')

        def aboutqt():
            QtGui.QMessageBox.aboutQt(self, "About Qt")
        about_qt.triggered.connect(aboutqt)

        aboutBiiDocs = QtGui.QAction('Arduino and biicode', self)
        aboutBiiDocs.setIcon(QtGui.QIcon(ARDUINO_GREY))
        aboutBiiDocs.triggered.connect(self.centralWidget.editor.openBiiArduinoDocs)

        aboutBiicode = QtGui.QAction('About biicode', self)
        aboutBiicode.setIcon(QtGui.QIcon(BII_GREY))
        aboutBiicode.triggered.connect(self.centralWidget.editor.openBiicoode)

        aboutBiiGUI = QtGui.QAction('About bii-IDE', self)
        aboutBiiGUI.setIcon(QtGui.QIcon(GUI_ICON))

        def aboutbiigui():
            self.about = AboutBiiGUI()
            self.about.show()
        aboutBiiGUI.triggered.connect(aboutbiigui)

        AboutMenu = self.menubar.addMenu('&About')
        AboutMenu.addAction(aboutBiiGUI)
        AboutMenu.addAction(aboutBiicode)
        AboutMenu.addAction(aboutBiiDocs)
        AboutMenu.addAction(about_qt)

        AboutToolbar = self.addToolBar('About')
        AboutToolbar.addAction(aboutBiiDocs)

    def CreateFileMenu(self):
        newProjectAction = QtGui.QAction(QtGui.QIcon(NEWPROJECT),
                                  'New project', self)
        newProjectAction.setStatusTip('Create new project')
        newProjectAction.triggered.connect(self.centralWidget.newProject)

        newAction = QtGui.QAction(QtGui.QIcon(NEWFILE),
                                  'New file', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.centralWidget.editor.newFile)

        saveAction = QtGui.QAction(QtGui.QIcon(SAVEFILE),
                                   'Save file', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.centralWidget.editor.saveFile)

        openAction = QtGui.QAction(QtGui.QIcon(OPENFILE),
                                   'Open file', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.centralWidget.editor.openFile)

        closeAction = QtGui.QAction(QtGui.QIcon(EXIT_ICON),
                                    'Close biiGUI', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close biiGUI')
        closeAction.triggered.connect(self.close)

        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(newProjectAction)
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(closeAction)

        fileToolbar = self.addToolBar('File')
        fileToolbar.addAction(saveAction)
        fileToolbar.addAction(newAction)
        fileToolbar.addAction(openAction)
        fileToolbar.addAction(newProjectAction)
