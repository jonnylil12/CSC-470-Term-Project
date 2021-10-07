import sqlite3

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



class Customer:

    def __init__(self,*attributes):
        self.__customer_ID , \
        self.__name, \
        self.__email, \
        self.__password, \
        self.__creditcard = attributes

    def getCustomer_ID(self):
        return self.__customer_ID
    def getName(self):
        return self.__name
    def getEmail(self):
        return self.__email
    def getPassword(self):
        return self.__password
    def getCreditcard(self):
        return self.__creditcard

    def setName(self,name):
        self.__name = name
        self.__update_record('name',name)

    def setEmail(self,email):
        self.__email = email
        return self.__update_record('email', email)

    def setPassword(self,password):
        self.__password = password
        self.__update_record('password', password)

    def setCreditcard(self,creditcard):
        self.__name = creditcard
        return self.__update_record('creditcard', creditcard)

    def create_record(self):
        error = Database.query(f"INSERT INTO customer VALUES(?,?,?,?,?)" ,
        [self.__customer_ID , self.__name, self.__email, self.__password, self.__creditcard])

        self.__customer_ID  = Database.query(f"SELECT customer_ID FROM customer WHERE email == '{self.__email}'")[0][0]

        return error

    def delete_record(self):
        Database.query(f"DELETE FROM customer WHERE customer_ID == {self.__customer_ID}")

    def __update_record(self,column,value):
        return Database.query(f"UPDATE customer SET '{column}' = '{value}' WHERE customer_ID == {self.__customer_ID}")

    def __str__(self):
        return f"{self.__customer_ID , self.__name, self.__email, self.__password, self.__creditcard}"


class Reservation:

    def __init__(self,*attributes):
        self.__reservation_ID, \
        self.__customer_ID, \
        self.__startdate, \
        self.__enddate,\
        self.__totalfees, \
        self.__isCheckedin ,\
        self.__period   = attributes

    def getReservation_ID(self):
        return self.__reservation_ID
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

    def create_record(self,customer_ID):
        error = Database.query(f"INSERT INTO customer VALUES(?,?,?,?,?,?,?)",
        [self.__reservation_ID,self.__customer_ID,self.__startdate,self.__enddate,self.__totalfees,self.__isCheckedin ,self.__period])

        self.__reservation_ID = Database.query(f"SELECT reservation_ID FROM reservations WHERE customer_ID == '{customer_ID}' ")[-1][0]
        return error

    def delete_record(self):
        Database.query(f"DELETE FROM reservations WHERE reservation_ID == {self.__reservation_ID}")


class Pre_paid(Reservation):

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
