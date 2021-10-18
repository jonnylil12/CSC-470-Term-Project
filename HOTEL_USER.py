from system_core import *

# get latest calender data
Calender.load_calender()

system_remove_noshows()   # remove reservations that havent checked in and its past startdate
system_remove_unpayed()   # remove sixtydays that havent payed and its pass grace period
system_remove_notlefted()  # remove reservations that havent been checked out and its past enddate
