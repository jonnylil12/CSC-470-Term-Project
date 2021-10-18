import sqlite3
from datetime import datetime, timedelta , date

#####################################################################################
#################################### SYSTEM CALLS  #################################
#######################################################################################


def system_str_to_date(string):
    return datetime.strptime(string, '%m-%d-%y').date()

def system_date_to_str(date):
    return date.strftime('%m-%d-%y')

def system_date_range(startdate, enddate):
    current = system_str_to_date(startdate)
    stop = system_str_to_date(enddate)
    while current < stop:
         yield current.strftime('%m-%d-%y')
         current += timedelta(days=1)



def system_remove_noshows():
    all_no_shows = Database.load_object("SELECT * FROM reservation  " +
                                        f"WHERE startdate < '{system_date_to_str(date.today())}' " +
                                        "AND checkedin == False",
                                        Reservation)

    if all_no_shows != []:
        for reservation in all_no_shows:
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' " +
                                            "ORDER BY date ASC",
                                            Day)
            penalty = 100.00

            # charged for first day only
            if reservation.getType() in 'conventional,incentive':

                [Database.delete_object(day) for day in all_days[1:]]

                reservation.setTotalFees(all_days[0].getRate())
                reservation.setPaydate(system_date_to_str(date.today()))

            # charged no show penalty
            else:
                all_days[0].setRate(all_days[0].getRate() + penalty)
                Database.save_object(all_days[0])

                reservation.setTotalFees(reservation.getTotalFees() + penalty)

            reservation.setCheckedin(None)
            Database.save_object(reservation)

            # update room avalibility
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()



def system_remove_unpayed():
    all_unpayed = Database.load_object("SELECT * FROM reservation " +
                                        "WHERE type == 'sixtyday' " +
                                        "AND checkedin IS NOT NULL " +
                                        "AND paydate IS NULL",
                                        Reservation)
    if all_unpayed != []:
        for reservation in all_unpayed:
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' ",
                                            Day)

            if date.today() > system_str_to_date(reservation.getStartdate()) - timedelta(days=30):

                [Database.delete_object(day) for day in all_days]

                reservation.setTotalFees(0)
                reservation.setCheckedin(None)
                Database.save_object(reservation)

                # update room avalibility
                Calender.setRooms(all_days, REMOVE=True)
                Calender.save_calender()



def system_remove_notlefted():
    all_not_lefted = Database.load_object("SELECT * FROM reservation " +
                                         f"WHERE '{system_date_to_str(date.today())}' > enddate " +
                                         'AND checkedin == True',
                                         Reservation)
    if all_not_lefted != []:
        for reservation in all_not_lefted:
            all_days = Database.load_object("SELECT * FROM day " +
                                            f"WHERE reservation_ID = '{reservation.getID()}' ",
                                            Day)

            if reservation.getType() in 'conventional,incentive':
                reservation.setPaydate(reservation.getEnddate())

            reservation.setCheckedin(None)
            Database.save_object(reservation)

            # update room avalibility
            Calender.setRooms(all_days, REMOVE=True)
            Calender.save_calender()



def system_generate_days(reservation):

        totalfees = 0
        all_days = []
        for date in system_date_range(reservation.getStartdate(),reservation.getEnddate()):
              rate = Calender.getBaserate(date) * reservation.getPercent()
              all_days.append(   Day(None, reservation.getID(), date, rate)  )
              totalfees += rate

        reservation.setTotalFees(totalfees)
        Database.save_object(reservation)

        return all_days

#####################################################################################
#################################### SYSTEM OBJECTS  #################################
#######################################################################################


class Database:

    """
     A class that represents the database.

    Methods
    --------------------------------------------------------------
    query() - makes general SQL query
        @:param
            query : str
        @:return
            cursor.fetchall() : list (list ( data....) )


    load_object() - based on query gets attributes and recontructs into a object
                    constructor parameter should be the class of the object
        @:param
            query : str
            constructor : object class
        @:return
            [constructor(*attributes) for attributes in Database.query(query)] : list ( object ... )


    delete_object() - removes object from database
        @:param
            record : object


    save_object() - decontructs object and new writes data in database
        @:param
            record : object
    """
    @staticmethod
    def query(query,values = None):

        with sqlite3.connect("database.db") as file:
            cursor = file.cursor()

            try:
                if values == None:
                     cursor.execute(query)
                else:
                     cursor.execute(query,values)

            except Exception as error:
                print(error)
                return error

            finally:
                file.commit()
                return cursor.fetchall()

    @staticmethod
    def load_object(query, constructor):
        return [constructor(*attributes) for attributes in Database.query(query)]


    @staticmethod
    def delete_object(record):
        Database.query(f"DELETE FROM {record.table} " +
                       f"WHERE ID == {record.getID()}")

    @staticmethod
    def save_object(record):
        Database.delete_object(record)
        error = Database.query(f"INSERT INTO {record.table} " +
                               f"VALUES(?" + ',?' * (len(record.__dict__) - 1) + ")",
                               [*record.__dict__.values()])

        ID = Database.query(f"SELECT ID FROM {record.table} " +
                            f"ORDER BY ID DESC " +
                            f"LIMIT 1")[0][0]

        record.setID(ID)
        return error

