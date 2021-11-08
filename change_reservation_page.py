from system_core import *
from PyQt5.QtWidgets import *

Calender.load_calender()

class Modification(QMainWindow):

    current_user = None
    table = None
    reservation = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


    def change(self):
        # get latest calender data
        Calender.load_calender()

        Type = Modification.reservation.getType()
        startdate = self.label_indate_change.text()
        enddate = self.label_outdate_change.text()

        if startdate and enddate:
            startdate = startdate[5:] + '-' + startdate[2:4]
            enddate = enddate[5:] + '-' + enddate[2:4]

            Modification.reservation.setStartdate(startdate)
            Modification.reservation.setEnddate(enddate)

            R = None
            if Type == 'prepaid':
                R = Prepaid(*Modification.reservation.__dict__.values())
            elif Type == 'sixtyday':
                R = Sixtyday(*Modification.reservation.__dict__.values())
            elif Type == 'conventional':
                R = Conventional(*Modification.reservation.__dict__.values())
            elif Type == 'incentive':
                R = Incentive(*Modification.reservation.__dict__.values())

            if R.getCheckedin():
                system_message(QMessageBox.Warning,"You are trying to change a reservation your currently checked into.\n"
                                                   "Try checking out instead")

            elif system_str_to_date(startdate) >= system_str_to_date(enddate):
                system_message(QMessageBox.Warning,"Startdate must be before  enddate")

            elif date.today() > system_str_to_date(startdate):
                system_message(QMessageBox.Warning,"You cannot make a reservation starting in the past")

            elif not Calender.rooms_are_avaliable(startdate, enddate):
                system_message(QMessageBox.Warning,"There are no rooms avaliable for that time period")

            elif not R.is_valid(Modification.current_user):
                system_message(QMessageBox.Warning,"Reservation is not valid and cannot be changed")

            else:
                Modification.confirmChange(R)



    def back(self):
        self.page_holder.setCurrentWidget(self.user)
        self.label_indate_change.setText('')
        self.label_outdate_change.setText('')




    @staticmethod
    def confirmChange(reservation):
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' " +
                                            "ORDER BY date ASC",
                                            Day)
            # get latest calender data
            Calender.load_calender()

            # generate charges and room space
            if reservation.getType() in 'conventional,incentive':
                [Database.delete_object(day) for day in all_days]
                new_days, totalfees = system_generate_days(reservation)

            else:
                new_days, totalfees = system_generate_days(reservation, True)

                # issuse refund if new amount is greater than old
                if totalfees >= reservation.getTotalFees():
                    [Database.delete_object(day) for day in all_days]

            # old calender room space is removed
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()

            # charges are saved
            [Database.save_object(day) for day in new_days]

            # reservation is saved
            reservation.setTotalFees(totalfees)
            Database.save_object(reservation)

            # calender room space is added
            Calender.setRooms(new_days, REMOVE=False)
            Calender.save_calender()


            # show charges
            system_message(QMessageBox.Information, "Modification succesfully saved\n"
                                                    f"Your total fees are ${reservation.getTotalFees()}")

            system_load_table(Modification.table, Modification.current_user)




