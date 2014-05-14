import os


#GENERAL
_path = os.getcwd()
if not os.path.exists(os.path.join(_path, 'resources')):
    # PyInstaller route
    _path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

GUI_ICON = "%s/resources/img/gorilla.png" % _path
GUI_ICON_128 = "%s/resources/img/gorilla_128.png" % _path
OK_ICON = "%s/resources/img/ok.png" % _path
CANCEL_ICON = "%s/resources/img/cancel.png" % _path
EXIT_ICON = "%s/resources/img/exit.png" % _path
PROCESS_ICON = "%s/resources/img/process.png" % _path
#EDITOR
NEWPROJECT = "%s/resources/img/editor/newProject.png" % _path
NEWFILE = "%s/resources/img/editor/newFile.png" % _path
OPENFILE = "%s/resources/img/editor/openFile.png" % _path
SAVEFILE = "%s/resources/img/editor/saveFile.png" % _path
#BIIORKSPACE
NEWWS = "%s/resources/img/biiworkspace/newws.png" % _path
OPENWS = "%s/resources/img/biiworkspace/openws.png" % _path
REFRESHWS = "%s/resources/img/biiworkspace/refreshws.png" % _path
#BIICOMMAND
BUILD = "%s/resources/img/biicommand/build.png" % _path
FIND = "%s/resources/img/biicommand/find.png" % _path
MONITOR = "%s/resources/img/biicommand/monitor.png" % _path
SETTINGS = "%s/resources/img/biicommand/settings.png" % _path
TERMINAL = "%s/resources/img/biicommand/terminal.png" % _path
SETUP = "%s/resources/img/biicommand/setup.png" % _path
UPLOAD = "%s/resources/img/biicommand/upload.png" % _path
#about
ARDUINO_GREY = "%s/resources/img/about/arduino_grey.png" % _path
BII_GREY = "%s/resources/img/about/bii_grey.png" % _path
HELP = "%s/resources/img/about/help.png" % _path
QT_ICON = "%s/resources/img/about/qt.png" % _path
