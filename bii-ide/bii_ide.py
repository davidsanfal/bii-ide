import sys
from PyQt4 import QtGui
from bii_ide.gui.biigui_main_window import biiGUI


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("GTK+"))
    mainWindows = biiGUI()
    mainWindows.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
