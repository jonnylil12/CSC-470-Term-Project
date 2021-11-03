import sys
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from login_page import *
from sign_up_page import *
from user_page import *
from make_reservation_page import *
from change_reservation_page import *

class Buttons(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    def reservation_home(self):
        self.btn_home.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.login))

    def login(self):
        self.btn_signup.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.signup))
        self.btn_login.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.user))

        # self.btn_login.clicked.connect(lambda: Login.load_reservations(self))
        # self.btn_login.clicked.connect(lambda: Login.validate(self))

    def signup(self):
        self.btn_back_login.clicked.connect(lambda: Signup.back(self))
        # self.btn_signup_confirm.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.login))
        self.btn_signup_confirm.clicked.connect(lambda: Signup.validate(self))

    def user(self):
        self.btn_logout.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.home))
        #self.btn_logout.clicked.connect(lambda: lambda: User.logout(self))

        self.btn_account.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.userinfo))
        self.btn_reservation.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.reservation))

        self.btn_change.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.change))
        #self.btn_change.clicked.connect(lambda: Modification.change(self))

        self.btn_cancel.clicked.connect(lambda: User.cancel(self))

        #self.btn_checkin.clicked.connect(lambda: User.checkinout(self))

    def reservation(self):
        self.btn_back_user.clicked.connect(lambda: Reservation.back(self))
        #self.btn_reservation_confirm.clicked.connect(lambda: Reservation.reserve(self))

    def change(self):
        self.btn_back_user_2.clicked.connect(lambda: Modification.back(self))
        #self.btn_change_confirm.clicked.connect(lambda: Reservation.change(self))

    def account(self):
        self.btn_back_user_3.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.user))
        self.btn_modify.clicked.connect(lambda: self.page_holder.setCurrentWidget(self.user))
        #self.btn_signup_confirm.clicked.connect(lambda: Account.change_info(self))