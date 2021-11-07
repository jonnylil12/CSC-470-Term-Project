from PyQt5.QtWidgets import *
from user_page import User
from system_core import *



class Login(QMainWindow):
    current_user = None
    all_reservations = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if not username:
            system_message(QMessageBox.Warning, "Please enter a username")
        elif not password:
            system_message(QMessageBox.Warning, "Please enter a password")
        elif not Database.query(f"SELECT * FROM customer WHERE (username,password) == ('{username}','{password}') "):
            system_message(QMessageBox.Warning, "Invalid username or password")

        else:

            # load data for next page
            User.current_user = Database.load_object("SELECT * FROM customer " +
                                                f"WHERE username == '{username}'",
                                                Customer)[0]

            self.label_welcome.setText(f'Welcome {User.current_user.getName()}')
            system_load_table(self.listWidget_reservations , User.current_user)

            # invoke next page
            self.page_holder.setCurrentWidget(self.user)
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()


    def sign_up(self):
        self.page_holder.setCurrentWidget(self.signup)
        self.lineEdit_username.clear()
        self.lineEdit_password.clear()


