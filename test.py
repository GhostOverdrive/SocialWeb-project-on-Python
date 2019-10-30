import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
from login import Ui_MainWindow_log
from reg import Ui_MainWindow_reg
from main_win import Ui_MainWindow_main


class MainWin(QMainWindow, Ui_MainWindow_main):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('CC')

        self.login = args[-1]
        con = sqlite3.connect("users.db")
        list_info = con.execute(f"""Select * from Users_info WHERE id = 
                        (select id from Users_log_password where login = '{self.login}')""").fetchall()
        self.name.setText(f'{list_info[0][1]} {list_info[0][2]} {list_info[0][3]}')


class Login(QMainWindow, Ui_MainWindow_log):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Войдите')
        # пароль становиться точками
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.registration.clicked.connect(self.reg_window)
        self.enter.clicked.connect(self.open_main_win)

    def check_log_pas(self):
        con = sqlite3.connect("users.db")
        # получаем пароль от этого логина
        password = con.execute(f"""Select password from Users_log_password 
                                   WHERE login = '{self.login_lineEdit.text()}'""").fetchall()
        # проверяем есть ли такой пароль и совпадает ли он
        if len(password) != 0 and str(
                password[0][0]) == self.password_lineEdit.text():
            return True
        else:
            return False

    def open_main_win(self):
        # проверяем пароль
        if self.check_log_pas():
            # здесь должна вызываться наша соц сеть
            self.close()
            self.main = MainWin(self, self.login_lineEdit.text())
            self.main.show()
        else:
            # окно ошибки
            self.error = QMessageBox(self)
            self.error.setText('Неверный логин или пароль!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def reg_window(self):
        # вызов окна регистрации
        self.reg = Registration(self)
        self.reg.show()


class Registration(QMainWindow, Ui_MainWindow_reg):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Регистрация')
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.reg.clicked.connect(self.registration)

    def registration(self):
        con = sqlite3.connect("users.db")
        # проверяем есть ли такой логин, если есть то длинна этого списка будет 1, иначе 0
        login = con.execute(f"""Select password from Users_log_password 
                                           WHERE login = '{self.mail_lineEdit.text()}'""").fetchall()
        # тупая проверка на пустые строки
        if (
                self.mail_lineEdit.text() != '' and self.password_lineEdit.text() != 0 and self.name_lineEdit.text() != '' and
                self.surname_lineEdit.text() != '' and self.patronymic_lineEdit.text() != '' and self.datebirth_dateEdit.text() != '' and
                self.city_lineEdit.text() != '' and len(login) == 0 and len(self.password_lineEdit.text()) >= 6 and self.name_lineEdit.text().isalpha()
                and self.surname_lineEdit.text().isalpha() and self.patronymic_lineEdit.text().isalpha() and self.city_lineEdit.text().isalpha()):
            # заносим в БД
            con.execute(f"""INSERT INTO Users_log_password(login, password) VALUES 
            ('{self.mail_lineEdit.text()}', '{self.password_lineEdit.text()}')""")
            con.execute(f"""INSERT INTO User_info(name, surname, patronymic, dateOfBirth, city) VALUES 
                    ('{self.name_lineEdit.text()}', '{self.surname_lineEdit.text()}', '{self.patronymic_lineEdit.text()}',
                    '{self.datebirth_dateEdit.text()}', '{self.city_lineEdit.text()}')""")
            con.commit()
            self.error = QMessageBox(self)
            self.error.setText('Успешная регистрация')
            self.error.setWindowTitle('Успешно')
            self.error.exec()
            # выходит окно об успешной регистрации, после нажатия ОК, окно регистрации закроется
            self.close()
        # если у нас не все поля заполнены
        elif not (self.mail_lineEdit.text() != '' and self.password_lineEdit.text() != 0 and self.name_lineEdit.text() != '' and
                self.surname_lineEdit.text() != '' and self.patronymic_lineEdit.text() != '' and self.datebirth_dateEdit.text() != '' and
                self.city_lineEdit.text() != ''):
            self.error = QMessageBox(self)
            self.error.setText('Заполните все поля!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

        # если у нас есть такой логин
        elif len(login) != 0:
            self.error = QMessageBox(self)
            self.error.setText('Такой логин уже существует!\nВведите другой')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        # проверка что в имени, фамилии, отчестве и городе только буквы
        elif (not self.name_lineEdit.text().isalpha()
                or not self.surname_lineEdit.text().isalpha() or not self.patronymic_lineEdit.text().isalpha() or not self.city_lineEdit.text().isalpha()):
            self.error = QMessageBox(self)
            self.error.setText('Для ввода имени, фамилии, отчества и города используйте только буквы!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        # проверка длинны пароля
        elif len(self.password_lineEdit.text()) < 6:
            self.error = QMessageBox(self)
            self.error.setText('Слишком короткий пароль!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
