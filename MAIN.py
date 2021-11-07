
import sys
from PyQt5.uic import loadUiType
from buttonCommands import *  # files
from system_core import *


Calender.load_calender() # get latest calender data

system_remove_noshows()   # remove reservations that havent checked in and its past startdate
system_remove_notlefted()  # remove reservations that havent been checked out and its past enddate
system_remove_unpayed()   # remove sixtydays that havent payed and its pass grace period




ui,_ = loadUiType('GUI.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        title = "Ophelia's Oasis Hotel"
        self.setWindowTitle(title)

        #home page
        Buttons.reservation_home(self)

        #login page
        Buttons.login(self)

        #signup page
        Buttons.signup(self)

        #User page
        Buttons.user(self)

        #account page
        Buttons.account(self)

        #Make Reservation page
        Buttons.reservation(self)
        self.calendarWidget_indate.selectionChanged.connect(self.dateSelectIn)
        self.calendarWidget_outdate.selectionChanged.connect(self.dateSelectInOut)

        #Change reservation page
        Buttons.change(self)
        self.calendarWidget_indate_change.selectionChanged.connect(self.dateSelectIn_change)
        self.calendarWidget_outdate_change.selectionChanged.connect(self.dateSelectInOut_change)



    def dateSelectIn(self):
        date = self.calendarWidget_indate.selectedDate()
        date2 = str(date.toPyDate())
        self.label_indate.setText(date2)

    def dateSelectInOut(self):
        date = self.calendarWidget_outdate.selectedDate()
        date2 = str(date.toPyDate())
        self.label_outdate.setText(date2)

    def dateSelectIn_change(self):
        date = self.calendarWidget_indate_change.selectedDate()
        date2 = str(date.toPyDate())
        self.label_indate_change.setText(date2)

    def dateSelectInOut_change(self):
        date = self.calendarWidget_outdate_change.selectedDate()
        date2 = str(date.toPyDate())
        self.label_outdate_change.setText(date2)

    def start(self):
        print(True)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()






