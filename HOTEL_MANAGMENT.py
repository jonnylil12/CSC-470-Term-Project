from system_core import *
import os
import smtplib ,ssl




def help():
    print("     Welcome to the Ophelia's Oasis Hotel Managment System\n"
          "------------------------------------------------------------------\n"
          "For more information on a specific command, type HELP command-name\n"
          
          "help                          Provides Help information for console commands.\n"
          "calender -S (input file)      saves data to database from inputfile in calenders folder\n"
          "reports -EI                   generates a expected income report and saves it to reports folder\n"
          "reports -EO                   generates a expected occupancy report and saves it to reports folder\n"
          "reports -I                    generates a incentive report and saves it to reports folder\n"
          "reports -DA                   generates a daily arrivals report and saves it to reports folder\n"
          "reports -DO                   generates a daily occupancy report and saves it to reports folder\n"
          "emails  -S                    generates and sends email reminders for sixtyday reservations\n")


def error(code,*args):

        if code == "program":
            print(f"\'{args[0]}\' is not recognized as an internal or external command\n"
                  "operable program or batch file.\n")

        elif code == "command":
            print(f"\nUsage:\n"
                  f"    {args[0]} <command> [options]\n"
                  f"\nno such option: {args[1]}\n")

        elif code == "file not found":
            print(f"ERROR No such file or directory: \\calenders\\{args[0]}\n")

        elif code == "file extension":
            print(f"ERROR input file must be a text file\n")

        elif code == "no input file":
            print("ERROR a inputfile must be provided")

        elif code == "invalid calender":
            print(f"ERROR  line {args[0]} has a invalid format")

        elif code == 'value':
            print(f"ERROR  invalid or missing penalty charge  ")

        else:
            print(f"That error code does not exist")




def calenders(command = '' ,inputfile = '',*_):
        if command.lower() != "-s" :
            error("command", "calenders", command)

        elif inputfile == '':
            error("no input file")

        elif inputfile == '':
            error("no input file")

        elif not inputfile.endswith(".txt"):
            error("file extension")

        elif not os.path.exists(os.path.abspath("calenders") + "\\" + inputfile):
            error("file not found", inputfile)

        else:
                filepath =  os.path.abspath("calenders") + "\\" + inputfile
                with open(filepath) as file:
                    for num , line in enumerate(file):
                        line = line.strip("\n").split()
                        if line != []:
                            try:
                                system_str_to_date(line[0])
                            except Exception:
                                error("invalid calender",num)
                            else:
                                Calender.setBaserate( line[0], float(line[1]) )


                Calender.save_calender()




def emails(command = '',*_):

        if command.lower() != "-s":
            error("command", "emails", command)

        else:
            all_unpayed = Database.load_object("SELECT * FROM reservation " +
                                                "WHERE type == 'sixtyday' " +
                                                "AND checkedin IS NOT NULL "
                                                "AND paydate IS NULL",
                                                Reservation)

            if all_unpayed != []:
                for reservation in all_unpayed:
                    from_start_45  = system_str_to_date(reservation.getStartdate()) - timedelta(days=45)
                    from_start_30 = system_str_to_date(reservation.getStartdate())  - timedelta(days=30)

                    if from_start_45 <= date.today() <= from_start_30:
                            name , email = Database.query("SELECT name , email FROM customer " +
                                                          f"WHERE ID == '{reservation.getCustomer_ID()}' ")[0]

                            port , username ,password = 465 ,'hotelmanagment470@gmail.com' ,'employee470'
                            message = f"""Subject: Payment Reminder\n\n
                                       Greetings {name},

                                       This is a reminder to pay for you reservation 
                                       within 15 days or else it will be cancelled

                                       Thank you.

                                       This is an automated email , please do not reply          
                                       """
                            print(name,email)
                            with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
                                server.login(username, password)
                                server.sendmail(username, email, message)




def  contextmanager(func):

        def wrapper(report_type):
            current = date.today()
            filepath = f"{os.path.abspath('reports')}\\{system_date_to_str(current)}  {report_type}"
            with open(f"{filepath}.txt", "w") as output_file:
                func(current,output_file)

        return wrapper



@contextmanager
def generatExpectedIncome(current,output_file):
        total_period_income = 0
        for _ in range(30):
            total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                              f"WHERE date == '{system_date_to_str(current)}'")[0][0]

            total_day_income = (total_day_income if total_day_income != None else 0.00)

            output_file.write(f"Date: {system_date_to_str(current)}    total income: ${total_day_income:.2f}\n")
            total_period_income += total_day_income
            current += timedelta(days=1)

        average_period_income = total_period_income / 30
        output_file.write(f"Total period income:      ${total_period_income:,.2f}\n")
        output_file.write(f"Average period income:    ${average_period_income:,.2f}")





