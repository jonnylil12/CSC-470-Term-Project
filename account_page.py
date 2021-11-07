from PyQt5.QtWidgets import *
from system_core import *
import re

class Account(QMainWindow):

    current_user = None

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

    def change_info(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        firstname = self.lineEdit_firstname_change.text()
        lastname = self.lineEdit_lastname_change.text()
        username = self.lineEdit_username_change.text()
        password = self.lineEdit_password_change.text()
        password_2 = self.lineEdit_password_change_2.text()
        email = (self.lineEdit_email_change.text() if self.lineEdit_email_change.text() else None)
        cc = (self.lineEdit_cc_change.text() if self.lineEdit_cc_change.text() else None)

        if not firstname:
            system_message(QMessageBox.Warning, "Please enter your first name")
        elif not lastname:
            system_message(QMessageBox.Warning, "Please enter your last name")
        elif not username:
            system_message(QMessageBox.Warning, "Please enter a username")
        elif not password:
            system_message(QMessageBox.Warning, "Please enter a password")
        elif not password_2:
            system_message(QMessageBox.Warning, "Please Retype your password")
        elif password != password_2:
            system_message(QMessageBox.Warning, "Password mismatch")

        elif username != Account.current_user.getUsername() and \
             Database.query(f"SELECT * FROM customer WHERE username == '{username}'"):
            system_message(QMessageBox.Warning, "Username already taken ")

        elif email and not re.fullmatch(regex, email):
            system_message(QMessageBox.Warning, "Please provide a valid email address")

        elif email and email != Account.current_user.getEmail() and \
                Database.query(f"SELECT * FROM customer WHERE email == '{email}'"):
            system_message(QMessageBox.Warning, "Email already taken")

        elif cc and not cc.isdigit():
            system_message(QMessageBox.Warning, "Please provide a valid credit card number")

        else:
            Account.current_user.setName(f'{firstname} {lastname}')
            Account.current_user.setEmail(email)
            Account.current_user.setUsername(username)
            Account.current_user.setPassword(password)
            Account.current_user.setCreditcard(cc)
            Database.save_object(Account.current_user)
            system_message(QMessageBox.Information, "Account Info saved")

    def back(self):
        self.page_holder.setCurrentWidget(self.user)
        self.lineEdit_firstname_change.clear()
        self.lineEdit_lastname_change.clear()
        self.lineEdit_username_change.clear()
        self.lineEdit_password_change.clear()
        self.lineEdit_password_change_2.clear()
        self.lineEdit_email_change.clear()
        self.lineEdit_cc_change.clear()
