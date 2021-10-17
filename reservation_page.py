from system_procedures import *
import os
Calender.load_calender()

username = 1
#query customer object with username
user = Database.load_object("SELECT * FROM customer " + \
                            f"WHERE username = '{username}'"
                            ,Customer)[0]

#query all reservations tied to customer and displays them
all_reservations = Database.load_object("SELECT * FROM reservation " + \
                                       f"WHERE customer_ID == '{user.getID()}' " +
                                        "AND checkedin IS NOT NULL"
                                       ,Reservation)


def generateAccomadationBill(user,reservation,totalnights):

    os.makedirs(os.path.dirname("accommodationbills\\_.txt"), exist_ok=True)
    filepath = f"{os.path.abspath('accommodationbills')}\\{user.getID()}"

    with open(f"{filepath}.txt", "w") as output_file:
        bill =  "                  Ophelia's Oasis Hotel\n" + \
                "Thank you for stay we hope you had the best experience and will see you again"+ \
                "\n\n"+ \
                f"Todays date:     {system_date_to_str(date.today())}\n"+ \
                f"Name:            {user.getName()}\n"+ \
                f"Room number:     {reservation.getRoomnumber()}\n"+ \
                f"Start date:      {reservation.getStartdate()}\n"+ \
                f"Departure date:  {reservation.getEnddate()}\n"+ \
                f"Total nights:    {totalnights}\n"+ \
                f"Total charge:    ${reservation.getTotalFees():,.2f}\n"


        if reservation.getType() in 'prepaid,sixtyday':
                bill += f"Payment date:    {reservation.getPaydate()}"

        output_file.write(bill)


#####################################################################################
########################################  CANCEL  RESERVATION ########################################
#####################################################################################




#customer selects a reservation and chooses to cancel
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " + \
                                f"WHERE reservation_ID = '{reservation.getID()}' " + \
                                "ORDER BY date ASC",
                                 Day)

#if reservation exists and user is not checked in
if reservation and not reservation.getCheckedin():
    #alert user if there sure they want to cancel


    startdate = system_str_to_date(reservation.getStartdate())
    if reservation.getType() in ('conventional','incentive'):

        # less than 3 days still start
        if startdate - timedelta(days = 3) < date.today() <= startdate:
            [Database.delete_object(day) for day in all_days[1:]]

        #more than 3 days from start
        elif date.today() <= startdate - timedelta(days= 3):
            [Database.delete_object(day) for day in all_days]


    reservation.setCheckedin(None)
    Database.save_object(reservation)

    #update room avalibility
    Calender.setRooms(all_days, REMOVE = True)
    Calender.save_calender()

    # alert user of successfull cancelation
else:
    pass
    #user cant cancel


#####################################################################################
#################################### CHECK INTO/ OUT RESERVATION   #################################
#######################################################################################


#customer selects a reservation and chooses to checkin
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " + \
                                f"WHERE reservation_ID = '{reservation.getID()}' " + \
                                "ORDER BY date ASC",
                                 Day)


#reservation exists and current date equals startdate
if reservation and reservation.getStartdate() == system_date_to_str(date.today()):

    #user is checking in
    if not reservation.getCheckedin():


        roomnumber = len(Database.query("SELECT * FROM reservation " +
                                         f"WHERE startdate <= '{system_date_to_str(date.today())}' " +
                                         f"AND '{system_date_to_str(date.today())}' < enddate " +
                                         "AND checkedin == True")) + 1

        reservation.setCheckedin(True)
        reservation.setRoomnumber(roomnumber)
        Database.save_object(reservation)
        # alert user of successfull checkin

    #user is checking out
    else:
        if reservation.getType()in 'prepaid,sixtyday':
            for day in all_days:
                if system_str_to_date(day.getDate()) > date.today():
                    Database.delete_object(day)

        reservation.setCheckedin(None)
        Database.save_object(reservation)
        generateAccomadationBill(user, reservation, len(all_days))
        # alert user of successfull checkout


else:
    pass
    #user cant checkin or checkout
