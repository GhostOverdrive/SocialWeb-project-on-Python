import sys
from PyQt5.QtWidgets import *
import sqlite3
from login import Ui_MainWindow_log
from reg import Ui_MainWindow_reg
from main_win import Ui_MainWindow_main
from dialog import Ui_MainWindow_dialog


class Login(QMainWindow, Ui_MainWindow_log):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Войдите')
        # пароль становиться точками
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        # подключаем все кнопки
        self.registration.clicked.connect(self.reg_window)
        self.enter.clicked.connect(self.open_main_win)

    def check_log_pas(self):
        con = sqlite3.connect("users.db")
        # получаем пароль от этого логина
        password = con.execute(f"""Select password from Users_log_password 
                                   WHERE login = '{self.login_lineEdit.text()}'""").fetchall()
        # проверяем есть ли такой пароль и совпадает ли он
        if len(password) != 0 and str(password[0][0]) == self.password_lineEdit.text():
            return True
        else:
            return False

    def open_main_win(self):
        # проверяем пароль
        if self.check_log_pas():
            # вызывается наша соц сеть
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
        # пароль точки
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        # подключение всех кнопок
        self.reg.clicked.connect(self.registration)

    def registration(self):
        con = sqlite3.connect("users.db")
        # проверяем есть ли такой логин, если есть то длинна этого списка будет 1, иначе 0
        login = con.execute(f"""Select password from Users_log_password 
                                WHERE login = '{self.mail_lineEdit.text()}'""").fetchall()
        if (self.mail_lineEdit.text() != '' and self.password_lineEdit.text() != 0 and
                self.name_lineEdit.text() != '' and self.surname_lineEdit.text() != '' and
                self.patronymic_lineEdit.text() != '' and self.datebirth_dateEdit.text() != '' and
                self.city_lineEdit.text() != '' and len(login) == 0 and
                len(self.password_lineEdit.text()) >= 6 and self.name_lineEdit.text().isalpha() and
                self.surname_lineEdit.text().isalpha() and self.patronymic_lineEdit.text().isalpha() and
                self.city_lineEdit.text().isalpha() and len(self.name_lineEdit.text()) <= 20 and
                len(self.surname_lineEdit.text()) <= 20 and len(self.patronymic_lineEdit.text()) <= 20 and
                len(self.city_lineEdit.text()) <= 20):
            # заносим в БД
            con.execute(f"""INSERT INTO Users_log_password(login, password) VALUES 
                            ('{self.mail_lineEdit.text()}', '{self.password_lineEdit.text()}')""")
            con.execute(f"""INSERT INTO Users_info(name, surname, patronymic, dateOfBirth, city) 
                            VALUES ('{self.name_lineEdit.text()}', '{self.surname_lineEdit.text()}', 
                            '{self.patronymic_lineEdit.text()}', '{self.datebirth_dateEdit.text()}', 
                            '{self.city_lineEdit.text()}')""")
            con.commit()
            self.error = QMessageBox(self)
            self.error.setText('Успешная регистрация')
            self.error.setWindowTitle('Успешно')
            self.error.exec()
            # выходит окно об успешной регистрации, после нажатия ОК, окно регистрации закроется
            self.close()
        # проверка, если длинна больше 20 символов
        elif (len(self.name_lineEdit.text()) > 20 or
              len(self.surname_lineEdit.text()) > 20 or
              len(self.patronymic_lineEdit.text()) > 20 or
              len(self.city_lineEdit.text()) > 20):
            self.error = QMessageBox(self)
            self.error.setText('Длинна имени, фамилии, отчества и города не должна превышать 20 символов!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        # если у нас не все поля заполнены
        elif not (self.mail_lineEdit.text() != '' and
                  self.password_lineEdit.text() != 0 and
                  self.name_lineEdit.text() != '' and
                  self.surname_lineEdit.text() != '' and
                  self.patronymic_lineEdit.text() != '' and
                  self.datebirth_dateEdit.text() != '' and
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
        elif (not self.name_lineEdit.text().isalpha() or
              not self.surname_lineEdit.text().isalpha() or
              not self.patronymic_lineEdit.text().isalpha() or
              not self.city_lineEdit.text().isalpha()):
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


class MainWin(QMainWindow, Ui_MainWindow_main):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('CC')
        # основное
        self.value = False
        self.value_close = False
        self.login = args[-1]
        self.con_main = sqlite3.connect("users.db")
        self.list_info = self.con_main.execute(f"""Select * from Users_info WHERE id = 
                                                   (select id from Users_log_password 
                                                   where login = '{self.login}')""").fetchall()
        self.id = self.list_info[0][0]
        self.id_users = None
        self.friends_id = self.list_info[0][6]
        self.name_str = f'{self.list_info[0][1]} {self.list_info[0][2]} {self.list_info[0][3]}'
        self.date_of_birth_str = f'{self.list_info[0][4]}'
        self.city_str = f'{self.list_info[0][5]}'
        # выводим данные на нашу страницу
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        # подключаем все кнопки
        self.my_page_btn.clicked.connect(self.my_page)
        self.friends_btn.clicked.connect(self.friends)
        self.exit_btn.clicked.connect(self.exit)
        self.add_friend_btn_2.clicked.connect(self.add_sub)
        self.del_friend_btn.clicked.connect(self.del_friend)
        self.search1_btn.clicked.connect(self.search1)
        self.search2_btn.clicked.connect(self.search2)
        self.add_friend_btn.clicked.connect(self.add_friend)
        self.go_to_page_btn_3.clicked.connect(self.go_to_page_3)
        self.go_to_page_btn_2.clicked.connect(self.go_to_page_2)
        self.go_to_page_btn.clicked.connect(self.go_to_page)
        self.add_friend_page_btn.clicked.connect(self.add_friend_page)
        self.message_btn.clicked.connect(self.dialog)
        # убираем все виджеты кроме моей страницы
        self.label_2.setVisible(False)
        self.search1_btn.setVisible(False)
        self.search1_lineEdit.setVisible(False)
        self.search1_tableWidget.setVisible(False)
        self.search2_btn.setVisible(False)
        self.search2_lineEdit.setVisible(False)
        self.my_friend_tableWidget.setVisible(False)
        self.label.setVisible(False)
        self.go_to_page_btn.setVisible(False)
        self.go_to_page_btn_2.setVisible(False)
        self.go_to_page_btn_3.setVisible(False)
        self.add_friend_btn.setVisible(False)
        self.label_5.setVisible(False)
        self.add_friend_btn_2.setVisible(False)
        self.subs_tableWidget.setVisible(False)
        self.del_friend_btn.setVisible(False)
        self.add_friend_page_btn.setVisible(False)

    def closeEvent(self, event):
        if self.value_close:
            self.exit()
        else:
            event.ignore()

    def exit(self):
        self.value_close = True
        self.login_win = Login(self)
        self.login_win.show()
        # проверка, что диалоговое окно было открыто
        if self.value:
            self.dialog_win.close()
        self.close()

    def dialog(self):
        # отбражаем нашу таблицу
        self.friends()
        # в данном окне, эта кнопка будет отвечать за сообщение
        self.del_friend_btn.setText('Написать сообщение')
        # возвращаем нашу страницу
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        # оставляем нужные
        self.del_friend_btn.setVisible(True)
        self.search2_btn.setVisible(True)
        self.search2_lineEdit.setVisible(True)
        self.my_friend_tableWidget.setVisible(True)
        self.label.setVisible(True)
        # убираем другие виджеты
        self.label_2.setVisible(False)
        self.search1_btn.setVisible(False)
        self.search1_lineEdit.setVisible(False)
        self.search1_tableWidget.setVisible(False)
        self.go_to_page_btn.setVisible(False)
        self.go_to_page_btn_2.setVisible(False)
        self.go_to_page_btn_3.setVisible(True)
        self.add_friend_btn.setVisible(False)
        self.label_5.setVisible(False)
        self.add_friend_btn_2.setVisible(False)
        self.subs_tableWidget.setVisible(False)
        self.add_friend_page_btn.setVisible(False)

    def my_page(self):
        # выставляем наши данные
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        # убираем другие виджеты
        self.label_2.setVisible(False)
        self.search1_btn.setVisible(False)
        self.search1_lineEdit.setVisible(False)
        self.search1_tableWidget.setVisible(False)
        self.search2_btn.setVisible(False)
        self.search2_lineEdit.setVisible(False)
        self.my_friend_tableWidget.setVisible(False)
        self.label.setVisible(False)
        self.go_to_page_btn.setVisible(False)
        self.go_to_page_btn_2.setVisible(False)
        self.go_to_page_btn_3.setVisible(False)
        self.add_friend_btn.setVisible(False)
        self.label_5.setVisible(False)
        self.add_friend_btn_2.setVisible(False)
        self.subs_tableWidget.setVisible(False)
        self.del_friend_btn.setVisible(False)
        self.add_friend_page_btn.setVisible(False)

    def add_friend_page(self):
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                           WHERE id = {self.id_users}""").fetchall()
        # проверка на то, что пользователь нам друг, подписчик или никто
        if self.add_friend_page_btn.text() == 'Добавить в друзья':
            self.friends_id += ' ' + str(self.id_users)
            self.con_main.execute(f"""UPDATE Users_info SET 
                                      id_friends = '{self.friends_id}' WHERE id = {self.id}""")
            self.con_main.commit()
            self.add_friend_page_btn.setText('Удалить из друзей')
        elif self.add_friend_page_btn.text() == 'Подписаться':
            self.friends_id += ' ' + str(self.id_users)
            self.con_main.execute(f"""UPDATE Users_info SET 
                                      id_friends = '{self.friends_id}' WHERE id = {self.id}""")
            self.con_main.commit()
            self.add_friend_page_btn.setText('Отписаться')
        elif self.add_friend_page_btn.text() == 'Отписаться':
            self.friends_id = self.friends_id.replace(str(self.id_users), '')
            self.con_main.execute(f"""UPDATE Users_info SET 
                                      id_friends = '{self.friends_id}' WHERE id = {self.id}""")
            self.con_main.commit()
            self.add_friend_page_btn.setText('Подписаться')
        elif self.add_friend_page_btn.text() == 'Удалить из друзей':
            self.friends_id = self.friends_id.replace(str(self.id_users), '')
            self.con_main.execute(f"""UPDATE Users_info SET 
                                      id_friends = '{self.friends_id}' WHERE id = {self.id}""")
            self.con_main.commit()
            self.add_friend_page_btn.setText('Добавить в друзья')

    def go_to_page_3(self):
        indexes = self.my_friend_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info WHERE id = 
                                        (select id from Users_log_password
                                         where id = {self.my_friend_tableWidget.item(index.row(), 0).text()})""").fetchall()
                # выставляем данные пользователя
                self.id_users = result[0][0]
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                # т. к. он у нас в друзьях, мы можем удалить его
                self.add_friend_page_btn.setText('Удалить из друзей')
                # отображаем все виджеты для страницы пользователя
                self.add_friend_page_btn.setVisible(True)
                # убираем другие виджеты
                self.label_2.setVisible(False)
                self.search1_btn.setVisible(False)
                self.search1_lineEdit.setVisible(False)
                self.search1_tableWidget.setVisible(False)
                self.search2_btn.setVisible(False)
                self.search2_lineEdit.setVisible(False)
                self.my_friend_tableWidget.setVisible(False)
                self.label.setVisible(False)
                self.go_to_page_btn.setVisible(False)
                self.go_to_page_btn_2.setVisible(False)
                self.go_to_page_btn_3.setVisible(False)
                self.add_friend_btn.setVisible(False)
                self.label_5.setVisible(False)
                self.add_friend_btn_2.setVisible(False)
                self.subs_tableWidget.setVisible(False)
                self.del_friend_btn.setVisible(False)

        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def go_to_page_2(self):
        indexes = self.search1_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info 
                                                   WHERE id = (select id from 
                                                   Users_log_password where id = 
                                                   {self.search1_tableWidget.item(index.row(), 0).text()})""").fetchall()
                # выставляем данные пользователя
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                self.id_users = result[0][0]
                # т. к. он не подписан на нас, мы можем подписаться, или отписаться
                if str(self.id_users) in self.friends_id:
                    self.add_friend_page_btn.setText('Отписаться')
                else:
                    self.add_friend_page_btn.setText('Подписаться')
                # отображаем все виджеты для страницы пользователя
                self.add_friend_page_btn.setVisible(True)
                # убираем другие виджеты
                self.label_2.setVisible(False)
                self.search1_btn.setVisible(False)
                self.search1_lineEdit.setVisible(False)
                self.search1_tableWidget.setVisible(False)
                self.search2_btn.setVisible(False)
                self.search2_lineEdit.setVisible(False)
                self.my_friend_tableWidget.setVisible(False)
                self.label.setVisible(False)
                self.go_to_page_btn.setVisible(False)
                self.go_to_page_btn_2.setVisible(False)
                self.go_to_page_btn_3.setVisible(False)
                self.add_friend_btn.setVisible(False)
                self.label_5.setVisible(False)
                self.add_friend_btn_2.setVisible(False)
                self.subs_tableWidget.setVisible(False)
                self.del_friend_btn.setVisible(False)
        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def go_to_page(self):
        indexes = self.subs_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info 
                                                   WHERE id = (select id from 
                                                   Users_log_password where id = 
                                                   {self.subs_tableWidget.item(index.row(), 0).text()})""").fetchall()
                # выставляем данные пользователя
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.id_users = result[0][0]
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                # т.к он на нас подписан, мы можем добавить его в друзья
                self.add_friend_page_btn.setText('Добавить в друзья')
                # отображаем все виджеты для страницы пользователя
                self.add_friend_page_btn.setVisible(True)
                # убираем другие виджеты
                self.label_2.setVisible(False)
                self.search1_btn.setVisible(False)
                self.search1_lineEdit.setVisible(False)
                self.search1_tableWidget.setVisible(False)
                self.search2_btn.setVisible(False)
                self.search2_lineEdit.setVisible(False)
                self.my_friend_tableWidget.setVisible(False)
                self.label.setVisible(False)
                self.go_to_page_btn.setVisible(False)
                self.go_to_page_btn_2.setVisible(False)
                self.go_to_page_btn_3.setVisible(False)
                self.add_friend_btn.setVisible(False)
                self.label_5.setVisible(False)
                self.add_friend_btn_2.setVisible(False)
                self.subs_tableWidget.setVisible(False)
                self.del_friend_btn.setVisible(False)
        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def search1(self):
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                           WHERE id != {self.id} AND (name like '{self.search1_lineEdit.text()}%' OR 
                                           surname like  '{self.search1_lineEdit.text()}%' OR 
                                           patronymic like '{self.search1_lineEdit.text()}%')""").fetchall()
        row = 0
        for i, elem in enumerate(result):
            if str(self.id) not in elem[-1]:
                row += 1
                self.search1_tableWidget.setRowCount(row)
                for j, val in enumerate(elem[:-1]):
                    self.search1_tableWidget.setItem(row - 1, j, QTableWidgetItem(str(val)))
        if row == 0:
            self.search1_tableWidget.setRowCount(0)

    def search2(self):
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                           WHERE id IN ({', '.join(self.friends_id.split())}) AND 
                                           (name like '{self.search2_lineEdit.text()}%' OR 
                                           surname like  '{self.search2_lineEdit.text()}%' OR 
                                           patronymic like '{self.search2_lineEdit.text()}%')""").fetchall()
        row = 0
        for i, elem in enumerate(result):
            if str(self.id) in elem[-1]:
                row += 1
                self.my_friend_tableWidget.setRowCount(row)
                for j, val in enumerate(elem[:-1]):
                    self.my_friend_tableWidget.setItem(row - 1, j, QTableWidgetItem(str(val)))
        if row == 0:
            self.my_friend_tableWidget.setRowCount(0)

    def add_friend(self):
        indexes = self.search1_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                if self.search1_tableWidget.item(index.row(), 0).text() not in self.friends_id:
                    self.friends_id += ' ' + self.search1_tableWidget.item(index.row(), 0).text()
                    self.con_main.execute(f"""UPDATE Users_info SET id_friends = '{self.friends_id}'
                                              WHERE id = {self.id}""")
                    self.con_main.commit()
                else:
                    self.error = QMessageBox(self)
                    self.error.setText('Вы уже подписаны на этого пользователя!')
                    self.error.setWindowTitle('Ошибка')
                    self.error.exec()
        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        self.friends()

    def add_sub(self):
        indexes = self.subs_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                self.friends_id += ' ' + self.subs_tableWidget.item(index.row(), 0).text()
                self.con_main.execute(f"""UPDATE Users_info SET id_friends = '{self.friends_id}' 
                                          WHERE id = {self.id}""")
                self.con_main.commit()
        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        self.friends()

    def del_friend(self):
        indexes = self.my_friend_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                if self.del_friend_btn.text() == 'Удалить из друзей':
                    self.friends_id = self.friends_id.replace(self.my_friend_tableWidget.item(index.row(), 0).text(),
                                                              '')
                    self.con_main.execute(f"""UPDATE Users_info SET id_friends = '{self.friends_id}' 
                                              WHERE id = {self.id}""")
                    self.con_main.commit()
                    self.friends()
                else:
                    self.dialog_win = Dialog(self, self.my_friend_tableWidget.item(index.row(), 0).text(),
                                             self.my_friend_tableWidget.item(index.row(), 1).text(),
                                             self.my_friend_tableWidget.item(index.row(), 2).text(),
                                             self.my_friend_tableWidget.item(index.row(), 3).text(),
                                             self.name_str, self.id)
                    self.value = True
                    self.dialog_win.show()
        else:
            self.error = QMessageBox(self)
            self.error.setText('Выберите полностью только 1 строку!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def friends(self):
        # исправляем последствия вкладки сообщения
        self.del_friend_btn.setText('Удалить из друзей')
        # возвращаем нашу страницу
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        # таблицы только для чтения
        self.search1_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subs_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.my_friend_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # таблица всех, кроме друзей
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                            WHERE id != {self.id} """).fetchall()
        row = 0
        for i, elem in enumerate(result):
            if str(self.id) not in elem[-1]:
                row += 1
                self.search1_tableWidget.setRowCount(row)
                for j, val in enumerate(elem[:-1]):
                    self.search1_tableWidget.setItem(row - 1, j, QTableWidgetItem(str(val)))
        if row == 0:
            self.search1_tableWidget.setRowCount(0)
        # таблица сабов
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, 
                                           id_friends from Users_info WHERE id != {self.id} and id NOT 
                                           IN ({', '.join(self.friends_id.split())})""").fetchall()
        row = 0
        for i, elem in enumerate(result):
            if str(self.id) in elem[-1]:
                row += 1
                self.subs_tableWidget.setRowCount(row)
                for j, val in enumerate(elem[:-1]):
                    self.subs_tableWidget.setItem(row - 1, j, QTableWidgetItem(str(val)))
        if row == 0:
            self.subs_tableWidget.setRowCount(0)
        # таблица друзей
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                           WHERE id IN ({', '.join(self.friends_id.split())})""").fetchall()
        row = 0
        for i, elem in enumerate(result):
            if str(self.id) in elem[-1]:
                row += 1
                self.my_friend_tableWidget.setRowCount(row)
                for j, val in enumerate(elem[:-1]):
                    self.my_friend_tableWidget.setItem(row - 1, j, QTableWidgetItem(str(val)))
        if row == 0:
            self.my_friend_tableWidget.setRowCount(0)

        # отображаем все виджеты для данной страницы
        self.label_2.setVisible(True)
        self.search1_btn.setVisible(True)
        self.search1_lineEdit.setVisible(True)
        self.search1_tableWidget.setVisible(True)
        self.search2_btn.setVisible(True)
        self.search2_lineEdit.setVisible(True)
        self.my_friend_tableWidget.setVisible(True)
        self.label.setVisible(True)
        self.go_to_page_btn.setVisible(True)
        self.go_to_page_btn_2.setVisible(True)
        self.go_to_page_btn_3.setVisible(True)
        self.add_friend_btn.setVisible(True)
        self.label_5.setVisible(True)
        self.add_friend_btn_2.setVisible(True)
        self.subs_tableWidget.setVisible(True)
        self.del_friend_btn.setVisible(True)
        # убираем другие виджеты
        self.add_friend_page_btn.setVisible(False)


class Dialog(QMainWindow, Ui_MainWindow_dialog):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Диалог')
        # основное
        self.id_user = args[1]
        self.my_id = args[-1]
        self.other = args[2:-2]
        self.name = args[-2].split()
        self.user.setText(f'{" ".join(self.other)}')
        # подключаем кнопки
        self.send_btn.clicked.connect(self.send_msg)
        # окно только для чтения
        self.dialog_plainTextEdit.setReadOnly(True)
        self.con_main = sqlite3.connect("users.db")
        result = self.con_main.execute(f"""SELECT text from Users_dialog 
                                           WHERE id = '{str(self.my_id) + ' ' + str(self.id_user)}' or 
                                           id = '{str(self.id_user) + ' ' + str(self.my_id)}'""").fetchall()
        if len(result) == 0:
            self.con_main.execute(
                f"""INSERT INTO Users_dialog VALUES ('{str(self.my_id) + ' ' + str(self.id_user)}', '')""")
            self.con_main.commit()
        else:
            self.dialog_plainTextEdit.insertPlainText(result[0][0])

    def send_msg(self):
        if self.msg_lineEdit.text() != '':
            result = self.con_main.execute(f"""SELECT text from Users_dialog 
                                                       WHERE id = '{str(self.my_id) + ' ' + str(self.id_user)}' or 
                                                       id = '{str(self.id_user) + ' ' + str(self.my_id)}'""").fetchall()
            self.dialog_plainTextEdit.insertPlainText(result[0][0])
            self.dialog_plainTextEdit.setPlainText(
                f'{self.dialog_plainTextEdit.toPlainText()}{self.name[0]}: \n    {self.msg_lineEdit.text()} \n')
            self.msg_lineEdit.setText('')
            self.con_main.execute(f"""UPDATE Users_dialog SET text = '{self.dialog_plainTextEdit.toPlainText()}' 
                                      WHERE id = '{str(self.my_id) + ' ' + str(self.id_user)}' or 
                                      id = '{str(self.id_user) + ' ' + str(self.my_id)}'""")
            self.con_main.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())