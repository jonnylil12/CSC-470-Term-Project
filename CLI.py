from events import *
import os

class CLI:

    @staticmethod
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

    @staticmethod
    def calenders(command = '' ,inputfile = '',*_):
        # get latest calender data
        Calender.load_calender()

        if command.lower() == "-s" :

            if inputfile == '':
                CLI.error("no input file")

            elif not inputfile.endswith(".txt"):
                CLI.error("file extension")

            elif not os.path.exists(os.path.abspath("calenders") + "\\" + inputfile):
                CLI.error("file not found", inputfile)

            else:
                filepath =  os.path.abspath("calenders") + "\\" + inputfile
                with open(filepath) as file:
                    for num , line in enumerate(file):
                        line = line.strip("\n").split()
                        if line != []:
                            try:
                                Calender.setBaserate(date_to_string(string_to_date(line[0])), float(line[1]))
                            except Exception:
                                CLI.error("invalid calender",num)

                Calender.save_calender()

        else:
            CLI.error("command", "calenders",command)


    @staticmethod
    def reports(command = '',*_):
        #get latest calender data
        Calender.load_calender()
        current = date.today()

        if command.lower() == "-ei":
            CLI.__generatExpectedIncome(current)
        elif command.lower() == "-eo":
            CLI.__generatExpectedOccupancy(current)
        elif command.lower() == "-i":
            CLI.__generateExpectedIncentive(current)
        elif command.lower() == "-da":
            CLI.__generateDailyArrivals(current)
        elif command.lower() == "-do":
            CLI.__generateDailyOccupancy(current)
        else:
            CLI.error("command", "reports", command)



    @staticmethod
    def __generatExpectedIncome(current):
         #testing
         current = datetime.strptime("10-01-21","%m-%d-%y").date()
         filepath = os.path.abspath('reports') + '\\' + date_to_string(current) + ".Expected Income"

         with open(f"{filepath}.txt","w") as file:
             total_period_income = 0
             for _ in range(30):
                  current_date = date_to_string(current)
                  total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                                   f"WHERE date == '{current_date}'")[0][0]

                  total_day_income = (0.00 if total_day_income == None else total_day_income)

                  file.write(f"Date: {current_date} total income: ${format(total_day_income, '.2f')}\n")
                  total_period_income += total_day_income
                  average_period_income = total_period_income / 30
                  current += timedelta(days=1)

             file.write(f"Total period income: ${format(total_period_income, '.2f')}\n")
             file.write(f"Average period income: ${format(average_period_income, '.2f')}")



    @staticmethod
    def __generatExpectedOccupancy(current):
        #testing
        current = datetime.strptime("10-01-21","%m-%d-%y").date()
        filepath = os.path.abspath('reports') + '\\' + date_to_string(current) + ".Expected Occupancy"

        with open(f"{filepath}.txt", "w") as file:
            total_period_occupancy = 0
            for _ in range(30):
                current_date = date_to_string(current)
                all_results = Database.query(f"SELECT type , count(*) FROM reservation " +
                                                           f"WHERE '{current_date}' BETWEEN startdate AND enddate " +
                                                           f"GROUP BY type")
                convert = {type[0]:type[1] for type in all_results}

                prepaid  = convert.get("prepaid",0)
                sixtyday  = convert.get("sixtyday",0)
                conventional = convert.get("conventional",0)
                incentive  =  convert.get("incentive",0)
                total_day_occupancy = 45 - Calender.getRooms(current_date)

                file.write(f"Date: {current_date}    Prepaid: {prepaid}    Sixtyday: {sixtyday}   " +
                           f"Conventional: {conventional}    Incentive: {incentive}    Total: {total_day_occupancy}\n")

                total_period_occupancy += total_day_occupancy
                average_period_occupancy = total_period_occupancy / 30
                occupancy_rate = average_period_occupancy / 45
                current += timedelta(days=1)

            file.write(f"Occupancy rate: {format(occupancy_rate, '.2f')}")


    @staticmethod
    def __generateExpectedIncentive(current):
        # testing
        current = datetime.strptime("10-01-21", "%m-%d-%y").date()
        filepath = os.path.abspath('reports') + '\\' + date_to_string(current) + ".Expected Incentive"

        with open(f"{filepath}.txt", "w") as file:
            total_period_incentive_discount = 0
            for _ in range(30):
                current_date = date_to_string(current)
                total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                                  f"WHERE date == '{current_date}'")[0][0]

                total_incentive_discount = (0.00 if total_day_income == None else total_day_income) * 0.20

                file.write(f"Date: {current_date} total incentive discount: ${format(total_incentive_discount, '.2f')}\n")
                total_period_incentive_discount +=  total_incentive_discount
                average_period_incentive_discount =  total_period_incentive_discount / 30
                current += timedelta(days=1)

            file.write(f"Total period incentive discount: ${format( total_period_incentive_discount, '.2f')}\n")
            file.write(f"Average period incentive discount: ${format(average_period_incentive_discount, '.2f')}")



    @staticmethod
    def __generateDailyArrivals(current):
        #testing
        current = datetime.strptime("10-01-21", "%m-%d-%y").date()
        filepath = os.path.abspath('reports') + '\\' + date_to_string(current) + ".Daily Arrivals"
        with open(f"{filepath}.txt", "w") as file:
            current_date = date_to_string(current)
            all_results = Database.query("SELECT (SELECT name FROM customer WHERE ID == r.customer_ID ), " +
                                        "type, roomnumber, enddate " +
                                        "FROM reservation r " +
                                        f"WHERE startdate == '{current_date}'"
                                        "AND roomnumber IS NOT NULL")
            if  all_results == []:
                file.write("No Daily Arrivals")
            else:
                for name , type , roomnumber , enddate in all_results:
                    file.write(f"Name: {name}    Type: {type}    Roomnumber: {roomnumber}    Enddate: {enddate}\n")


    @staticmethod #todo
    def __generateDailyOccupancy(current):
        pass

    @staticmethod
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


    @staticmethod
    def main():

        while True:
            args = input("HotelManagment>").split()

            if args == []:
                pass

            elif args[0] == "help":
                CLI.help()

            elif args[0] == "calenders":
                CLI.calenders(*args[1:])

            elif args[0] == "reports":
                CLI.reports(*args[1:])

            else:
                CLI.error("program",*args)



if __name__ == "__main__":
    os.makedirs(os.path.dirname("calenders\\_.txt"), exist_ok=True)
    os.makedirs(os.path.dirname("reports\\_.txt"), exist_ok=True)
    CLI.main()
