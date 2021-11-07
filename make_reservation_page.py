from PyQt5.QtWidgets import *
from system_core import *


class Reservations(QMainWindow):

    current_user = None
    table = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    def reserve(self):

        Type = self.comboBox_types.currentText()
        startdate = self.label_indate.text()
        enddate = self.label_outdate.text()

        if startdate and enddate:
            startdate = startdate[5:] + '-' + startdate[2:4]
            enddate = enddate[5:] + '-' + enddate[2:4]

            R = None
            if Type == 'prepaid':
                R = Prepaid(None, Reservations.current_user.getID(), startdate, enddate, None, False, None, Type,
                                                                                    system_date_to_str(date.today()))
            elif Type == 'sixtyday':
                R = Sixtyday(None, Reservations.current_user.getID(), startdate, enddate, None, False, None, Type, None)
            elif Type == 'conventional':
                R = Conventional(None, Reservations.current_user.getID(), startdate, enddate, None, False, None, Type, None)
            elif Type == 'incentive':
                R = Incentive(None, Reservations.current_user.getID(), startdate, enddate, None, False, None, Type, None)

            if system_str_to_date(startdate) >= system_str_to_date(enddate):
                system_message(QMessageBox.Warning, "Startdate must be before enddate")

            elif date.today() > system_str_to_date(startdate):
                system_message(QMessageBox.Warning, "You cannot make a reservation starting in the past")

            elif not Calender.rooms_are_avaliable(startdate, enddate):
                system_message(QMessageBox.Warning, "Sorry but there are no rooms avaliable for that entire period")

            elif not R.is_valid(Reservations.current_user):
                system_message(QMessageBox.Warning, "Reservation is not valid and cannot be made")
            else:
                Reservations.confirmMake(R)



    def back(self):
        self.page_holder.setCurrentWidget(self.user)
        self.label_indate.setText('')
        self.label_outdate.setText('')
        self.comboBox_types.setCurrentIndex(0)


    @staticmethod
    def confirmMake(reservation):

        # get latest calender data
        Calender.load_calender()

        # generate charges and room space
        Database.save_object(reservation)
        all_days, totalfees = system_generate_days(reservation)

        # charges are saved
        [Database.save_object(day) for day in all_days]

        # reservation is saved
        reservation.setTotalFees(totalfees)
        Database.save_object(reservation)

        # calender room space is added
        Calender.setRooms(all_days, REMOVE=False)
        Calender.save_calender()

        # show charges
        system_message(QMessageBox.Information,"Reservation Succesfull saved\n"
                                               f"Your total fees are ${reservation.getTotalFees()}")

        system_load_table(Reservations.table,Reservations.current_user)









