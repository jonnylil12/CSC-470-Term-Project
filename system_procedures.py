from datetime import *
from system_objects import *

def str_to_date(string):
    return datetime.strptime(string, '%m-%d-%y').date()

def date_to_str(date):
    return date.strftime('%m-%d-%y')

def system_date_range(startdate, enddate):
    current , stop = str_to_date(startdate) , str_to_date(enddate)
    while current < stop:
         yield current.strftime('%m-%d-%y')
         current += timedelta(days=1)



#gets rid of days for prepaid and sixtyday reservations
#if todays date is greater than them.
def system_clear_days():
    all_days = Database.load_object("SELECT * FROM day d" +
                                   f"WHERE date < '{date_to_str(date.today())}' " +
                                    "AND (SELECT type reservation WHERE ID == d.reservation_ID )",
                                    Day)

    [Database.delete_object(day) for day in all_days]


