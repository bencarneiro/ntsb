from django.core.management.base import BaseCommand
from fatalities.models import State, Accident
import csv

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        states = State.objects.all()
        for s in states:
            print(s.name)
            print(s.id)
            # Write CSV file
            print("total")
            with open(f"../population/csvs/total/total_{s.id}.csv", "wt") as fp:
                state_crashes = Accident.objects.filter(state=s)
                writer = csv.writer(fp, delimiter=",")
                writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])
                # writer.writerow(["your", "header", "foo"])  # write header
                for crash in state_crashes:
                    writer.writerow([crash.st_case, crash.fatalitytotals.total_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])
            print("vehicle")
            with open(f"../population/csvs/vehicle/vehicle_{s.id}.csv", "wt") as fp:
                state_crashes = Accident.objects.filter(state=s, fatalitytotals__vehicle_fatalities__gte=1)
                writer = csv.writer(fp, delimiter=",")
                writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])
                # writer.writerow(["your", "header", "foo"])  # write header
                for crash in state_crashes:
                    writer.writerow([crash.st_case, crash.fatalitytotals.vehicle_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])
            print("nonmotorist")
            with open(f"../population/csvs/nonmotorist/nonmotorist_{s.id}.csv", "wt") as fp:
                state_crashes = Accident.objects.filter(state=s, fatalitytotals__nonmotorist_fatalities__gte=1)
                writer = csv.writer(fp, delimiter=",")
                writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])
                # writer.writerow(["your", "header", "foo"])  # write header
                for crash in state_crashes:
                    writer.writerow([crash.st_case, crash.fatalitytotals.nonmotorist_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])
            # break
        # wrecks = Accident.objects.all()
        # for w in wrecks:


        # Define data
        # data = [
        #     (1, "A towel,", 1.0),
        #     (42, " it says, ", 2.0),
        #     (1337, "is about the most ", -1),
        #     (0, "massively useful thing ", 123),
        #     (-2, "an interstellar hitchhiker can have.", 3),
        # ]

        # # Write CSV file
        # with open("test.csv", "wt") as fp:
        #     writer = csv.writer(fp, delimiter=",")
        #     # writer.writerow(["your", "header", "foo"])  # write header
        #     writer.writerows(data)




# def total_csv_all_years(request):
#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": f'attachment; filename="total_fatalities_all_years.csv"'},
#     )

#     writer = csv.writer(response)
#     writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

#     crashes = Accident.objects.filter(state=State.objects.all()[0])
#     for crash in crashes:
#         writer.writerow([crash.st_case, crash.fatalitytotals.total_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

#     return response



# def vehicle_csv_all_years(request):
#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": f'attachment; filename="total_fatalities_all_years.csv"'},
#     )

#     writer = csv.writer(response)
#     writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

#     crashes = Accident.objects.all()
#     for crash in crashes:
#         writer.writerow([crash.st_case, crash.fatalitytotals.vehicle_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

#     return response


# def nonmotorist_csv_all_years(request):
#     response = HttpResponse(
#         content_type="text/csv",
#         headers={"Content-Disposition": f'attachment; filename="total_fatalities_all_years.csv"'},
#     )

#     writer = csv.writer(response)
#     writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

#     crashes = Accident.objects.all()
#     for crash in crashes:
#         writer.writerow([crash.st_case, crash.fatalitytotals.nonmotorist_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

#     return response
