from system_procedures import *
Calender.load_calender()

def generate_days(reservation):
    all_dates = system_date_range(reservation.getStartdate(),reservation.getEnddate())

    all_days = []
    totalfees = 0
    for date in all_dates:
          rate = Calender.getBaserate(date)
          day = Day(None, reservation.getID(), date, rate * reservation.percent)
          all_days.append(day)
          totalfees += rate

    reservation.setTotalFees(totalfees)
    Database.save_object(reservation)

    return all_days


#customer chooses to make prepaid reservation

Type = input("Type:") #prepaid

#customer enters info
customer_ID = user.getID()
startdate = input("startdate:") #'10-08-21'
enddate = input("enddate:") #'10-10-21'
totalfees = None
checkin = False
roomnumber = None
paydate = (system_date_to_str(date.today()) if Type in 'prepaid,conventional' else None)


#user chooses to create reservation
reservation = Prepaid(None,customer_ID,startdate,enddate,None,False,None,Type,paydate)



if not (system_str_to_date(startdate) < system_str_to_date(enddate)):
    print("SYSTEM ERROR startdate must be less than enddate")

elif not (date.today() <= system_str_to_date(startdate) ):
    print("SYSTEM ERROR you cannot make a reservation starting in the past")

elif not Calender.rooms_are_avaliable(startdate, enddate):
    print("SYSTEM ERROR there are no rooms avaliable for that entire period")

elif not reservation.is_valid():
    print("SYSTEM ERROR reservation is not valid")


else:
    #generate chares
    Database.save_object(reservation)

    all_days = generate_days(reservation)

    [Database.save_object(day) for day in all_days]

    # show charges

    # calender room space is updated
    Calender.setRooms(all_days, REMOVE = False)
    Calender.save_calender()

   # alert user of successfull creation







