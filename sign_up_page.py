import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from system_core  import *
import re

def message(type, text):
    msg = QMessageBox()
    msg.setIcon(type)
    msg.setWindowTitle('Ophelia\'s Oasis Hotel')
    msg.setText(text)
    msg.exec_()


class Signup(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

    def clear_text(self):
        self.lineEdit_firstname.clear()
        self.lineEdit_lastname.clear()
        self.lineEdit_username_signup.clear()
        self.lineEdit_password_signup.clear()
        self.lineEdit_password_signup_2.clear()
        self.lineEdit_email.clear()
        self.lineEdit_cc.clear()

    def validate(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        firstname = self.lineEdit_firstname.text()
        lastname = self.lineEdit_lastname.text()
        username = self.lineEdit_username_signup.text()
        password = self.lineEdit_password_signup.text()
        password_2 = self.lineEdit_password_signup_2.text()
        email = (self.lineEdit_email.text() if self.lineEdit_email.text() else None)
        cc = (self.lineEdit_cc.text() if self.lineEdit_cc.text() else None)


        if not firstname:
            message(QMessageBox.Warning,"Please enter your first name")
        elif not lastname:
            message(QMessageBox.Warning, "Please enter your last name")
        elif not username:
            message(QMessageBox.Warning, "Please enter a username")
        elif not password:
            message(QMessageBox.Warning, "Please enter a password")
        elif not password_2:
            message(QMessageBox.Warning, "Please Retype your password")
        elif password != password_2:
            message(QMessageBox.Warning, "Password mismatch")

        elif Database.query(f"SELECT * FROM customer WHERE username == '{username}'"):
            message(QMessageBox.Warning, "Username already taken ")

        elif email and not re.fullmatch(regex,email):
            message(QMessageBox.Warning, "Please provide a valid email address")

        elif email and Database.query(f"SELECT * FROM customer WHERE email == '{email}'"):
            message(QMessageBox.Warning, "Email already taken")

        elif cc and not cc.isdigit():
            message(QMessageBox.Warning, "Please provide a valid credit card number")

        else:
            Database.save_object(Customer(None,f'{firstname} {lastname}',email,username,password,cc))
            message(QMessageBox.Information, "Account Creation Success")


    def back(self):
        self.page_holder.setCurrentWidget(self.login)
        Signup.clear_text(self)


