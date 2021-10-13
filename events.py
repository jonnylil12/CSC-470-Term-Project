from objects import *

def yield_dates(startdate,enddate):
    current = datetime.strptime(startdate, '%m-%d-%y').date()
    stop = datetime.strptime(enddate, '%m-%d-%y').date()
    while current <= stop:
         yield current.strftime("%m-%d-%y")
         current += timedelta(days=1)

def generate_rates(startdate,enddate,ID):
    all_dates = yield_dates(startdate, enddate)
    all_days = [Day(None, ID, date, Calender.getBaserate(date)) for date in all_dates]
    totalfees = sum([day.getRate() for day in all_days])
    return all_days , totalfees

def string_to_date_object(string):
    return datetime.strptime(string, "%d-%m-%y").date()

def date_object_to_string(date):
    return date.strftime("%m-%d-%y")
