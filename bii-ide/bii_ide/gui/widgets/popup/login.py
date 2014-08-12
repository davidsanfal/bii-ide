from PyQt4 import QtGui
from biicode.common.model.brl.brl_user import BRLUser
from biicode.common.exception import InvalidNameException


class BiiLogin(QtGui.QDialog):
    def __init__(self, username=None):
        QtGui.QDialog.__init__(self)
        self.username = username
        self.password = ""
        title_font = QtGui.QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        text_username = QtGui.QLabel("User name: ")
        text_username.setFont(title_font)
        text_password = QtGui.QLabel("Password: ")
        text_password.setFont(title_font)
        if self.username:
            self.textName = QtGui.QLabel(self.username)
            self.textName.setFont(title_font)
        else:
            self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        grid = QtGui.QGridLayout()
        grid.addWidget(text_username, 0, 0)
        grid.addWidget(self.textName, 0, 1)
        grid.addWidget(text_password, 1, 0)
        grid.addWidget(self.textPass, 1, 1)
        grid.addWidget(self.buttonLogin, 2, 0, 1, 2)
        self.setLayout(grid)

    def handleLogin(self):
        if (self.textName.text() and self.textPass.text()):
            try:
                self.username = BRLUser(str(self.textName.text()))
                self.password = str(self.textPass.text())
                self.close()
            except InvalidNameException:
                QtGui.QMessageBox.warning(self, 'Error', 'Bad user name')
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Insert user name and password')
