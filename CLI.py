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

        if command.lower() == "-s" :

            if inputfile == '':
                CLI.error("no input file")

            elif not inputfile.endswith(".txt"):
                CLI.error("file extension")

            elif not os.path.exists(os.path.abspath("calenders") + "\\" + inputfile):
                CLI.error("file not found", inputfile)

            else:
                with open(os.path.abspath("calenders") + "\\" +  inputfile) as file:
                    for x , line in enumerate(file.readlines()):
                        line = line.strip("\n").split()
                        try:
                            if line != []:
                                date , baserate , rooms = line
                                Calender.setData(date_to_string(string_to_date(date)),float(baserate),int(rooms))
                        except Exception:
                            CLI.error("invalid calender",x)


                Calender.save_calender()

        else:
            CLI.error("command", "calenders",command)


    @staticmethod
    def reports(command = '',*_):
        current = date.today()
        if command.lower() == "-ei":
            CLI.__generatExpectedIncome(current)
        elif command.lower() == "-eo":
            CLI.__generatExpectedOccupancy(current)
        elif command.lower() == "-i":
                pass
        elif command.lower() == "-da":
                pass
        elif command.lower() == "-do":
                pass
        else:
            CLI.error("command", "reports", command)



    @staticmethod
    def __generatExpectedIncome(current):
         filepath = os.path.abspath('reports') + '\\' + current.strftime('%m-%d-%y') + ".Expected Income"
         with open(f"{filepath}.txt","w") as file:
             total_period_income = 0
             for _ in range(30):
                  day = current.strftime('%m-%d-%y')
                  total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                                   f"WHERE date == '{day}'")[0][0]

                  total_day_income = (0.00 if total_day_income == None else total_day_income)

                  file.write(f"Date: {day} total income: ${format(total_day_income, '.2f')}\n")
                  total_period_income += total_day_income
                  current += timedelta(days=1)

             file.write(f"total period income: ${format(total_period_income, '.2f')}\n")
             file.write(f"average period income: ${format(total_period_income / 30, '.2f')}")



    @staticmethod
    def __generatExpectedOccupancy(current):
        filepath = os.path.abspath('reports') + '\\' + current.strftime('%m-%d-%y') + ".Expected Occupancy"
        with open(f"{filepath}.txt", "w") as file:
            total_period_occupancy = 0
            for _ in range(30):
                day = current.strftime('%m-%d-%y')
                prepaid = Database.query(f"SELECT count(*) FROM reservation "  +
                                         "WHERE type == 'prepaid' " +
                                         f"AND '{day}' BETWEEN startdate and enddate")[0][0]

                sixtyday = Database.query(f"SELECT count(*) FROM reservation "  +
                                           "WHERE type == 'sixtyday' " +
                                           f"AND '{day}' BETWEEN startdate and enddate")[0][0]

                conventional = Database.query(f"SELECT count(*) FROM reservation "  +
                                             "WHERE type == 'conventional' " +
                                             f"AND '{day}' BETWEEN startdate and enddate")[0][0]

                incentive = Database.query(f"SELECT count(*) FROM reservation "  +
                                             "WHERE type == 'incentive' " +
                                             f"AND '{day}' BETWEEN startdate and enddate")[0][0]

                total_day_occupancy = prepaid + sixtyday + conventional + incentive


                file.write(f"Date: {day}  " +
                           f"prepaid: {prepaid}   sixtyday: {sixtyday}   " +
                           f"conventional: {conventional}   incentive: {incentive}   " +
                           f"total: {total_day_occupancy}\n")

                total_period_occupancy += total_day_occupancy
                current += timedelta(days=1)

            file.write(f"average period occupancy: {format(total_period_occupancy / 30, '.2f')}")


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
