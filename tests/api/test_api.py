import requests
import pandas as pd

def get_crash_details(crash_id):
    r = requests.get(f"http://127.0.0.1:8000/v1/accidents/{crash_id}")
    return r

def stringify_id(id:int):
    if len(str(id)) == 5:
        return "0" + str(id)
    return str(id)

# 2023
def test_crash_details():
    crashes = pd.read_csv('../../data/csvs/1984/ACCIDENT.CSV', encoding='latin-1')
    for crash_id in crashes['ST_CASE']:
        r = get_crash_details("1984" + stringify_id(crash_id))
        assert r.status_code == 200, f"assertion failed for id: {stringify_id(crash_id)} ---- STACKTRACE {r.text}"
    # break
        


    # for year in range(1986,1997):
    #     more_factors = True
    #     offset = 0
    #     while more_factors:
    #         link = f"http://127.0.0.1:8000/v1/person_related_factors?person__accident__year={year}&limit=100&offset={offset}"
    #         r = requests.get(link)
    #         assert r.status_code == 200, f"assertion failed for id: {link} ---- STACKTRACE {r.text}"
    #         if len(r.json()['items']) == 0:
    #             more_factors = False
    #         offset += 100