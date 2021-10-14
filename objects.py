import sqlite3
from datetime import datetime, timedelta , date

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
        self.__type = attributes

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
    def isCheckedin(self):
        return self.__isCheckedin
    def getRoomnumber(self):
        return self.__roomnumber
    def getType(self):
        return self.__type

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
    def setCheckin(self,isCheckedin):
        self.__isCheckedin = isCheckedin
    def setRoomnumber(self,roomnumber):
        self.__roomnumber = roomnumber
    def setType(self,Type):
        self.__type = Type

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

    # should only be called from the CLI.py
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

    #should only be called from the CLI.py
    @staticmethod
    def setBaserate(date, baserate):
        if Calender.__CALENDER.get(date,"null") == 'null':
            Calender.__CALENDER[date] = [baserate,45]
        else:
            Calender.__CALENDER[date][0] = baserate

    @staticmethod
    def rooms_are_avaliable(startdate, enddate):
        current = datetime.strptime(startdate, '%m-%d-%y').date()
        stop = datetime.strptime(enddate, '%m-%d-%y').date()
        while current <= stop:
            if Calender.__CALENDER[current.strftime('%m-%d-%y')][1] == 0:
                    return False
            current += timedelta(days=1)
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
        for day in Calender.__CALENDER:
            date = day
            baserate = Calender.__CALENDER[day][0]
            rooms = Calender.__CALENDER[day][1]
            Database.query("INSERT INTO calender VALUES(?,?,?)", [date, baserate, rooms])


#todo
class Prepaid(Reservation):

     def  __init__(self,*attributes):
        super().__init__(*attributes)

     def is_valid(self):
        return Calender.rooms_are_avaliable(self.getStartdate(), self.getEnddate())


#todo
class Sixty_days_in_advance(Reservation):

    def __init__(self,*attributes):
        super().__init__(*attributes)


#todo
class Conventional(Reservation):

    def __init__(self,*attributes):
        super().__init__(*attributes)


#todo
class Incentive(Reservation):
    def __init__(self,*attributes):
        super().__init__(*attributes)






