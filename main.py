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
    def create_record(table,record):
        error = Database.query("INSERT INTO customer VALUES(?" + ',?' * (len(record)-1) +")",[*record])
        record.setID(Database.query(f"SELECT ID FROM {table} ")[-1][0])
        return error

    @staticmethod
    def delete_record(table,record):
        Database.query(f"DELETE FROM {table} WHERE ID == {record.getID()}")

    @staticmethod
    def update_record(table,ID,column,value):

        query = f"UPDATE {table} SET {column} = {value} WHERE ID == {ID}"
        print(query)
        return Database.query(f"UPDATE {table} SET {column} = {value} WHERE ID = {ID}")


class Customer:
    """
     A class to represent a person.

    Attributes
    ----------
    customer_ID : int
        primary key of customer object in database
    name : str
        full name of the person
    email : str
        email of person, should be unique and follow regex
    username : str
        username of pserson , should be unique
    password : str
        saved password of persond
    creditcard : int
        creditcard information , should be unique

    Methods
    -------
    getters and setters for each attribute
    """
    def __init__(self,*attributes):
        attributes = attributes[0] if len(attributes) == 1 else attributes

        self.__ID , x = (attributes[0] , 1) if len(attributes) == 6 else (None ,0)
        self.__name, \
        self.__email, \
        self.__username, \
        self.__password, \
        self.__creditcard = attributes[x:]

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
        Database.update_record('customer',self.__ID,'name',name)

    def setEmail(self,email):
        self.__email = email
        return Database.update_record('customer',self.__ID,'email',email)

    def setUsername(self,username):
        self.__username = username
        return Database.update_record('customer',self.__ID,'username',username)

    def setPassword(self,password):
        self.__password = password
        Database.update_record('customer',self.__ID,'password',password)

    def setCreditcard(self,creditcard):
        self.__name = creditcard
        return Database.update_record('customer',self.__ID,'creditcard',creditcard)

    def __len__(self):
        return len((self.__ID, self.__name, self.__email,self.__username,self.__password,self.__creditcard))

    def __iter__(self):
        return iter((self.__ID, self.__name, self.__email,self.__username,self.__password,self.__creditcard))

    def __str__(self):
        return f"{self.__ID , self.__name, self.__email, self.__username,self.__password, self.__creditcard}"

c = Customer(28,1,1,1,1,1)
c.setName("david")



class Reservation:
    """
       A class to represent a reservation.

      Attributes
      ----------
      reservation_ID : int
          primary key of reservation object in database
      customer_ID : int
          foreign key of reservation object in database mapped to customer object
      startdate: datetime
          startdate of reservation
      endate: datetime

      totalfees: float

      password : str
          saved password of persond
      creditcard : int
          creditcard information , should be unique

      Methods
      -------
      getters and setters for each attribute except customer_ID
      """
    def __init__(self,*attributes):
        attributes = attributes[0] if len(attributes) == 1 else attributes

        self.__ID , x = (attributes[0] , 1) if len(attributes) == 6 else (None ,0)
        self.__customer_ID, \
        self.__startdate, \
        self.__enddate,\
        self.__totalfees, \
        self.__isCheckedin ,\
        self.__period   = attributes[x:]

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
    def getPeriod(self):
        return self.__period

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
    def setPeriod(self,period):
        self.__period = period


class Prepaid(Reservation):

     def  __init__(self,*attributes):
        Reservation.__init__(*attributes)



class Sixty_days_in_advance(Reservation):

    def __init__(self, *attributes):
        Reservation.__init__(*attributes)



class Conventional(Reservation):

    def __init__(self, *attributes):
        Reservation.__init__(*attributes)



class Incentive(Reservation):
    def __init__(self, *attributes):
        Reservation.__init__(*attributes)


class Calender:

    __global_calender = {}

    def __init__(self,*attributes):
        attributes = attributes[0] if len(attributes) == 1 else attributes

        self.ID, x = (attributes[0], 1) if len(attributes) == 6 else (None, 0)
        self.__reservation_ID , \
        self.__date , \
        self.__rate = attributes[x:]

    def validate_period(self,reservation_ID,start,end):
        pass

    @staticmethod
    def __setitem__(self, key, value):
        Calender.__global_calender[key] = value

    def __getitem__(self, item):
        return Calender.__global_calender[item]
