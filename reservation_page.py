from system_objects import *
Calender.load_calender()

#query customer object with username
user = Database.load_object("SELECT * FROM customer " + \
                            f"WHERE username = '{username}'"
                            ,Customer)[0]

#query all reservations tied to customer and displays them
all_reservations = Database.load_object("SELECT * FROM reservation " + \
                                       f"WHERE customer_ID == '{user.getID()}'"
                                       ,Reservation)


#################################################################################################
#################################################################################################
##################################################################################################

#customer selects a reservation and chooses to cancel
reservation = all_reservations[0]

all_days = Database.load_object("SELECT * FROM day " + \
                                f"WHERE reservation_ID = '{reservation.getID()}' " + \
                                "ORDER BY date ASC",
                                 Day)

#alert user if there sure they want to cancel
Database.delete_object(reservation)




# startdate = string_to_date_object(reservation.getStartdate())
# if reservation.getType() in ('conventional','incentive'):
#
#     # less than 3 days still start
#     if startdate - timedelta(days = 3) < date.today() <= startdate:
#         [Database.delete_object(day) for day in all_rates[1:]]
#
#     #more than 3 days from start
#     elif date.today() <= startdate - timedelta(days= 3):
#         [Database.delete_object(day) for day in all_rates]
#
#     else:
#         for day in all_rates:
#             if string_to_date_object(day.getDate()) > date.today():
#                 Database.delete_object(day)


#update room avalibility
Calender.setRooms(all_days, REMOVE = True)
Calender.save_calender()


#####################################################################################
###################################################################################
#######################################################################################
