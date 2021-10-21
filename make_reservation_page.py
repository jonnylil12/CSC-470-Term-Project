from system_core import *
Calender.load_calender()

user = Customer() #remove this



#customer chooses to make prepaid reservation

Type = input("Type:") #prepaid

#customer enters info
startdate = input("startdate:") #'10-08-21'
enddate = input("enddate:") #'10-10-21'

#user confirms

reservation = None
if Type == 'prepaid':
    reservation = Prepaid(None,user.getID(),startdate,enddate,None,False,None,Type,system_date_to_str(date.today()))
elif Type == 'sixtyday':
    reservation = Sixtyday(None, user.getID(), startdate, enddate, None, False, None, Type, None)
elif Type == 'conventional':
    reservation = Prepaid(None, user.getID(), startdate, enddate, None, False, None, Type, None)
elif Type == 'incentive':
    reservation = Prepaid(None, user.getID(), startdate, enddate, None, False, None, Type, None)




if system_str_to_date(startdate) >= system_str_to_date(enddate):
    print("SYSTEM ERROR startdate must be less than enddate")

elif date.today() > system_str_to_date(startdate):
    print("SYSTEM ERROR you cannot make a reservation starting in the past")

elif not Calender.rooms_are_avaliable(startdate, enddate):
    print("SYSTEM ERROR there are no rooms avaliable for that entire period")

elif not reservation.is_valid(user):
    print("SYSTEM ERROR reservation is not valid and cannot be made")

else:
    #generate charges and room space
    Database.save_object(reservation)

    all_days , totalfees = system_generate_days(reservation)

    # charges are saved
    [Database.save_object(day) for day in all_days]

    # reservation is saved
    reservation.setTotalFees(totalfees)
    Database.save_object(reservation)

    # calender room space is added
    Calender.setRooms(all_days, REMOVE = False)
    Calender.save_calender()

    # show charges
    print(reservation.getTotalFees())


# alert user of successfull creation







