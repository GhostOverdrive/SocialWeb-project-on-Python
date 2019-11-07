import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
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
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.registration.clicked.connect(self.reg_window)
        self.enter.clicked.connect(self.open_main_win)

    def check_log_pas(self):
        """
        Проверка правильности логина и пароля
        :return: bool
        """
        con = sqlite3.connect("info\\users.db")
        password = con.execute(f"""Select password from Users_log_password 
                                   WHERE login = '{self.login_lineEdit.text()}'""").fetchall()
        if len(password) != 0 and str(password[0][0]) == self.password_lineEdit.text():
            return True
        else:
            return False

    def open_main_win(self):
        """
        Открывает основное окно если логин и пароль введены верно
        Открывает диалоговое окно если логин и пароль введны не верно
        """
        if self.check_log_pas():
            self.close()
            self.main = MainWin(self, self.login_lineEdit.text())
            self.main.show()
        else:
            self.error = QMessageBox(self)
            self.error.setText('Неверный логин или пароль!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()

    def reg_window(self):
        """
        Откртие окна регистрации
        """
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
        """
        Проверка правильности введеных данных при регистрации
        И сохранение все в базе данных SQL
        """
        con = sqlite3.connect("info\\users.db")
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
                len(self.city_lineEdit.text()) <= 20 and len(self.mail_lineEdit.text()) <= 255 and
                len(self.password_lineEdit.text()) <= 255):
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
            self.close()
        elif (len(self.name_lineEdit.text()) > 20 or
              len(self.surname_lineEdit.text()) > 20 or
              len(self.patronymic_lineEdit.text()) > 20 or
              len(self.city_lineEdit.text()) > 20):
            self.error = QMessageBox(self)
            self.error.setText('Длинна имени, фамилии, отчества и города не должна превышать 20 символов!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        elif (len(self.mail_lineEdit.text()) > 255 or
              len(self.password_lineEdit.text()) > 255):
            self.error = QMessageBox(self)
            self.error.setText('Длинна логина и пароля не должна превышать 255 символов!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
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
        elif len(login) != 0:
            self.error = QMessageBox(self)
            self.error.setText('Такой логин уже существует!\nВведите другой')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        elif (not self.name_lineEdit.text().isalpha() or
              not self.surname_lineEdit.text().isalpha() or
              not self.patronymic_lineEdit.text().isalpha() or
              not self.city_lineEdit.text().isalpha()):
            self.error = QMessageBox(self)
            self.error.setText('Для ввода имени, фамилии, отчества и города используйте только буквы!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()
        elif len(self.password_lineEdit.text()) < 6:
            self.error = QMessageBox(self)
            self.error.setText('Слишком короткий пароль!')
            self.error.setWindowTitle('Ошибка')
            self.error.exec()


class MainWin(QMainWindow, Ui_MainWindow_main):
    def __init__(self, *args):
        """
        Иницилизация всех переменных
        :param args: login_user
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('NAPRIA')
        self.value = False
        self.value_close = False
        self.login = args[-1]
        self.con_main = sqlite3.connect("info\\users.db")
        self.list_info = self.con_main.execute(f"""Select * from Users_info WHERE id = 
                                                   (select id from Users_log_password 
                                                   where login = '{self.login}')""").fetchall()
        self.id = self.list_info[0][0]
        self.id_users = None
        self.friends_id = self.list_info[0][6]
        self.name_str = f'{self.list_info[0][1]} {self.list_info[0][2]} {self.list_info[0][3]}'
        self.date_of_birth_str = f'{self.list_info[0][4]}'
        self.city_str = f'{self.list_info[0][5]}'
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
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
        """
        Отключение стандартной кнопки выхода
        Функция выхода сообщается кнопке "Выход" в программе
        """
        if self.value_close:
            self.exit()
        else:
            event.ignore()

    def exit(self):
        """
        Закрывает все окна, которые были открыты
        И открывает окно входа
        """
        self.value_close = True
        self.login_win = Login(self)
        self.login_win.show()
        if self.value:
            self.dialog_win.close()
        self.close()

    def dialog(self):
        """
        Отображаем виджеты, которые нужны нам для вкладки "Диалоги"
        Возваращаем данные о себе, если они были изменены, после посещения другого пользователя
        Отображаем всех друзей из базы данных, с котормы можем начать диалог
        """
        self.friends()
        self.del_friend_btn.setText('Написать сообщение')
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        self.del_friend_btn.setVisible(True)
        self.search2_btn.setVisible(True)
        self.search2_lineEdit.setVisible(True)
        self.my_friend_tableWidget.setVisible(True)
        self.label.setVisible(True)
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
        """
        Отображаем виджеты, которые нужны нам для вкладки "Моя страница"
        Возваращаем данные о себе, если они были изменены, после посещения другого пользователя
        """
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
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
        """
        Функция, отвечающая за подписку/отписку/добавление/удаление на какого-либо пользователя,
        когда находишься на его странице
        И предотвращение повторной подписки
        """
        result = self.con_main.execute(f"""Select id, name, surname, patronymic, id_friends from Users_info 
                                           WHERE id = {self.id_users}""").fetchall()
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
        """
        Проверяем, выделена ли вся строка таблицы
        Открываем страницу выбранного друга и заносим данные о нем
        """
        indexes = self.my_friend_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info WHERE id = 
                                    (select id from Users_log_password
                                     where id = {self.my_friend_tableWidget.item(index.row(), 0).text()})""").fetchall()
                self.id_users = result[0][0]
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                self.add_friend_page_btn.setText('Удалить из друзей')
                self.add_friend_page_btn.setVisible(True)
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
        """
        Проверяем, выделена ли вся строка таблицы
        Открываем страницу выбранного пользователя и заносим данные о нем
        """
        indexes = self.search1_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info 
                                                WHERE id = (select id from 
                                                Users_log_password where id = 
                                                {self.search1_tableWidget.item(index.row(), 0).text()})""").fetchall()
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                self.id_users = result[0][0]
                if str(self.id_users) in self.friends_id:
                    self.add_friend_page_btn.setText('Отписаться')
                else:
                    self.add_friend_page_btn.setText('Подписаться')
                self.add_friend_page_btn.setVisible(True)
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
        """
        Проверяем, выделена ли вся строка таблицы
        Открываем страницу выбранного подписчика и заносим данные о нем
        """
        indexes = self.subs_tableWidget.selectionModel().selectedRows()
        if len(indexes) == 1:
            for index in sorted(indexes):
                result = self.con_main.execute(f"""Select * from Users_info 
                                                   WHERE id = (select id from 
                                                   Users_log_password where id = 
                                                   {self.subs_tableWidget.item(index.row(), 0).text()})""").fetchall()
                self.name.setText(f'{result[0][1]} {result[0][2]} {result[0][3]}')
                self.id_users = result[0][0]
                self.dateOfbirth.setText(f'{result[0][4]}')
                self.city.setText(f'{result[0][5]}')
                self.add_friend_page_btn.setText('Добавить в друзья')
                self.add_friend_page_btn.setVisible(True)
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
        """
        Поиск пользователя по имени, фамилии или отчеству
        И отображение в таблице
        """
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
        """
        Поиск пользователя по имени, фамилии или отчеству
        И отображение в таблице
        """
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
        """
        Подписка на выбранного пользователя
        """
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
        """
        Добавление в друзья выбранного подписчика
        """
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
        """
        Если название кнопки "Удалить из друзей", то она отвечает за удаления выбранного пользователя из друзей
        Если название кнопки "Написать сообщение", то она отвечает за открытие диалогового окна с выбранным
        другом
        """
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
        """
        Отображение всех таблиц: друзей, всех пользователей, подписчиков
        И восстановление данных о себе
        """
        self.del_friend_btn.setText('Удалить из друзей')
        self.name.setText(self.name_str)
        self.dateOfbirth.setText(self.date_of_birth_str)
        self.city.setText(self.city_str)
        self.search1_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subs_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.my_friend_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        self.add_friend_page_btn.setVisible(False)


class Dialog(QMainWindow, Ui_MainWindow_dialog):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Диалог')
        self.id_user = args[1]
        self.my_id = args[-1]
        self.other = args[2:-2]
        self.name = args[-2].split()
        self.user.setText(f'{" ".join(self.other)}')
        self.send_btn.clicked.connect(self.send_msg)
        self.msg_lineEdit.textEdited.connect(self.update_msg)
        self.dialog_plainTextEdit.setReadOnly(True)
        self.con_main = sqlite3.connect("info\\users.db")
        result = self.con_main.execute(f"""SELECT text from Users_dialog  
                                           WHERE id = '{str(self.my_id) + "_" + str(self.id_user)}' or 
                                           id = '{str(self.id_user) + "_" + str(self.my_id)}'""").fetchall()
        if len(result) == 0:
            self.name_file = f'info\\dialog_{str(self.my_id) + "_" + str(self.id_user)}.txt'
            self.f = open(self.name_file, 'w')
            self.con_main.execute(
                f"""INSERT INTO Users_dialog VALUES 
                ('{str(self.my_id) + "_" + str(self.id_user)}', '{self.name_file}')""")
            self.con_main.commit()
        else:
            self.name_file = result[0][0]
            self.f = open(self.name_file)
            text = self.f.read()
            self.dialog_plainTextEdit.setPlainText(text)

    def update_msg(self):
        """
        Обновление диалога, если текст в строке не равен пустой строке, то есть когда начался ввод сообщения
        """
        if self.msg_lineEdit.text() != '':
            self.f = open(self.name_file)
            text = self.f.read()
            self.dialog_plainTextEdit.setPlainText(f'{text}')
            self.dialog_plainTextEdit.verticalScrollBar().setValue(
                self.dialog_plainTextEdit.verticalScrollBar().maximum())

    def keyPressEvent(self, event):
        """
        При нажатии клавиш "Enter" отправка сообщения
        """
        if event.key() == Qt.Key_Enter or event.key() == 16777220:
            self.send_msg()

    def send_msg(self):
        """
        Отправка сообщения
        """
        if self.msg_lineEdit.text() != '':
            self.f = open(self.name_file)
            text = self.f.read()
            self.f = open(self.name_file, 'w')
            all_msg = f'{text}{self.name[0]}: \n    {self.msg_lineEdit.text()} \n'
            self.dialog_plainTextEdit.setPlainText(all_msg)
            self.f.write(all_msg)
            self.f.close()
            self.dialog_plainTextEdit.verticalScrollBar().setValue(
                self.dialog_plainTextEdit.verticalScrollBar().maximum())
            self.msg_lineEdit.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