class Customer:
    """
     A class to represent a person.

    Attributes
     --------------------------------------------------------------
    ID : int
        primary key of customer object in database
    name : str
        full name of the person
    email : str
        email of person, should be unique and follow regex
    username : str
        username of person , should be unique
    password : str
        saved password of persond
    creditcard : int
        creditcard information , should be unique

    Methods
    --------------------------------------------------------------
    getters and setters for each attribute
    """

    #for database
    table = 'customer'

    def __init__(self,*attributes):
        self.__ID , \
        self.__name , \
        self.__email , \
        self.__username , \
        self.__password , \
        self.__creditcard = attributes

    def getID(self):
        return self.__ID
    def getName(self):
        return self.__name
    def getEmail(self):
        return self.__email
    def getUsername(self):
        return self.__username
    def getPassword(self):
        return self.__password
    def getCreditcard(self):
        return self.__creditcard

    def setID(self,ID):
        self.__ID = ID
    def setName(self,name):
        self.__name = name
    def setEmail(self,email):
        self.__email = email
    def setUsername(self,username):
        self.__username = username
    def setPassword(self,password):
        self.__password = password
    def setCreditcard(self,creditcard):
        self.__creditcard = creditcard

class Reservation:
    """
       A Super class to represent a reservation.

      Attributes
       --------------------------------------------------------------
      ID : int
          primary key of reservation object in database
      customer_ID : int
          foreign key of reservation object mapped to customer object in database
      startdate: datetime
          startdate of reservation
      endate: datetime
           enddate of reservation
      totalfees: float
           total amout of accumulated charges
      ischeckedin : bool
          true or false if person is occuping this reservation
      roomnumber : int
          current room number
      type : str
          type of reservation
      TIMEPERIOD : dict
          a dictonary reprsenting all days and there values

      Methods
       --------------------------------------------------------------
       getters and setters for each attribute

       load_period() - gets time period data from database
       save_period() - saves all time period into database
       delete_period() - removes all time period data from database
      """

    # for database
    table = 'reservation'

    def __init__(self,*attributes):
        self.__ID  , \
        self.__customer_ID , \
        self.__startdate , \
        self.__enddate , \
        self.__totalfees , \
        self.__isCheckedin , \
        self.__roomnumber , \
        self.__type , \
        self.__paydate = attributes

    def getID(self):
        return self.__ID
    def getCustomer_ID(self):
        return self.__customer_ID
    def getStartdate(self):
        return self.__startdate
    def getEnddate(self):
        return self.__enddate
    def getTotalFees(self):
        return self.__totalfees
    def getCheckedin(self):
        return self.__isCheckedin
    def getRoomnumber(self):
        return self.__roomnumber
    def getType(self):
        return self.__type
    def getPaydate(self):
        return self.__paydate

    def setID(self,ID):
        self.__ID = ID
    def setCustomer_ID(self,customer_ID):
        self.__customer_ID = customer_ID
    def setStartdate(self,startdate):
        self.__startdate = datetime
    def setEnddate(self,enddate):
        self.__enddate =  datetime
    def setTotalFees(self,totalfees):
        self.__totalfees = totalfees
    def setCheckedin(self, isCheckedin):
        self.__isCheckedin = isCheckedin
    def setRoomnumber(self,roomnumber):
        self.__roomnumber = roomnumber
    def setType(self,Type):
        self.__type = Type
    def setPaydate(self, paydate):
        self.__paydate = paydate

