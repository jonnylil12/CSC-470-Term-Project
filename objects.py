import sqlite3



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
        Database.query(f"DELETE FROM {record.table} WHERE ID == {record.getID()}")

    @staticmethod
    def save_object(record):
        Database.delete_object(record)
        error = Database.query(f"INSERT INTO {record.table} VALUES(?" + ',?' * (len(record.__dict__) - 1) + ")",
                                                                                [*record.__dict__.values()])
        record.setID(Database.query(f"SELECT ID FROM {record.table} ")[-1][0])
        return error

class Customer:
    """
     A class to represent a person.

    Attributes
     --------------------------------------------------------------
    customer_ID : int
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
        self.__name, \
        self.__email, \
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
          foreign key of reservation object in database mapped to customer object
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
    table = 'reservations'

    def __init__(self,*attributes,TIME_PERIOD = None):
        self.__ID  , \
        self.__customer_ID , \
        self.__startdate , \
        self.__enddate , \
        self.__totalfees , \
        self.__isCheckedin , \
        self.__roomnumber , \
        self.__type = attributes

        self.TIME_PERIOD = TIME_PERIOD


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
        self.__startdate = startdate
    def setEnddate(self,enddate):
        self.__enddate = enddate
    def setTotalFees(self,totalfees):
        self.__totalfees = totalfees
    def setCheckin(self,isCheckedin):
        self.__isCheckedin = isCheckedin
    def setRoomnumber(self,roomnumber):
        self.__roomnumber = roomnumber
    def setType(self,Type):
        self.__type = Type

    def load_period(self):
        for day in Database.query(f"SELECT * FROM periods WHERE reservation_ID == '{self.__ID}'"):
            reservation_ID, date , rate = day
            self.TIME_PERIOD[date] = [reservation_ID, rate]

    def delete_period(self):
        Database.query(f"DELETE FROM periods WHERE reservation_ID == '{self.__ID}")

    def save_period(self):
        self.delete_period()
        for day in self.TIME_PERIOD:
            self.TIME_PERIOD[day][0] = self.__ID

        for day in self.TIME_PERIOD:
            date = day
            reservation_ID = self.TIME_PERIOD[day][0]
            rate = self.TIME_PERIOD[day][1]
            Database.query("INSERT INTO periods VALUES(?,?,?)", [reservation_ID, date, rate])



class Internal_Calender:
    """
           A class to represent the internal calender.

          Attributes
          --------------------------------------------------------------

          global_calender: dict
              a collection of datetime and baserate/room avalibity pairs

          Methods
          --------------------------------------------------------------
          booking()  -
             @:param
                period : dict
                remove : bool

          is_valid()  - determines if period can be made (subject to avalibility)
             @:param
                period : ( Day , Day , Day ... )
             @:return
               all(Calender.get(day.getDate())[1] != 0 for day in period) : bool

          query_calender() - gets calender data from database
          save_calender() - updates all calender data in database
          delete_calender() - removes all calender data from database
          show() - displays calender contents

          """
    CALENDER = {}

    @staticmethod
    def booking(period,*,REMOVE = False ):
         x = -1 if not REMOVE else 1
         for day in period:
            Internal_Calender.CALENDER[day][1] += x

    @staticmethod
    def is_valid(period):
        return all(Internal_Calender.CALENDER[day][1] != 0 for day in period)

    @staticmethod
    def load_calender():
        for day in Database.query("SELECT * FROM calender"):
            date ,baserate , rooms = day
            Internal_Calender.CALENDER[date] = [baserate, rooms]

    @staticmethod
    def delete_calender():
        Database.query("DELETE FROM calender")

    @staticmethod
    def save_calender():
        Internal_Calender.delete_calender()
        for day in Internal_Calender.CALENDER:
            date = day
            baserate = Internal_Calender.CALENDER[day][0]
            rooms =Internal_Calender.CALENDER[day][1]
            Database.query("INSERT INTO calender VALUES(?,?,?)", [date, baserate, rooms])


#todo
class Prepaid(Reservation):

     def  __init__(self,*attributes,TIME_PERIOD = None):
        Reservation.__init__(self,*attributes,TIME_PERIOD = TIME_PERIOD)

     def is_valid(self):
        return all((Internal_Calender.is_valid(self.TIME_PERIOD),
                    "?"
                    "?"
                    "?"
                    "?"
                    "?"
                    "???"))


#todo
class Sixty_days_in_advance(Reservation):

    def __init__(self,*attributes,TIME_PERIOD = None):
        Reservation.__init__(self,*attributes,TIME_PERIOD = TIME_PERIOD)


#todo
class Conventional(Reservation):

    def __init__(self,*attributes,TIME_PERIOD = None):
        Reservation.__init__(self,*attributes,TIME_PERIOD = TIME_PERIOD)


#todo
class Incentive(Reservation):
    def __init__(self,*attributes,TIME_PERIOD = None):
        Reservation.__init__(self,*attributes,TIME_PERIOD = TIME_PERIOD)






