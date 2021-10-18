from system_core import *
Calender.load_calender()


user = Customer()

#customer chooses to make prepaid reservation

Type = input("Type:") #prepaid

#customer enters info
customer_ID = user.getID()
startdate = input("startdate:") #'10-08-21'
enddate = input("enddate:") #'10-10-21'
totalfees = None
checkin = False
roomnumber = None
paydate = (system_date_to_str(date.today()) if Type in 'prepaid,sixtyday' else None)


#user chooses to create reservation
reservation = Prepaid(None,customer_ID,startdate,enddate,None,False,None,Type,paydate)


if system_str_to_date(startdate) >= system_str_to_date(enddate):
    print("SYSTEM ERROR startdate must be less than enddate")

elif date.today() > system_str_to_date(startdate):
    print("SYSTEM ERROR you cannot make a reservation starting in the past")

elif not Calender.rooms_are_avaliable(startdate, enddate):
    print("SYSTEM ERROR there are no rooms avaliable for that entire period")

elif not reservation.is_valid(user):
    print("SYSTEM ERROR reservation is not valid")

else:
    #generate chares
    Database.save_object(reservation)

    all_days = system_generate_days(reservation)

    [Database.save_object(day) for day in all_days]

    # calender room space is updated
    Calender.setRooms(all_days, REMOVE = False)
    Calender.save_calender()

    # show charges
    print(reservation.getTotalFees())


# alert user of successfull creation







