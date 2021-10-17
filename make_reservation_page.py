from system_procedures import *
Calender.load_calender()

def generate_days(startdate, enddate, ID):
    all_dates = system_date_range(startdate, enddate)
    all_days = [ Day(None, ID, date, Calender.getBaserate(date)) for date in all_dates]
    totalfees = sum([day.getRate() for day in all_days])
    return all_days , totalfees

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



if not (system_str_to_date(startdate < enddate)):
    print("SYSTEM ERROR startdate must be less than enddate")

if not date.today() <= system_str_to_date(startdate):
    print("SYSTEM ERROR you cannot make a reservation starting in the past")

elif not reservation.is_valid():
    print("SYSTEM ERROR reservation is not valid")

else:
    #generate chares
    Database.save_object(reservation)

    all_days ,totalfees = generate_days(startdate, enddate, reservation.getID())
    [Database.save_object(day) for day in all_days]

    reservation.setTotalFees(totalfees)
    Database.save_object(reservation)

    # show charges

    # calender room space is updated
    Calender.setRooms(all_days, REMOVE = False)
    Calender.save_calender()

   # alert user of successfull creation







