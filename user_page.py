from system_core import *
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from make_reservation_page import *
from change_reservation_page import *

# get latest calender data
Calender.load_calender()

class User(QMainWindow):

    current_user = None
    reservation = None


    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # query all reservations tied to customer and displays them
        all_reservations = Database.load_object("SELECT * FROM reservation " +
                                                f"WHERE customer_ID == '{User.current_user.getID()}' " +
                                                "AND checkedin IS NOT NULL"
                                                , Reservation)

    def clear_text(self):
        self.listWidget_reservations.clear()

        self.lineEdit_firstname_change.clear()
        self.lineEdit_lastname_change.clear()
        self.lineEdit_username_change.clear()
        self.lineEdit_password_change.clear()
        self.lineEdit_password_change_2.clear()
        self.lineEdit_email_change.clear()
        self.lineEdit_cc_change.clear()

        Reservation.clear_text(self)
        Modification.clear_text_change(self)



    def cancel(self):
        all_days = Database.load_object("SELECT * FROM day " +
                                        f"WHERE reservation_ID = '{User.reservation.getID()}' " +
                                        "ORDER BY date ASC",
                                        Day)

        if not User.reservation:
            print("SYSTEM ERROR you have no active reservations\n")


        elif User.reservation.getCheckedin():
            print("SYSTEM ERROR your trying to cancel a reservation your currently checked into.\n"
                  "Try checking out instead\n")

        else:

            self.confirmCancel(all_days)



    def checkinout(self):
        all_days = Database.load_object("SELECT * FROM day " +
                                        f"WHERE reservation_ID = '{User.reservation.getID()}' " +
                                        "ORDER BY date ASC",
                                        Day)

        if not User.reservation:
            print("SYSTEM ERROR you have no active reservations \n")

        elif date.today() < system_str_to_date(User.reservation.getStartdate()):
            print("SYSTEM ERROR you are trying to check ( in / out )  of a reservation before it started.\n"
                  "Please wait until your startdate to try again\n")

        else:

            # user is checking in
            if not User.reservation.getCheckedin():
                self.checkIn()

            # user is checking out
            else:
                self.checkOut(all_days)

            # alert user of successfull check in / out








    def confirmCancel(self,all_days):

            # user confirms
            if User.reservation.getType() in 'conventional,incentive':

                # charge for first day only
                if date.today() > (system_str_to_date(User.reservation.getStartdate()) - timedelta(days=3)):

                    [Database.delete_object(day) for day in all_days[1:]]
                    User.reservation.setTotalFees(all_days[0].getRate())
                    User.reservation.setPaydate(system_date_to_str(date.today()))

                # more than 3 days from start
                else:

                    [Database.delete_object(day) for day in all_days]
                    User.reservation.setTotalFees(0)

            User.reservation.setCheckedin(None)
            Database.save_object(User.reservation)

            # old calender room space is removed
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()

        # alert user of successfull cancelation






    def checkIn(self):

        roomnumber = len(Database.query("SELECT * FROM reservation " +
                                        f"WHERE startdate <= '{system_date_to_str(date.today())}' " +
                                        f"AND '{system_date_to_str(date.today())}' < enddate " +
                                        "AND checkedin == True")) + 1

        User.reservation.setCheckedin(True)
        User.reservation.setRoomnumber(roomnumber)
        Database.save_object(User.reservation)





    def checkOut(self,all_days):
        # if user checks out early remove remaining charges
        if User.reservation.getType() in 'conventional,incentive':
            for day in all_days:
                if date.today() < system_str_to_date(day.getDate()):
                    Database.delete_object(day)
                    User.reservation.setTotalFees(User.reservation.getTotalFees() - day.getRate())

            User.reservation.setPaydate(system_date_to_str(date.today()))

        # reservation is saved
        User.reservation.setCheckedin(None)
        Database.save_object(User.reservation)

        # old calender room space is removed
        Calender.setRooms(all_days, REMOVE=True)
        Calender.save_calender()

        # make a accomodation bill
        self.generateAccomadationBill(len(all_days))



    def generateAccomadationBill(self,totalnights):

        os.makedirs(os.path.dirname("accommodation_bills\\_.txt"), exist_ok=True)
        filepath = f"{os.path.abspath('accommodation_bills')}\\{User.current_user.getID()}"


        with open(f"{filepath}.txt", "w") as output_file:

            bill =  "                  Ophelia's Oasis Hotel\n" + \
                    "Thank you for stay we hope you had the best experience and will see you again"+ \
                    "\n\n"+ \
                    f"Todays date:     {system_date_to_str(date.today())}\n"+ \
                    f"Name:            {User.current_user.getName()}\n"+ \
                    f"Room number:     {User.reservation.getRoomnumber()}\n"+ \
                    f"Start date:      {User.reservation.getStartdate()}\n"+ \
                    f"Departure date:  {User.eservation.getEnddate()}\n"+ \
                    f"Total nights:    {totalnights}\n"+ \
                    f"Total charge:    ${User.reservation.getTotalFees():,.2f}\n"


            if User.reservation.getType() in 'prepaid,sixtyday':
                    bill += f"Payment date:    {User.reservation.getPaydate()}"

            output_file.write(bill)

