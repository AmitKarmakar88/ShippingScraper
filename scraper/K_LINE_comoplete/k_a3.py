from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
import wget
import shutil
import wget
# import tabula
import os
import pandas as pd
import numpy as np
import urllib.request
from time import sleep
import re
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# monthYear={"jan":[1,2021],"feb":[2,2021],"mar":[3,2021],"apr":[4,2021],"may":[5,2021],"jun":[6,2021],"dec":[12,2020],"nov":[11,2020],"july":[7,2021]}

# def datetimeFunction(DateTime):
#     if DateTime=='Na':
#         return 'NA'
#     try:
#         if "*" in DateTime:
#             DateTime=DateTime.replace("*","")
        
#         DateTime=DateTime.split('-')
#         return DateTime[0]+'/'+str(monthYear[DateTime[1].lower()][0])+'/'+str(monthYear[DateTime[1].lower()][1])
#     except Exception as e:
#         print(e)
#         return 'NA'



monthYear={"1":2021,"2":2021,"3":2021,"4":2021,"5":2021,"6":2021,"7":2021,"8":2021,"9":2021,"10":2021,"11":2020,"12":2020}

def datetimeFunction(DateTime):
    if DateTime=='Na':
        return 'NA'
    try:
        Day=str(DateTime.day)
        Month=str(DateTime.month).lower()
        # print(Month)
        # DateTime=DateTime.split('-')
        return Day+'/'+Month+'/'+str(monthYear[Month])
    except Exception as e:
        # print(e)
        return 'NA'


def clean_ramp(x):
    p=re.sub('[^0-9.,]+',' ', x)
    return p
    
def fun1(x):
    if x=="jacksonville (bit), u.s.a.":
        return x.split(" ")[0]
    else:
        return x

def port_code_substring(x):
    x=re.sub('[^A-Za-z(), ]+',' ', x)
    
    if len(x.split(','))>1:
        x=x.split(',')[0].strip()
        return x.lower()
        
        #now remove white space and comma
    elif '(' in x:
        x=re.sub(r'\([^)]*\)', '', x)
        return x.lower()
            
    elif len(x.split(' '))>1:
        x=x.split(' ')[0].strip()

        return x.lower()
        
    

    elif len(x)>3:
        return x.lower()
    else:
        return "NA"


fileName='2-1_north_america_and_south_america_shuttle_service.pdf'

# DOWNLOAD PDF
download_dir = os.getcwd()
print(download_dir)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True #I
})
# driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)
#for local running on windows uncomment above line if using linux and commen below line of code
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
if os.path.exists(fileName):
    os. remove(fileName)
    
url = 'https://www.klineglobalroro.com/schedules.html'
driver.get(url)
driver.find_element(By.XPATH,f'//a[contains(@href,"{fileName}")]').click()

sleep(10)

# if not os.path.exists(fileName):
# 	wget.download(url,fileName)

driver.quit()


# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

#for local running on windows uncomment above line if using linux and commen below line of code
# driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file

# function to handle setting up headless download
enable_download_headless(driver, download_dir)


sleep(1)

driver.get("https://www.onlineocr.net/")
sleep(4)
completeFile=download_dir+"/"+fileName
driver.find_element_by_id("fileupload").send_keys(completeFile)
sleep(10)
el = driver.find_element_by_id('MainContent_comboOutput')
for option in el.find_elements_by_tag_name('option'):
    if option.text=='Microsoft Excel (xlsx)':
        option.click()

sleep(10)
Submitbutton = driver.find_element_by_xpath('//*[@id="MainContent_btnOCRConvert"]')
driver.execute_script("arguments[0].click();", Submitbutton)

sleep(10)


try:
    button = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="MainContent_lnkBtnDownloadOutput"]')))
    button.click()
except:
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    button = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="MainContent_lnkBtnDownloadOutput"]')))
    button.click()


sleep(3)
os.remove(completeFile)

driver.close();

driver.quit();



df=pd.read_excel("2-1_north_america_and_south_america_shuttle_service.xlsx",engine="openpyxl")

StartIndex=df.index[df.iloc[:,0].str.contains("HIGHWAY")==True].to_list()[0]
EndIndex=df.index[df.iloc[:,0].str.contains("CALL SUBJECT TO INDUCEMENT")==True].to_list()[0]

df=df.iloc[StartIndex:EndIndex,:].reset_index(drop=True)
df=df.dropna(axis='columns',how='all')#remove all nan columns
df=df.dropna(thresh=1)

df=df.replace(np.nan,'NA')
df=df.replace('SKIP','NA')
df=df.replace('-','NA')

df.columns=["col_{}".format(i) for i in range(0,df.shape[1])]

print(df)

vassel_name=[data.split()[0]+' '+data.split()[1] if ' ' in data else data for data in list(df.iloc[0,1:])]

vassel_name.remove('NA')

