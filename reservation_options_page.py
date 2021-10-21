from system_core import *
import os

# get latest calender data
Calender.load_calender()

user = Customer()

#query customer object with username
user = Database.load_object("SELECT * FROM customer " +
                            f"WHERE username = '{user.getUsername()}'"
                            ,Customer)[0]

#query all reservations tied to customer and displays them
all_reservations = Database.load_object("SELECT * FROM reservation " +
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




#customer chooses to cancel reservation

# alert user if there sure they want to cancel
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " +
                                f"WHERE reservation_ID = '{reservation.getID()}' " +
                                "ORDER BY date ASC",
                                 Day)



if not reservation:
    print("SYSTEM ERROR you have no active reservations\n")


elif reservation.getCheckedin():
    print("SYSTEM ERROR your trying to cancel a reservation your currently checked into.\n" 
          "Try checking out instead\n")

else:
    #user confirms
    if reservation.getType() in 'conventional,incentive':

        # charge for first day only
        if  date.today() > ( system_str_to_date(reservation.getStartdate()) - timedelta(days = 3)):

            [Database.delete_object(day) for day in all_days[1:]]
            reservation.setTotalFees(all_days[0].getRate())
            reservation.setPaydate(system_date_to_str(date.today()))

        #more than 3 days from start
        else:

            [Database.delete_object(day) for day in all_days]
            reservation.setTotalFees(0)




    reservation.setCheckedin(None)
    Database.save_object(reservation)

    # old calender room space is removed
    Calender.setRooms(all_days, REMOVE=True)
    Calender.save_calender()

# alert user of successfull cancelation


#####################################################################################
#################################### CHECK INTO/ OUT RESERVATION   #################################
#######################################################################################


#customer selects a reservation and chooses to checkin
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " +
                                f"WHERE reservation_ID = '{reservation.getID()}' " +
                                "ORDER BY date ASC",
                                 Day)


if not reservation:
    print("SYSTEM ERROR you have no active reservations \n")

elif date.today() < system_str_to_date(reservation.getStartdate()) :
    print("SYSTEM ERROR you are trying to check ( in / out )  of a reservation before it started.\n"
          "Please wait until your startdate to try again\n")

else:
    #user is checking in
    if not reservation.getCheckedin():
        roomnumber = len(Database.query("SELECT * FROM reservation " +
                                         f"WHERE startdate <= '{system_date_to_str(date.today())}' " +
                                         f"AND '{system_date_to_str(date.today())}' < enddate " +
                                         "AND checkedin == True")) + 1

        reservation.setCheckedin(True)
        reservation.setRoomnumber(roomnumber)
        Database.save_object(reservation)


    #user is checking out
    # alert user if there sure they want to checkout
    else:

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

        #make a accomodation bill
        generateAccomadationBill(user, reservation, len(all_days))

    # alert user of successfull check in / out


