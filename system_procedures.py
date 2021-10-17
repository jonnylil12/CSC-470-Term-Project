from datetime import *
from system_objects import *


def system_str_to_date(string):
    return datetime.strptime(string, '%m-%d-%y').date()

def system_date_to_str(date):
    return date.strftime('%m-%d-%y')

def system_date_range(startdate, enddate):
    current , stop = system_str_to_date(startdate) , system_str_to_date(enddate)
    while current < stop:
         yield current.strftime('%m-%d-%y')
         current += timedelta(days=1)

def system_overdue_reservations():
    overdue_stays = Database.load_object("SELECT * FROM reservation " +
                                         f"WHERE '{system_date_to_str(date.today())}' > enddate " +
                                         'AND checkedin == True',
                                         Reservation)
    for reservation in overdue_stays:
        if reservation.getType() in 'convetional,incentive':
            reservation.setPaydate(reservation.getEnddate())

        reservation.setCheckedin(None)
        Database.save_object(reservation)