vassel_name=[vassel.replace("150","").strip() if "150" in vassel else vassel for vassel in vassel_name]

Ramp_capacity=['150', '150', '150', '150', '150', 'NN', '150']

Max_Deck_Height=[data.split()[-3] for data in list(df.iloc[0,1:])]

Max_Deck_Height.remove('')

SOUTHBOUND_VOYAGE_index=df.index[df.iloc[:,0].str.contains("SOUTHBOUND VOYAGE")==True].to_list()[0]

NORTHBOUND_VOYAGE_index=df.index[df.iloc[:,0].str.contains("NORTHBOUND VOYAGE")==True].to_list()[0]


SOUTHBOUND_VOYAGE_df=df.iloc[SOUTHBOUND_VOYAGE_index:NORTHBOUND_VOYAGE_index,:].reset_index(drop=True)

NORTHBOUND_VOYAGE_df=df.iloc[NORTHBOUND_VOYAGE_index:,:].reset_index(drop=True)

SOUTHBOUND_VOYAGE_NO=[str(data).split()[-1] for data in list(SOUTHBOUND_VOYAGE_df.iloc[0,:])][1:]

NORTHBOUND_VOYAGE_NO=[str(data).split()[-1] for data in list(NORTHBOUND_VOYAGE_df.iloc[0,:])][1:]

#SOUTHBOUND_VOYAGE_NO.remove('NA')

#NORTHBOUND_VOYAGE_NO.remove('NA')
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

if len(SOUTHBOUND_VOYAGE_NO)==len(vassel_name) and len(Ramp_capacity)==len(Max_Deck_Height):
    #print("************************  SOUTHBOUND_VOYAGE_df   *************************")
    for index,row in SOUTHBOUND_VOYAGE_df.iterrows():
        if index==0:
            pass
        else:
            port_name=row[0]
            # print(port_name)
            for x in range(1,len(vassel_name)+1):
                if len(str(row[x])) >2:
                    Date=row[x]   
                    data_dict['Carrier'].append("K-LINE")
                    data_dict['Vessel Name'].append(vassel_name[x-1].replace('\n',' ').replace(',',' '))
                    data_dict['Voyage Number'].append(SOUTHBOUND_VOYAGE_NO[x-1])
                    data_dict['Port Name'].append(port_name.lower())
                    data_dict['Date of Arrival (ETA)'].append(datetimeFunction(Date))
                    data_dict['Date of Departure (ETD)'].append("NA")
                    data_dict['Vessel Capacity (in MT)'].append(Ramp_capacity[x-1])
                    data_dict['Vessel Ramp Height (in meters)'].append(Max_Deck_Height[x-1])
                    data_dict['Route Code'].append("NA-SA")
    

if len(SOUTHBOUND_VOYAGE_NO)==len(vassel_name) and len(Ramp_capacity)==len(Max_Deck_Height):
    #print("************************  SOUTHBOUND_VOYAGE_df   *************************")
    for index,row in NORTHBOUND_VOYAGE_df.iterrows():
        if index==0:
            pass
        else:
            port_name=row[0]
            print(port_name)
            for x in range(1,len(vassel_name)+1):
                if len(str(row[x])) >2:
                    Date=row[x]
                    data_dict['Carrier'].append("K-LINE")
                    data_dict['Vessel Name'].append(vassel_name[x-1])
                    data_dict['Voyage Number'].append(NORTHBOUND_VOYAGE_NO[x-1])
                    data_dict['Port Name'].append(port_name.lower())
                    data_dict['Date of Arrival (ETA)'].append(datetimeFunction(Date))
                    data_dict['Date of Departure (ETD)'].append("NA")
                    data_dict['Vessel Capacity (in MT)'].append(Ramp_capacity[x-1])
                    data_dict['Vessel Ramp Height (in meters)'].append(Max_Deck_Height[x-1])
                    data_dict['Route Code'].append("NA-SA")
    

MasterDf=pd.DataFrame(data_dict)
MasterDf['Port Name']=MasterDf['Port Name'].apply(lambda x :fun1(x))

MasterDf['Vessel Ramp Height (in meters)']=MasterDf['Vessel Ramp Height (in meters)'].apply(lambda x:clean_ramp(x))
    
MasterDf['Vessel Capacity (in MT)']=MasterDf['Vessel Capacity (in MT)'].apply(lambda x:clean_ramp(x))

port_df=pd.read_csv("port.csv")

port_list=[]
for index,row in MasterDf.iterrows():
    port_name=port_code_substring(row['Port Name']) 
    if port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)].shape[0]>0:
        portCode=port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)]['CODE'].values
        #print('len=',len(port_name),port_name,portCode[0])
        port_list.append(portCode[0])
    else:
        #print('len=',len(port_name),'NO-----------------')
        port_list.append("NA")


MasterDf['port_code']=np.array(port_list)
MasterDf=MasterDf.replace("NA",'')
MasterDf.to_csv('a3.csv',index=False)












