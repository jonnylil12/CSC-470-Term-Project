from system_core import *
Calender.load_calender()

user = Customer() #remove this
all_reservations= [] #remove this


#customer selects a reservation and chooses to change
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " +
                                f"WHERE reservation_ID = '{reservation.getID()}' " +
                                "ORDER BY date ASC",
                                 Day)

#customer chooses to change reservation
# alert user if there sure they want to change reservation


#customer enters info

startdate = input("startdate:") #'10-08-21'
enddate = input("enddate:") #'10-10-21'

#user confirms
reservation.setStartdate(startdate)
reservation.setEnddate(enddate)

if not reservation:
    print("SYSTEM ERROR you have no active reservations\n")

elif reservation.getCheckedin():
    print("SYSTEM ERROR your trying to change a reservation your currently checked into.\n"
          "Try checking out instead\n")

elif system_str_to_date(startdate) >= system_str_to_date(enddate):
    print("SYSTEM ERROR startdate must be less than enddate")

elif date.today() > system_str_to_date(startdate):
    print("SYSTEM ERROR you cannot make a reservation starting in the past")

elif not Calender.rooms_are_avaliable(startdate, enddate):
    print("SYSTEM ERROR there are no rooms avaliable for that entire period")

elif not reservation.is_valid(user):
    print("SYSTEM ERROR reservation is not valid and cannot be changed")

else:

    #generate charges and room space
    if reservation.getType() in 'conventional,incentive':
         [Database.delete_object(day) for day in all_days]
         new_days, totalfees = system_generate_days(reservation)

    else:
         new_days, totalfees = system_generate_days(reservation,True)

         # issuse refund if new amount is greater than old
         if totalfees >= reservation.getTotalFees():
             [Database.delete_object(day) for day in all_days]


    # old calender room space is removed
    Calender.setRooms(all_days, REMOVE=True)
    Calender.save_calender()


    #charges are saved
    [Database.save_object(day) for day in new_days]

    # reservation is saved
    reservation.setTotalFees(totalfees)
    Database.save_object(reservation)

    # calender room space is added
    Calender.setRooms(new_days, REMOVE = False)
    Calender.save_calender()

    # show charges
    print(reservation.getTotalFees())
