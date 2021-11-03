from system_core import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Calender.load_calender()

class Reservation(QMainWindow):

    current_user = None
    reservation = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    def clear_text(self):
        self.label_indate.setText('Selected Date')
        self.label_outdate.setText('Selected Date')
        #self.currentText()

    def reserve(self):

        Type = self.comboBox_types.currentText()
        startdate = self.label_indate.text()
        enddate = self.label_outdate.text()

        if Type == 'prepaid':
            reservation = Prepaid(None, Reservation.user.getID(), startdate, enddate, None, False, None, Type,
                                                                                system_date_to_str(date.today()))
        elif Type == 'sixtyday':
            reservation = Sixtyday(None, Reservation.user.getID(), startdate, enddate, None, False, None, Type, None)
        elif Type == 'conventional':
            reservation = Prepaid(None, Reservation.user.getID(), startdate, enddate, None, False, None, Type, None)
        elif Type == 'incentive':
            reservation = Prepaid(None, Reservation.user.getID(), startdate, enddate, None, False, None, Type, None)

        if system_str_to_date(startdate) >= system_str_to_date(enddate):
            print("SYSTEM ERROR startdate must be less than enddate")

        elif date.today() > system_str_to_date(startdate):
            print("SYSTEM ERROR you cannot make a reservation starting in the past")

        elif not Calender.rooms_are_avaliable(startdate, enddate):
            print("SYSTEM ERROR there are no rooms avaliable for that entire period")

        elif not Reservation.reservation.is_valid(Reservation.user):
            print("SYSTEM ERROR reservation is not valid and cannot be made")

        else:
            self.confirmMake()



    def back(self):
        Reservation.clear_text(self)
        self.page_holder.setCurrentWidget(self.user)
        type = self.comboBox_types.currentText()
        print(str(type))
        self.comboBox_types.setCurrentIndex(0)



    def confirmMake(self):
            # generate charges and room space
            Database.save_object(Reservation.reservation)

            all_days, totalfees = system_generate_days(Reservation.reservation)

            # charges are saved
            [Database.save_object(day) for day in all_days]

            # reservation is saved
            Reservation.reservation.setTotalFees(totalfees)
            Database.save_object(Reservation.reservation)

            # calender room space is added
            Calender.setRooms(all_days, REMOVE=False)
            Calender.save_calender()

            # show charges
            print(Reservation.reservation.getTotalFees())

            # alert user of successfull creation







