import os.path
start = 1
end = 90
total = 14801
while end < total:
    path = f"data/crash_data_2017__{start}_to_{end}_of_{total}.csv"
    if os.path.isfile(path):
        print("yes")
    else:
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOO")
    start += 90
    end += 90