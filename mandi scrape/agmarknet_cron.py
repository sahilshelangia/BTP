import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
import os
import time
import json
from bs5 import *
import logging

lag = 0

#os.chdir('/home/ubuntu/pytfiles/')

with open('comm.json', 'r') as fp:
    commDict = json.load(fp)

import datetime as dt

cwd = os.getcwd()
logging.basicConfig(filename = cwd + r"/logscrape.log",level = logging.DEBUG)
logger = logging.getLogger()

    

# while True:
print('Start.')
da = dt.date.today()
diso = da.strftime('%Y-%m-%d')
diso="2019-01-05"
dliso = (da - dt.timedelta(lag)).strftime('%Y-%m-%d')
dliso="2019-01-05"
d = da.strftime("%d-%b-%Y")
d="2019-01-05"
lis = []

tries = 0

for code in commDict:
    print(commDict[code])
    try:
		
        initResp = getInitPage(diso,dliso,code,commDict[code])
        initSoup = soup(initResp,'lxml')
        initVS = initSoup.input.getText()
        if initVS == '':
            initVS = initSoup.input['value']

        #popLis(initSoup,lis)
        
        

        if str(initResp).find('Page$Next') != -1:
            nextP = getNextPage(d,initVS)
            vs = findViewState(str(nextP))
            #popLis(soup(nextP,'lxml'),lis)

            while str(nextP).find('Page$Next') != -1:
                vs = findViewState(str(nextP))
                nextP = getNextPage(d,vs)
               # popLis(soup(nextP,'lxml'),lis)


        # tonnage begin (does not take lag)
        for lagdur in range(lag+1):
            # diso = da.strftime('%Y-%m-%d')
            dlisoTon = (da - dt.timedelta(lagdur)).strftime('%Y-%m-%d')
            dlisoTon="2019-01-05"
            initResp = getInitPageTon(dlisoTon,dlisoTon,code,commDict[code])
            initSoup = soup(initResp,'lxml')
            initVS = initSoup.input.getText()
            if initVS == '':
                initVS = initSoup.input['value']
                
            popLisTon(initSoup,lis,commDict[code])
            exit()
        # tonnage end

        # print(commDict[code],len(lis),end = " ")
        logger.info(d + " done")
        
        send(lis)
        print('.',end = ' ')
        lis = []
    except Exception as e:
        tries += 1
        print(e)
        print("skipping ",commDict[code])
        if tries <= 100:
            continue
        else:
            print("Too much failure. breaking.")
            break

# df = pd.read_csv('sample.csv',usecols = ['TS'])
# l = df.shape[0]
# df.loc[l] = time.time()
# df.to_csv("sample.csv")
# time.sleep(7200)
