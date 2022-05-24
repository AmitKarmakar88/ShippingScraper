import pandas as pd
from selenium import webdriver
import os
from time import sleep
from bs4 import BeautifulSoup as BS
import numpy as np
from collections import OrderedDict
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import date, timedelta
from selenium.webdriver import ActionChains
import time
from datetime import datetime, timedelta,date

#FOR HEADLESS BROWSER
from selenium.webdriver.chrome.options import Options

start_time = time.time()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
import os
import re
# from send_mail import send_email


Calendra_dict={'jan':1,'feb':2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

def Date_new(x):
    if len(x)>3:
        x=x.split('/')
        # print(x)
        if len(x)==3:
            # print(str(Calendra_dict[x[1][0:3].strip().lower()]))
            return x[0]+'/'+str(Calendra_dict[x[1].strip().lower()])+'/'+x[-1]
        else:
            return ''   
    else:
        return ''

def port_code_substring(x):
    x=re.sub('[^A-Za-z(), ]+',' ', x)
    
    if len(x.split(','))>1:
        x=x.split(',')[0].strip()
        return x.lower()
        
        #now remove white space and comma
    
    elif len(x.split(' '))>1:
        x=x.split(' ')[0].strip()

        return x.lower()
        
    
    elif '(' in x:
        x=re.sub(r'\([^)]*\)', '', x)
        return x.lower()
    elif len(x)>3:
        return x.lower()
    else:
        return "NA"

# try:
url="https://libertygl.com/schedule#planning"

#driver = webdriver.Firefox()
# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

#for local running on windows uncomment above line if using linux and commen below line of code
# driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)
driver.get(url)    # Opening the submission url

sleep(25)

data_dict={}
data_dict['Vessel Name']=[]
data_dict['Voyage Number']=[]
data_dict['Port Name']=[]
data_dict['Carrier']=[]
data_dict['Date of Arrival (ETA)']=[]
data_dict['Date of Departure (ETD)']=[]
data_dict['Route Code']=[]
data_dict['Vessel Capacity (in MT)']=[]
data_dict['Vessel Ramp Height (in meters)']=[]


el = driver.find_element_by_id("route")
for option in el.find_elements_by_tag_name('option')[1:3]:
    option.click() # select() in earlier versions of webdriver
    print(option.text)

    sleep(25)
    result_div= driver.find_element_by_class_name("port-result")

    #first header 
    PortName=[]
    VoyageNo=[]
    VasselName=[]



    columns_name=result_div.find_element_by_class_name("first")
    port_head=columns_name.find_elements_by_class_name("arrival-port-name")
    for ports in port_head:
        port_name = ports.get_attribute('innerHTML').strip()
        print(port_name)
        PortName.append(port_name)



    #1st to end columns
    columns=result_div.find_elements_by_class_name("col")[1:-1]

    for column_data in columns:
        vassel_name,Voyage_no=column_data.find_element_by_class_name("ship-name").text.split('/')
        #print(vassel_name,Voyage_no)
        VoyageNo.append(Voyage_no)
        VasselName.append(vassel_name)




    for column_data in columns:
        iterate=0
        vassel_name,Voyage_no=column_data.find_element_by_class_name("ship-name").text.split('/')
        dateTimeRow=column_data.find_elements_by_class_name("arrival-cutoff")
        for dateTime in dateTimeRow:
            etaData= dateTime.find_element_by_class_name("eta")
            cutoffData= dateTime.find_element_by_class_name("cutoff")
            etaData=etaData.text.split('\n')
            cutoffData=cutoffData.text.split('\n')
            
            if len(etaData)==2:
                Day=etaData[-1]
                month=etaData[0].split()[0]
                Year=etaData[0].split()[1]
                ETA=Date_new(Day+'/'+month+'/'+Year)
            else:
                ETA=''
                
            if len(cutoffData)==2:
                Day=cutoffData[-1]
                month=cutoffData[0].split()[0]
                Year=cutoffData[0].split()[1]
                ETD=Date_new(Day+'/'+month+'/'+Year)
            else:
                ETD=''
                
            # print("vassel_name="+vassel_name)
            # print("Voyage_no="+Voyage_no)
            # print("portName="+PortName[iterate])
            # print("ETA="+ETA)
            # print("ETD="+ETD)
            
            data_dict['Vessel Name'].append(vassel_name)
            data_dict['Voyage Number'].append(Voyage_no)
            data_dict['Port Name'].append(PortName[iterate])
            data_dict['Carrier'].append("LIBERTY GLOBAL LOGISTICS")
            data_dict['Date of Arrival (ETA)'].append(ETA)
            data_dict['Date of Departure (ETD)'].append(ETD)
            data_dict['Route Code'].append("NA")
            data_dict['Vessel Capacity (in MT)'].append("NA")
            data_dict['Vessel Ramp Height (in meters)'].append("NA")
            
            iterate+=1
        print("****************** end *******************")

    sleep(10)

MasterDf=pd.DataFrame(data_dict)


port_df=pd.read_csv("port.csv")

port_list=[]
for index,row in MasterDf.iterrows():
    port_name=port_code_substring(row['Port Name']) 
    if port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)].shape[0]>0:
        portCode=port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)]['CODE'].values
        # print('len=',len(port_name),port_name,portCode[0])
        port_list.append(portCode[0])
    else:
        # print('len=',len(port_name),'NO-----------------')
        port_list.append("NA")


MasterDf['port_code']=np.array(port_list)

MasterDf=MasterDf.replace("NA",'')
# MasterDf['Date of Arrival (ETA)']=MasterDf['Date of Arrival (ETA)'].apply(lambda x:Date_new(x))
# MasterDf['Date of Departure (ETD)']=MasterDf['Date of Departure (ETD)'].apply(lambda x:Date_new(x))
MasterDf=MasterDf[['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)','Date of Departure (ETD)']]


MasterDf.to_csv("LGL.csv",index=False)


# except Exception as e:
#     print(e)
#     pass

driver.close();
driver.quit();