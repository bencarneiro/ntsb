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
    crashes = pd.read_csv('../../data/csvs/2020/FARS2020NationalCSV/accident.csv', encoding='latin-1')[10900:]
    for crash_id in crashes['ST_CASE']:
        r = get_crash_details("2020" + stringify_id(crash_id))
        assert r.status_code == 200, f"assertion failed for id: {stringify_id(crash_id)} ---- STACKTRACE {r.text}"
    # break