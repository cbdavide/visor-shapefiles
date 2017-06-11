import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QLineEdit,
    QDesktopWidget, QMessageBox)

from model import Model

class CenteredWindow:
    '''
    Useful class, to get a centered window, closable at ESC key press.
    '''
    def center(self):
        '''
        Center the window in the screen.
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        '''
        Close the window when the user press ESC key.
        '''
        if e.key() == Qt.Key_Escape:
            self.close()

class Window(QWidget, CenteredWindow):

    def __init__(self, model):
        super().__init__()
        self.model = model

        self.initUI()

    def initUI(self):
        #Labels
        emailLabel = QLabel('Correo:')
        passLabel = QLabel('Contraseña')
        #Text Field
        self.emailField = QLineEdit()
        self.passField = QLineEdit()
        self.passField.setEchoMode(QLineEdit.Password)
        #Buttons
        sendButton = QPushButton('Ingresar')
        sendButton.clicked.connect(self.handler)

        #Settig up the layouts
        vbox = QVBoxLayout()

        vbox.addWidget(emailLabel)
        vbox.addWidget(self.emailField)

        vbox.addWidget(passLabel)
        vbox.addWidget(self.passField)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(sendButton)

        vbox.addSpacing(10)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(20, 20, 20, 30)

        self.setLayout(vbox)

        self.setFixedSize(300, 200)
        self.center()
        self.setWindowTitle('Iniciar Sesión')
        self.show()

    def displayError(self):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Critical)
       msg.setText("Usuario o contraseña incorrectos.")
       msg.setWindowTitle("Error de autenticación")
       msg.setStandardButtons(QMessageBox.Ok)
       msg.buttonClicked.connect(self.msgbtn)
       msg.exec_()

    def msgbtn(self):
      self.emailField.setText('')
      self.passField.setText('')

    def handler(self):
        email = self.emailField.text()
        password = self.passField.text()
        if self.model.checkUser(email, password):
            self.close()
        else:
            self.displayError()


if __name__ == '__main__':
    model = Model()
    app = QApplication(sys.argv)
    ex = Window(model)
    sys.exit(app.exec_())
