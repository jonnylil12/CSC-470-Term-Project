from objects import *
import os


class CLI:

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
                    for x , line in enumerate(file.readlines()[:-2]):
                        try:
                            date, baserate, rooms = line.strip("\n").split()
                            Calender.setData(datetime.strptime(date,"%m-%d-%y"),float(baserate),int(rooms))
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
                pass
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
         current = datetime.strptime("10-08-21",'%m-%d-%y').date()
         filepath = os.path.abspath('reports') + '\\' + current.strftime('%m-%d-%y')


         with open(f"{filepath}.txt","w") as file:
             total_period_income = 0
             for _ in range(30):
                  total_day_income = Database.query(f"SELECT sum(rate) FROM day "
                                                   f"WHERE date == '{current.strftime('%m-%d-%y')}'")[0][0]
                  if total_day_income != None:
                       file.write(f"Date: {current} total income: ${format(total_day_income, '.2f')}\n")
                       total_period_income += total_day_income
                  current += timedelta(days=1)

             file.write(f"total period income: ${format(total_period_income, '.2f')}\n")
             file.write(f"total average income ${format(total_period_income / 30, '.2f')}")



    @staticmethod
    def error(code,*args):
        if code == "program":
            print(f"\'{args[0]}\' is not recognized as an internal or external command\n"
                  "operable program or batch file.\n")

        elif code == "command":
            print(f"Usage:\n"
                  f"    {args[0]} <command> [options]\n"
                  f"\nno such option: {args[1]}\n")

        elif code == "file not found":
            print(f"ERROR No such file or directory: \\{args[1]}\\{args[2]}\n")

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
                CLI.error("program",*args[1:])



if __name__ == "__main__":
    os.makedirs(os.path.dirname("calenders\\x.txt"), exist_ok=True)
    os.makedirs(os.path.dirname("reports\\x.txt"), exist_ok=True)
    CLI.main()
