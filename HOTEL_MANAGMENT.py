from system_procedures import *
from system_objects import *
import os





def help():
    print("     Welcome to the Ophelia's Oasis Hotel Managment System\n"
          "------------------------------------------------------------------\n"
          "For more information on a specific command, type HELP command-name\n"
          "help                        Provides Help information for console commands.\n"
          "calender -S (inputfile)     saves data to database from inputfile in calenders folder\n"
          "reports -EI                 generates a expected income report and saves it to reports folder\n"
          "reports -EO                 generates a expected occupancy report and saves it to reports folder\n"
          "reports -I                  generates a incentive report and saves it to reports folder\n"
          "reports -DA                 generates a daily arrivals report and saves it to reports folder\n"
          "reports -DO                 generates a daily occupancy report and saves it to reports folder\n")


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

        elif code =="invalid calender":
            print(f"ERROR  line {args[0]} has a invalid format")



def  contextmanager(func):

    def wrapper(report_type):

        current = date.today()
        # testing purposes
        # current = string_to_date("10-02-21")
        filepath = f"{os.path.abspath('reports')}\\{date_to_str(current)}  {report_type}"
        with open(f"{filepath}.txt", "w") as file:
            func(current, file)

    return wrapper



def calenders(command = '' ,inputfile = '',*_):
        if command.lower() == "-s" :

            if inputfile == '':
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
                                Calender.setBaserate(date_to_str(str_to_date(line[0])), float(line[1]))
                            except Exception:
                                error("invalid calender",num)

                Calender.save_calender()

        else:
            error("command", "calenders",command)




@contextmanager
def generatExpectedIncome(current,file):
        total_period_income = 0
        for _ in range(30):
            total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                              f"WHERE date == '{date_to_str(current)}'")[0][0]

            total_day_income = (0.00 if total_day_income == None else total_day_income)

            file.write(f"Date: {date_to_str(current)}    total income: ${total_day_income:.2f}\n")
            total_period_income += total_day_income
            current += timedelta(days=1)

        average_period_income = total_period_income / 30
        file.write(f"Total period income:      ${total_period_income:.2f}\n")
        file.write(f"Average period income:    ${average_period_income:.2f}")



@contextmanager
def generatExpectedOccupancy(current,file):
     total_period_occupancy = 0
     for _ in range(30):
         all_results = Database.query(f"SELECT type , count(*) FROM reservation " +
                                      f"WHERE '{date_to_str(current)}' " +
                                      f"BETWEEN startdate AND enddate " +
                                      f"GROUP BY type")

         convert = {type[0]: type[1] for type in all_results}

         prepaid = convert.get("prepaid", 0)
         sixtyday = convert.get("sixtyday", 0)
         conventional = convert.get("conventional", 0)
         incentive = convert.get("incentive", 0)
         total_day_occupancy = 45 - Calender.getRooms(date_to_str(current))

         file.write(f"Date: {date_to_str(current)}    Prepaid: {prepaid}    " +
                    f"Sixtyday: {sixtyday}   Conventional: {conventional}    " +
                    f"Incentive: {incentive}    Total: {total_day_occupancy}\n")

         total_period_occupancy += total_day_occupancy
         current += timedelta(days=1)

     average_period_occupancy = total_period_occupancy / 30
     occupancy_rate = average_period_occupancy / 45
     file.write(f"Occupancy rate: {occupancy_rate:.2%}")




@contextmanager
def generateExpectedIncentive(current,file):
    total_period_incentive_discount = 0
    for _ in range(30):
        total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                          f"WHERE date == '{date_to_str(current)}'")[0][0]

        total_incentive_discount = (0.00 if total_day_income == None else total_day_income) * 0.20

        file.write(f"Date: {date_to_str(current)}    " +
                   f"total incentive discount: ${total_incentive_discount:.2f}\n")

        total_period_incentive_discount += total_incentive_discount
        current += timedelta(days=1)

    average_period_incentive_discount = total_period_incentive_discount / 30
    file.write(f"Total period incentive discount: ${total_period_incentive_discount:.2f}\n")
    file.write(f"Average period incentive discount: ${average_period_incentive_discount:.2f}")





@contextmanager
def generateDailyArrivals(current,file):
    all_results = Database.query("SELECT (SELECT name FROM customer WHERE ID == r.customer_ID ), " +
                                 "type, roomnumber, enddate " +
                                 "FROM reservation r " +
                                 f"WHERE startdate == '{date_to_str(current)}' " +
                                 "AND roomnumber IS NOT NULL " +
                                 "ORDER BY name ASC")
    if all_results != []:
        for name, Type, roomnumber, enddate in all_results:
            file.write(f"Name: {name}    Type: {Type}   " +
                       f"Room number: {roomnumber}    Departure date: {enddate}\n")
    else:
        file.write("No Daily Arrivals")



@contextmanager
def generateDailyOccupancy(current,file):
    all_results = Database.query("SELECT (SELECT name FROM customer WHERE ID == r.customer_ID ), " +
                                 "roomnumber, enddate " +
                                 "FROM reservation r " +
                                 f"WHERE startdate < '{date_to_str(current)}' " +
                                 "AND roomnumber IS NOT NULL " +
                                 "ORDER BY roomnumber ASC")

    if all_results != []:
        for name, roomnumber, enddate in all_results:
            if date_to_str(current) == enddate:  # user leaves that day
                file.write(f"Name: *{name}    Room number: {roomnumber}    Departure date: {enddate}\n")
            else:
                file.write(f"Name: {name}    Room number: {roomnumber}    Departure date: {enddate}\n")
    else:
        file.write("No Daily Occupants")





def reports(command='', *_):

    if command.lower() == "-ei":
        generatExpectedIncome("Expected Income")
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

            args = input("HotelManagment>").split()

            if args == []:
                pass

            elif args[0] == "help":
                help()

            elif args[0] == "calenders":
                calenders(*args[1:])

            elif args[0] == "reports":
                reports(*args[1:])

            else:
                error("program",*args)


if __name__ == "__main__":
    os.makedirs(os.path.dirname("calenders\\_.txt"), exist_ok=True)
    os.makedirs(os.path.dirname("reports\\_.txt"), exist_ok=True)
    main()
