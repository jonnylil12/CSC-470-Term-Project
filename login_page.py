from system_core import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Calender.load_calender()


class Login(QMainWindow):

    current_user = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    def clear_text(self):
        self.lineEdit_username.clear()
        self.lineEdit_password.clear()

    def validate(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        self.label_welcome.setText(f'Welcome {username}')
        Login.clear_text(self)

        Login.current_user = Database.load_object("SELECT * FROM customer " +
                                                  f"WHERE username = '{username}'"
                                                  , Customer)[0]

        #Write code here for putting the reservations into the list widget

        #Write code here for loading their account info into the account fields
        self.lineEdit_firstname_change.setText()
        self.lineEdit_lastname_change.setText()
        self.lineEdit_username_change.setText()
        self.lineEdit_password_change.setText()
        self.lineEdit_password_change_2.setText()
        self.lineEdit_email_change.setText()
        self.lineEdit_cc_change.setText()

        self.page_holder.setCurrentWidget(self.user)


    def modify(self):
        firstname = self.lineEdit_firstname_change.text()
        lastname = self.lineEdit_lastname_change.text()
        username = self.lineEdit_username_change.text()
        password = self.lineEdit_password_change.text()
        password_2 = self.lineEdit_password_change_2.text()
        email = self.lineEdit_email_change.text()
        cc = self.lineEdit_cc_change.text()