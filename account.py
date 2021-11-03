import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Account(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

    def change_info(self):
        firstname = self.lineEdit_firstname_change.text()
        lastname = self.lineEdit_lastname_change.text()
        username = self.lineEdit_username_change.text()
        password = self.lineEdit_password_change.text()
        password_2 = self.lineEdit_password_change_2.text()
        email = self.lineEdit_email_change.text()
        cc = self.lineEdit_cc_change.text()

        self.page_holder.setCurrentWidget(self.user)