class Day:
    """
         A class to represent a individual day in a reservation.

        Attributes
         --------------------------------------------------------------
        ID : int
            primary key of customer object in database
        reservation_ID : int
           foreign key of day object  mapped to reservation object in database
        date : datetime
            current date for the day
        rate : float
            current rate for the day

        Methods
        --------------------------------------------------------------
        getters and setters for each attribute
        """
    table = "day"
    def __init__(self,*attributes):

        self.__ID , \
        self.__reservation_ID , \
        self.__date , \
        self.__rate = attributes

    def getID(self):
        return self.__ID
    def getReservation_ID(self):
        return self.__reservation_ID
    def getDate(self):
        return self.__date
    def getRate(self):
        return self.__rate

    def setID(self,ID):
        self.__ID = ID
    def setReservation_ID(self,reservation_ID):
        self.__reservation_ID = reservation_ID
    def setDate(self,date):
        self.__date = date
    def setRate(self,rate):
        self.__rate = rate

class Calender:
    """
           A class to represent the internal calender.

          Attributes
          --------------------------------------------------------------

          __CALENDER: dict
              a collection of date and baserate/room avalibity pairs

          Methods
          --------------------------------------------------------------
          getBaserate() - returns for rate at specifyed date
             :param
                date : str
             :return
                Calender.__CALENDER[date][0] : float

          booking()  - will incrememnt or decrement the number of rooms avaliable
                        for each date in calender from list of rate objects
             :param
                time_period : ( Rate , Rate ... )
                REMOVE: bool

          rooms_are_avaliable()  - determines if period can be made (subject to avalibility)
             :param
                startdate : str
                enddate : str
             :return
                bool

          load_calender() - gets calender data from database
          save_calender() - updates all calender data in database
          delete_calender() - removes all calender data from database

          """
    __CALENDER = {}

    # should only be called from the HOTEL_MANAGMENT.py
    @staticmethod
    def getRooms(date):
        return Calender.__CALENDER[date][1]

    @staticmethod
    def getBaserate(date):
        return Calender.__CALENDER[date][0]

    @staticmethod
    def setRooms(time_period, *, REMOVE=False):
        x = (-1 if not REMOVE else 1)
        for day in time_period:
            Calender.__CALENDER[day.getDate()][1] += x

    #should only be called from the HOTEL_MANAGMENT.py
    @staticmethod
    def setBaserate(date, baserate):
        if Calender.__CALENDER.get(date,"null") == 'null':
            Calender.__CALENDER[date] = [baserate,45]
        else:
            Calender.__CALENDER[date][0] = baserate

    @staticmethod
    def rooms_are_avaliable(startdate, enddate):
        for date in system_date_range(startdate,enddate):
            if Calender.__CALENDER[date][1] == 0:
                    return False
        return True


    @staticmethod
    def load_calender():
        for day in Database.query("SELECT * FROM calender"):
            date ,baserate , rooms = day
            Calender.__CALENDER[date] = [baserate, rooms]

    @staticmethod
    def __delete_calender():
        Database.query("DELETE FROM calender")

    @staticmethod
    def save_calender():
        Calender.__delete_calender()
        for date in Calender.__CALENDER:
            baserate = Calender.__CALENDER[date][0]
            rooms = Calender.__CALENDER[date][1]
            Database.query("INSERT INTO calender VALUES(?,?,?)", [date, baserate, rooms])


class Prepaid(Reservation):


     def  __init__(self,*attributes):
        super().__init__(*attributes)


     def is_valid(self,user):
         return all ( ( system_str_to_date(self.getStartdate()) <= (date.today() - timedelta(days=90)),
                       user.getCreditcard() != None ) )


     def getPercent(self):
         return 0.75



class Sixtyday(Reservation):


    def __init__(self,*attributes):
        super().__init__(*attributes)

    def is_valid(self,user):
        return all ( ( system_str_to_date(self.getStartdate()) == (date.today() - timedelta(days=60)),
                      user.getEmail() != None ) )


    def getPercent(self):
        return 0.85



class Conventional(Reservation):


    def __init__(self,*attributes):
        super().__init__(*attributes)

    def is_valid(self, user):
        return user.getCreditcard() != None


    def getPercent(self):
        return 1.00



class Incentive(Reservation):

    def __init__(self,*attributes):
        super().__init__(*attributes)

    def is_valid(self, user):
        return  user.getCreditcard() != None


    def getPercent(self):

        percent  = 1.00

        if date.today() > system_str_to_date(self.getStartdate()) - timedelta(days = 30):

            total_days = 0
            total_period_occupancy = 0
            for day in system_date_range(self.getStartdate(),self.getEnddate()):
                total_day_occupancy = 45 - Calender.getRooms(day)
                total_period_occupancy += total_day_occupancy
                total_days += 1

            average_period_occupancy = total_period_occupancy / total_days
            occupancy_rate = average_period_occupancy / 45

            if occupancy_rate <= 0.60:
                percent = 0.80

        return percent








