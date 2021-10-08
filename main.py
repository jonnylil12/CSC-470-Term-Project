import sqlite3
import datetime

class Database:

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
    def load_record(constructor, query):
        return [constructor(*attributes) for attributes in Database.query(query)]

    @staticmethod
    def create_record(record):
        error = Database.query(f"INSERT INTO {record.table} VALUES(?" + ',?' * (len(record)-1) +")",[*record])
        record.setID(Database.query(f"SELECT ID FROM {record.table} ")[-1][0])
        return error

    @staticmethod
    def delete_record(record):
        Database.query(f"DELETE FROM {record.table} WHERE ID == {record.getID()}")

    @staticmethod
    def update_record(record):
        Database.delete_record(record)
        return Database.create_record(record)

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
    table = 'customer'
    def __init__(self,*attributes):

        self.__ID , \
        self.__name, \
        self.__email, \
        self.__username, \
        self.__password, \
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


    def __len__(self):
        return len((self.__ID, self.__name, self.__email,
                    self.__username,self.__password,self.__creditcard))

    def __iter__(self):
        return iter((self.__ID, self.__name, self.__email,
                     self.__username,self.__password,self.__creditcard))

    def __str__(self):
        return f"primary key: {self.__ID} \n" \
               f"name: {self.__name} \n" \
               f"email: {self.__email} \n" \
               f"username: {self.__username} \n" \
               f"password: {self.__password} \n" \
               f"credit card: {self.__creditcard} \n " \

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
           enddate of reservatiion
      totalfees: float
           total amout of accumulated charges
      ischeckedin : bool
          true or false if person is occuping this reservation
      roomnumber : int
          current room number
      type : str
          type of reservation


      Methods
       --------------------------------------------------------------
      getters and setters for each attribute except customer_ID
      """

    table = 'reservations'
    def __init__(self,*attributes):
        self.__ID , \
        self.__customer_ID, \
        self.__startdate, \
        self.__enddate,\
        self.__totalfees, \
        self.__isCheckedin, \
        self.__roomnumber, \
        self.__type =  attributes

        self.__period = {}


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
            self.__period[date] = [reservation_ID, rate]
        return self.__period

    def create_period(self,newperiod):

        for day in newperiod:
            newperiod[day][0] = self.__ID

        self.__period = newperiod
        for day in newperiod:
            date = day
            reservation_ID =  newperiod[day][0]
            rate =  newperiod[day][1]
            Database.query("INSERT INTO periods VALUES(?,?,?)", [reservation_ID,date,rate])


    def delete_period(self):
        Database.query(f"DELETE FROM periods WHERE reservation_ID == '{self.__ID}")

    def update_period(self):
        self.delete_period()
        self.create_period(self.__period)


    def __len__(self):
        return len((self.__ID, self.__customer_ID, self.__startdate, self.__enddate,
                        self.__totalfees, self.__isCheckedin, self.__roomnumber,
                        self.__type))

    def __iter__(self):
        return iter((self.__ID, self.__customer_ID, self.__startdate, self.__enddate,
                         self.__totalfees, self.__isCheckedin, self.__roomnumber,
                         self.__type))

    def __str__(self):
        return f"primary key: {self.__ID} \n" \
               f"foreign key: {self.__customer_ID} \n" \
               f"start date: {self.__startdate} \n" \
               f"end date: {self.__enddate} \n" \
               f"total charges: ${format(self.__totalfees,',.2f')} \n" \
               f"checked in: {self.__isCheckedin} \n" \
               f"room number: {self.__roomnumber} \n" \
               f"type: {self.__type} \n"

class Managment:
    """
           A class to represent the internal Management.

          Attributes
          --------------------------------------------------------------

          global_calender: dict
              a collection of datetime and baserate/room avalibity pairs

          Methods
          --------------------------------------------------------------

          room_avalibility()  -
             @:param
                period : dict
                remove : bool

          is_valid()  - determines if period can be made (subject to avalibility)
             @:param
                period : ( Day , Day , Day ... )
             @:return
               all(Calender.get(day.getDate())[1] != 0 for day in period) : bool

          load_calender() - gets calender data from database
              @:return
                    Managment.__calender : dict

          create_calender() - writes all calender data into database
          update_calender() - updates all calender data in database
          delete_calender() - removes all calender data from database

          """
    __calender = {}

    @staticmethod
    def room(period,*,remove = False ):
         x = -1 if not remove else 1
         for day in period:
            Managment.__calender[day][1] += x

    @staticmethod
    def is_valid(period):
        return all(Managment.__calender[day][1] != 0 for day in period)

    @staticmethod
    def load_calender():
        for day in Database.query("SELECT * FROM calender"):
            date ,baserate , rooms = day
            Managment.__calender[date] = [baserate,rooms]
        return Managment.__calender

    @staticmethod
    def create_calender(new_calender):
        Managment.__calender = new_calender
        for day in new_calender:
            date = day
            baserate = new_calender[day][0]
            rooms = new_calender[day][1]
            Database.query("INSERT INTO calender VALUES(?,?,?)",[date,baserate,rooms])

    @staticmethod
    def delete_calender():
        Database.query("DELETE FROM calender")

    @staticmethod
    def update_calender():
        Managment.delete_calender()
        Managment.create_calender(Managment.__calender)

    @staticmethod
    def show(self):
        for day in Managment.__calender:
            date = day
            baserate = Managment.__calender[day][0]
            rooms = Managment.__calender[day][1]
            print(f"date: {date} , base rate: {baserate} , rooms avaliable: {rooms}")

#todo
class Prepaid(Reservation):

     def  __init__(self,*attributes):
        Reservation.__init__(self,*attributes)

     def is_valid(self,period):
        return Managment.is_valid(period)
#todo
class Sixty_days_in_advance(Reservation):

    def __init__(self, *attributes):
        Reservation.__init__(*attributes)


#todo
class Conventional(Reservation):

    def __init__(self, *attributes):
        Reservation.__init__(*attributes)


#todo
class Incentive(Reservation):
    def __init__(self, *attributes):
        Reservation.__init__(*attributes)






