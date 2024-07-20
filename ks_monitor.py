from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tabulate import tabulate
import time
import requests
import json


# Fonction pour ajouter des couleurs
def colorize(text, condition):
    if condition:
        return f"\033[92m{text}\033[0m"  # Vert
    else:
        return f"\033[91m{text}\033[0m"  # Rouge

def Average(lst): 
    return sum(lst) / len(lst) 


def extract_data(ip):
    # url = f"http://{ip}/user/timeseries?series=hashrate"
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get(url)
    # html_content = driver.page_source
    # soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.text)

    url = f"http://{ip}/user/userpanel"
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    res = requests.post(url, data={'post': 4})

    monitorDataDict = json.loads(res.text)['data']

    url = f"http://{ip}/user/timeseries?series=hashrate"
    res = requests.get(url)
    hs = json.loads(res.text)['ret']['series']
    # print(hs[-1][0])
    # print(monitorDataDict)

    url = f"http://{ip}/user/timeseries?series=chiptemp"
    res = requests.get(url)
    chiptemp = json.loads(res.text)['ret']['series']

    chiptempMax = max(chiptemp[-1][0])
    chiptempMiN = min(chiptemp[-1][0])
    chiptempAvg = Average(chiptemp[-1][0])


    url = f"http://{ip}/user/timeseries?series=boardtemp"
    res = requests.get(url)
    boardtemp = json.loads(res.text)['ret']['series']

    boardtempIntake = boardtemp[-1][0][0]
    boardtempExhust = boardtemp[-1][0][1]
    boardtempMax = boardtemp[-1][0][2]


    url = f"http://{ip}/user/timeseries?series=chipclock"
    res = requests.get(url)
    chipclock = json.loads(res.text)['ret']['series']
    chipclockAvg = Average(chipclock[-1][0])

    url = f"http://{ip}/user/timeseries?series=chipvoltage"
    res = requests.get(url)
    chipvoltage = json.loads(res.text)['ret']['series']
    chipvoltageAvg = Average(chipvoltage[-1][0])


    url = f"http://{ip}/user/timeseries?series=fanrpm"
    res = requests.get(url)
    fanrpm = json.loads(res.text)['ret']['series']
    fanrpm1 = fanrpm[-1][0]
    fanrpm2 = fanrpm[-1][1]


    fiveminshashrate = hs[-1][0]
    networkstatus = monitorDataDict['online']


    data = [ip, fiveminshashrate, networkstatus, fanrpm1, fanrpm2, boardtempIntake, boardtempExhust, chipclockAvg, chipvoltageAvg, chipclockAvg]
    results = []
    results.append(data)

    headers = ['IP', '5 Min HS(G)', 'Status', 'Fan1', 'Fan2', 'B InTemp(C)', 'B ExTemp(C)', 'C Temp(C)', 'C Voltage', 'C Freq']


    print(tabulate(results, headers=headers, tablefmt="grid"))


if __name__ == '__main__':
    extract_data('192.168.51.11')