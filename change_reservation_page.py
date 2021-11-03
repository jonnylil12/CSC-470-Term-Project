from system_core import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

Calender.load_calender()

class Modification(QMainWindow):

    current_user = None
    reservation = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    def clear_text_change(self):
        self.label_indate_change.setText('Selected Date')
        self.label_outdate_change.setText('Selected Date')



    def change(self):

        startdate = self.label_indate.text()
        enddate = self.label_outdate.text()
        all_days = Database.load_object("SELECT * FROM day " +
                                        f"WHERE reservation_ID = '{Modification.reservation.getID()}' " +
                                        "ORDER BY date ASC",
                                        Day)

        Modification.reservation.setStartdate(startdate)
        Modification.reservation.setEnddate(enddate)

        if not Modification.reservation:
            print("SYSTEM ERROR you have no active reservations\n")

        elif Modification.reservation.getCheckedin():
            print("SYSTEM ERROR your trying to change a reservation your currently checked into.\n"
                  "Try checking out instead\n")

        elif system_str_to_date(startdate) >= system_str_to_date(enddate):
            print("SYSTEM ERROR startdate must be less than enddate")

        elif date.today() > system_str_to_date(startdate):
            print("SYSTEM ERROR you cannot make a reservation starting in the past")

        elif not Calender.rooms_are_avaliable(startdate, enddate):
            print("SYSTEM ERROR there are no rooms avaliable for that entire period")

        elif not Modification.reservation.is_valid(Modification.user):
            print("SYSTEM ERROR reservation is not valid and cannot be changed")

        else:
            self.confirmChange(all_days)



    def back(self):
        Modification.clear_text_change(self)
        self.page_holder.setCurrentWidget(self.user)





    def confirmChange(self,all_days):


            # generate charges and room space
            if Modification.reservation.getType() in 'conventional,incentive':
                [Database.delete_object(day) for day in all_days]
                new_days, totalfees = system_generate_days(Modification.reservation)

            else:
                new_days, totalfees = system_generate_days(Modification.reservation, True)

                # issuse refund if new amount is greater than old
                if totalfees >= Modification.reservation.getTotalFees():
                    [Database.delete_object(day) for day in all_days]

            # old calender room space is removed
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()



            # charges are saved
            [Database.save_object(day) for day in new_days]

            # reservation is saved
            Modification.reservation.setTotalFees(totalfees)
            Database.save_object(Modification.reservation)

            # calender room space is added
            Calender.setRooms(new_days, REMOVE=False)
            Calender.save_calender()

            # show charges
            print(Modification.reservation.getTotalFees())


