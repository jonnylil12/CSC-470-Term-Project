import os
from make_reservation_page import *
from change_reservation_page import *
from account_page import *
from system_core import *




class User(QMainWindow):

    current_user = None
    all_reservations = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


    def cancel(self):
        reservation = User.getSelection(self.listWidget_reservations)
        if reservation:
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' " +
                                            "ORDER BY date ASC",
                                            Day)

            if reservation.getCheckedin():
                system_message(QMessageBox.Warning,"You are trying to cancel a reservation your "
                                                   "currently checked into. Try checking out instead\n")

            else:
                ans = system_message(QMessageBox.Question, "Are you sure you want to cancel your reservation?")
                if ans == QMessageBox.Yes:
                    User.confirmCancel(all_days,reservation)
                    system_load_table(self.listWidget_reservations, User.current_user)




    def checkinout(self):
        if (reservation := User.getSelection(self.listWidget_reservations)):
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' " +
                                            "ORDER BY date ASC",
                                            Day)


            if date.today() < system_str_to_date(reservation.getStartdate()):
                system_message(QMessageBox.Warning,"You are trying to check ( in / out )  of a reservation before it started.\n"
                                                  "Please wait until your startdate to try again\n")
            else:
                # user is checking in
                if not reservation.getCheckedin():
                    User.checkIn(reservation)
                    system_load_table(self.listWidget_reservations, User.current_user)

                # user is checking out
                else:
                    ans = system_message(QMessageBox.Question,"Are you sure you want to checkout?")
                    if ans == QMessageBox.Yes:
                        User.checkOut(all_days, reservation)
                        system_load_table(self.listWidget_reservations, User.current_user)



    def make_reservation(self):

        #load data for next page
        Reservations.current_user = User.current_user
        Reservations.table = self.listWidget_reservations

        # invoke next page
        self.page_holder.setCurrentWidget(self.reservation)



    def change(self):
        # load data for next page
        Modification.current_user = User.current_user
        Modification.table = self.listWidget_reservations

        if (reservation := User.getSelection(self.listWidget_reservations)):
            Modification.reservation = reservation

            # invoke next page
            self.page_holder.setCurrentWidget(self.change)



    def change_info(self):

        #load data for next page
        Account.current_user = User.current_user

        name = User.current_user.getName().split()
        self.lineEdit_firstname_change.setText(name[0])
        self.lineEdit_lastname_change.setText(name[1])
        self.lineEdit_username_change.setText(User.current_user.getUsername())
        self.lineEdit_password_change.setText(User.current_user.getPassword())
        self.lineEdit_password_change_2.setText(User.current_user.getPassword())
        self.lineEdit_email_change.setText(User.current_user.getEmail())
        self.lineEdit_cc_change.setText(str(User.current_user.getCreditcard()))

        #invoke next page
        self.page_holder.setCurrentWidget(self.userinfo)



    def logout(self):
        self.listWidget_reservations.clear()
        self.page_holder.setCurrentWidget(self.home)



    @staticmethod
    def confirmCancel(all_days,reservation):
            # get latest calender data
            Calender.load_calender()

            # user confirms
            if reservation.getType() in 'conventional,incentive':

                # charge for first day only
                if date.today() > (system_str_to_date(reservation.getStartdate()) - timedelta(days=3)):

                    [Database.delete_object(day) for day in all_days[1:]]
                    reservation.setTotalFees(all_days[0].getRate())
                    reservation.setPaydate(system_date_to_str(date.today()))

                # more than 3 days from start
                else:

                    [Database.delete_object(day) for day in all_days]
                    reservation.setTotalFees(0)

            reservation.setCheckedin(None)
            Database.save_object(reservation)

            # old calender room space is removed
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()

            system_message(QMessageBox.Information, "Cancellation Successfull")




    @staticmethod
    def checkIn(reservation):

        roomnumber = len(Database.query("SELECT * FROM reservation " +
                                        f"WHERE startdate <= '{system_date_to_str(date.today())}' " +
                                        f"AND '{system_date_to_str(date.today())}' < enddate " +
                                        "AND checkedin == True")) + 1

        reservation.setCheckedin(True)
        reservation.setRoomnumber(roomnumber)
        Database.save_object(reservation)
        system_message(QMessageBox.Information, "Checkin Successfull\n"
                                                f"Your room number is {reservation.getRoomnumber()}")



    @staticmethod
    def checkOut(all_days,reservation):
        # get latest calender data
        Calender.load_calender()

        # if user checks out early remove remaining charges
        if reservation.getType() in 'conventional,incentive':
            for day in all_days:
                if date.today() < system_str_to_date(day.getDate()):
                    Database.delete_object(day)
                    reservation.setTotalFees(reservation.getTotalFees() - day.getRate())

            reservation.setPaydate(system_date_to_str(date.today()))

        # reservation is saved
        reservation.setCheckedin(None)
        Database.save_object(reservation)

        # old calender room space is removed
        Calender.setRooms(all_days, REMOVE=True)
        Calender.save_calender()

        # make a accomodation bill
        User.generateAccomadationBill(len(all_days),User.current_user,reservation)

        system_message(QMessageBox.Information, "Checkout successfull\n"
                                                "A accommodation bill has been generated for you")








    @staticmethod
    def getSelection(table):
        selected_index = table.currentRow()
        if selected_index < 0:
            system_message(QMessageBox.Warning,"Please select a reservation")
        elif not selected_index:
            pass
        else:
            ID = table.currentItem().text().split()[0]
            return Database.load_object("SELECT * FROM reservation "  +
                                        f"WHERE ID == '{ID}'"
                                        ,Reservation)[0]
        return None



    @staticmethod
    def generateAccomadationBill(totalnights,current_user,reservation):

        os.makedirs(os.path.dirname("accommodation_bills\\_.txt"), exist_ok=True)
        filepath = f"{os.path.abspath('accommodation_bills')}\\{current_user.getID()}"

        with open(f"{filepath}.txt", "w") as output_file:
            bill = "                  Ophelia's Oasis Hotel\n" + \
                   "Thank you for stay we hope you had the best experience and will see you again" + \
                   "\n\n" + \
                   f"Todays date:     {system_date_to_str(date.today())}\n" + \
                   f"Name:            {current_user.getName()}\n" + \
                   f"Room number:     {reservation.getRoomnumber()}\n" + \
                   f"Start date:      {reservation.getStartdate()}\n" + \
                   f"Departure date:  {reservation.getEnddate()}\n" + \
                   f"Total nights:    {totalnights}\n" + \
                   f"Total charge:    ${reservation.getTotalFees():,.2f}\n"

            if reservation.getType() in 'prepaid,sixtyday':
                bill += f"Payment date:    {reservation.getPaydate()}"

            output_file.write(bill)