@contextmanager
def generatExpectedOccupancy(current,output_file):

     total_period_occupancy = 0
     for _ in range(30):
         all_results  =    Database.query(f"SELECT type , count(*) FROM reservation " +
                                          f"WHERE startdate <= '{system_date_to_str(current)}' " +
                                          f"AND '{system_date_to_str(current)}' < enddate " +
                                          "AND checkedin IS NOT NULL " +
                                          f"GROUP BY type")

         all_results = ( dict(all_results) if all_results != [] else {} )

         prepaid = all_results.get("prepaid", 0)
         sixtyday = all_results.get("sixtyday", 0)
         conventional = all_results.get("conventional", 0)
         incentive = all_results.get("incentive", 0)
         total_day_occupancy = 45 - Calender.getRooms(system_date_to_str(current))

         output_file.write(f"Date: {system_date_to_str(current)}    Prepaid: {prepaid}    " +
                           f"Sixtyday: {sixtyday}   Conventional: {conventional}    " +
                           f"Incentive: {incentive}    Total: {total_day_occupancy}\n")

         total_period_occupancy += total_day_occupancy
         current += timedelta(days=1)

     average_period_occupancy = total_period_occupancy / 30
     occupancy_rate = average_period_occupancy / 45
     output_file.write(f"Occupancy rate: {occupancy_rate:.2%}")





@contextmanager
def generateExpectedIncentive(current,output_file):

    total_period_discount = 0
    for _ in range(30):
        total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                          f"WHERE date == '{system_date_to_str(current)}'")[0][0]

        total_day_discount = (total_day_income if total_day_income != None else 0.00) * 0.20

        output_file.write(f"Date: {system_date_to_str(current)}    " +
                         f"total incentive discount: ${total_day_discount:,.2f}\n")

        total_period_discount += total_day_discount
        current += timedelta(days=1)

    average_period_incentive_discount = total_period_discount / 30
    output_file.write(f"Total period incentive discount: ${total_period_discount:,.2f}\n")
    output_file.write(f"Average period incentive discount: ${average_period_incentive_discount:,.2f}")





@contextmanager
def generateDailyArrivals(current,output_file):
    all_results = Database.query("SELECT name, type, roomnumber, enddate " +
                                 "FROM reservation r , customer c " +
                                 f"WHERE startdate == '{system_date_to_str(current)}' " +
                                 "AND c.ID == customer_ID " +
                                 "AND checkedin == True " +
                                 "ORDER BY name ASC")
    if all_results != []:
        for name, Type, roomnumber, enddate in all_results:
            output_file.write(f"Name: {name}    Type: {Type}   " +
                              f"Room number: {roomnumber}    Departure date: {enddate}\n")
    else:
        output_file.write("No Daily Arrivals")




@contextmanager
def generateDailyOccupancy(current,output_file):
    all_results = Database.query("SELECT name, roomnumber, enddate " +
                                 "FROM reservation r , customer c " +
                                 f"WHERE startdate < '{system_date_to_str(current)}' " +
                                 "AND c.ID == customer_ID " +
                                 "AND checkedin == True " +
                                 "ORDER BY roomnumber ASC")

    if all_results != []:
        for name, roomnumber, enddate in all_results:
            if system_date_to_str(current) == enddate:  # user leaves that day
                output_file.write(f"Name: *{name}    Room number: {roomnumber}    Departure date: {enddate}\n")
            else:
                output_file.write(f"Name: {name}    Room number: {roomnumber}    Departure date: {enddate}\n")
    else:
        output_file.write("No Daily Occupants")






def reports(command='', *_):

    if command.lower() == "-ei":
        generatExpectedIncome("Expected income")
    elif command.lower() == "-eo":
        generatExpectedOccupancy("Expected Occupancy")
    elif command.lower() == "-i":
        generateExpectedIncentive("Expected Incentive")
    elif command.lower() == "-da":
        generateDailyArrivals("Daily Arrivals")
    elif command.lower() == "-do":
        generateDailyOccupancy("Daily Occupancy")
    else:
        error("command", "reports", command)



def main():
        while True:
            # get latest calender data
            Calender.load_calender()

            system_remove_noshows()  # remove reservations that havent checked in and its past startdate
            system_remove_unpayed()  # remove sixtydays that havent payed and its pass grace period
            system_remove_notlefted()  # remove reservations that havent been checked out and its past enddate

            args = input("HotelManagment>").split()

            if args == []:
                pass

            elif args[0] == "help":
                help()

            elif args[0] == "calenders":
                calenders(*args[1:])

            elif args[0] == "reports":
                reports(*args[1:])

            elif args[0] == "emails":
                emails(*args[1:])

            else:
                error("program",*args)


if __name__ == "__main__":
    os.makedirs(os.path.dirname("calenders\\_.txt"), exist_ok=True)
    os.makedirs(os.path.dirname("reports\\_.txt"), exist_ok=True)
    main()
