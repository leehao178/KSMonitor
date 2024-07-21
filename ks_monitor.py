# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

from tabulate import tabulate
import time
import requests
import json
import csv
import os

# Fonction pour ajouter des couleurs
def colorize(text, condition):
    if condition:
        return f'\033[92m{text}\033[0m'  # Vert
    else:
        return f'\033[91m{text}\033[0m'  # Rouge


def Average(lst): 
    return sum(lst) / len(lst) 


def extract_data(ip, csvdata):
    url = f'http://{ip}/user/userpanel'

    res = requests.post(url, data={'post': 4})

    monitorDataDict = json.loads(res.text)['data']

    url = f'http://{ip}/user/timeseries?series=hashrate'
    res = requests.get(url)
    hs = json.loads(res.text)['ret']['series']

    # print(hs[-1][0])
    # print(monitorDataDict['host'])

    host = monitorDataDict['host']

    url = f'http://{ip}/user/timeseries?series=chiptemp'
    res = requests.get(url)
    chiptemp = json.loads(res.text)['ret']['series']

    chiptempMax = max(chiptemp[-1][0])
    chiptempMiN = min(chiptemp[-1][0])
    chiptempAvg = Average(chiptemp[-1][0])


    url = f'http://{ip}/user/timeseries?series=boardtemp'
    res = requests.get(url)
    boardtemp = json.loads(res.text)['ret']['series']

    boardtempIntake = boardtemp[-1][0][0]
    boardtempExhust = boardtemp[-1][0][1]
    boardtempMax = boardtemp[-1][0][2]


    url = f'http://{ip}/user/timeseries?series=chipclock'
    res = requests.get(url)
    chipclock = json.loads(res.text)['ret']['series']
    chipclockAvg = Average(chipclock[-1][0])

    url = f'http://{ip}/user/timeseries?series=chipvoltage'
    res = requests.get(url)
    chipvoltage = json.loads(res.text)['ret']['series']
    chipvoltageAvg = Average(chipvoltage[-1][0])


    url = f'http://{ip}/user/timeseries?series=fanrpm'
    res = requests.get(url)
    fanrpm = json.loads(res.text)['ret']['series']
    fanrpm1 = fanrpm[-1][0]
    fanrpm2 = fanrpm[-1][1]


    fiveminshashrate = hs[-1][0]
    networkstatus = monitorDataDict['online']


    data = [ip, host, fiveminshashrate, networkstatus, fanrpm1, fanrpm2, boardtempIntake, boardtempExhust, chiptempAvg, chipvoltageAvg, chipclockAvg]
    results = []
    results.append(data)

    csvdata += [f'{ip}.{host}', fiveminshashrate, fanrpm1, fanrpm2, boardtempIntake, boardtempExhust, boardtempMax, chiptempMax, chiptempMiN, chiptempAvg, chipvoltageAvg, chipclockAvg]

    headers = ['IP', 'Name', '5 Min HS(G)', 'Status', 'Fan1', 'Fan2', 'B InTemp(C)', 'B ExTemp(C)', 'C Temp(C)', 'C Voltage', 'C Freq']


    print(tabulate(results, headers=headers, tablefmt='grid'))
    
    
    return csvdata


if __name__ == '__main__':

    with open('iplist.txt', 'r') as f:
        ips = f.readlines()
    for i in range(2):
        new = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        csvdata = [new]

        if os.path.isfile('output.csv') == False:
            isfile = False
        with open('output.csv', 'a', newline='') as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile)
            if isfile == False:
                title = ['Time']
                for idx, ip in enumerate(ips):
                    title += [f'{idx + 1}_Miner', f'{idx + 1}_Hashrate', f'{idx + 1}_Fan1', f'{idx + 1}_Fan2', f'{idx + 1}_BtempIntake', f'{idx + 1}_BtempExhust', f'{idx + 1}_BtempMax', f'{idx + 1}_CtempMax', f'{idx + 1}_CtempMiN', f'{idx + 1}_CtempAvg', f'{idx + 1}_CvoltageAvg', f'{idx + 1}_CclockAvg']
                writer.writerow(title)
                isfile = True
            for ip in ips:
                csvdata = extract_data(ip=ip.strip(), csvdata=csvdata)
            # 寫入一列資料
            writer.writerow(csvdata)
        time.sleep(300)