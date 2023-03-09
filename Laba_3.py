from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from encryption import encryption, publicKey, data_verification
import TkCheckers


# Класс отвечающий за стартовое окно
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(lambda: self.personal_ac())
        self.registration_btn.clicked.connect(lambda: self.registration())

    def registration(self):
        self.login.setText('')
        self.password.setText('')
        widget.setCurrentWidget(registration_window)

    def personal_ac(self):
        username = self.login.text().strip()
        password = self.password.text().strip()
        data_user = username + password
        if username != '' and password != '' and encryption(data_user, publicKey, 'авторизация'):
            self.close()
            TkCheckers.run()
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Введен неверный логин или пароль.")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()


# Класс отвечающий за окно регистрации
class Registration(QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("registration.ui", self)

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_btn.clicked.connect(lambda: self.ac_window())
        self.back_btn.clicked.connect(lambda: self.login_window())

    def login_window(self):
        self.login.setText('')
        self.password.setText('')
        self.password_2.setText('')
        return widget.setCurrentWidget(login_window)

    def ac_window(self):
        username = self.login.text().strip()
        password = self.password.text().strip()
        password_2 = self.password_2.text().strip()
        if password != password_2:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Пароли не совпадают!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
        else:
            if not data_verification(username, password):
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Введены неверный данные!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
            else:
                self.close()
                TkCheckers.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    registration_window = Registration()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(login_window)
    widget.addWidget(registration_window)
    widget.show()
    sys.exit(app.exec_())