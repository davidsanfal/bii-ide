import sys
from PyQt4 import QtGui
from bii_ide.gui.biigui_main_window import biiGUI
import platform


def main():
    app = QtGui.QApplication(sys.argv)
    if platform.system() == "Linux":
        app.setStyle(QtGui.QStyleFactory.create("GTK+"))
    if platform.system() == "Windows":
        app.setStyle(QtGui.QStyleFactory.create("Plastique"))
    mainWindows = biiGUI()
    mainWindows.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
