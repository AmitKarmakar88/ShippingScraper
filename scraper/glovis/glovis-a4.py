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
#==================================================
from urllib.request import Request, urlopen

#===============================================

def clean_Date(x):
    p=re.sub('[^0-9-.]+',' ', x).strip()
    p=p.split(" ")
    date=p[0]
    
    if "-" in date:
        date=date.split("-")
        date=date[1]+'/'+date[-1]+'/'+date[0]
        return date
    elif "." in date:
        date=date.split(".")
        date=date[0]+'/'+date[1]+'/'+date[-1]
        return date
    else:
        return "NA"


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

try:
    
    download_dir = os.getcwd()
    print(download_dir)
        
    #=======================================================================================
    site= "https://www.stenaglovis.com/customer-centre/schedules/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    contentTable  = soup.find('div', { "class" : "content-wrapper"})
    link = [a['href'] for a in contentTable.find_all('a', href=True)][2:][3]
    print("links=",link)
    #========================================================================================= 
        
    url=link   

    fileName='a4.pdf'
    
    if not os.path.exists(fileName):
        wget.download(url,fileName)
        
    
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
    
    DownloadFile=driver.find_element_by_xpath('//*[@id="MainContent_lnkBtnDownloadOutput"]')
    
    DownloadFile.click()
    
    sleep(3)
    os.remove(completeFile)
    
    driver.close();

    driver.quit();

    
    
    df=pd.read_excel("a4.xlsx",engine="openpyxl")
    
    Split_list=df.index[df.iloc[:,0].str.contains("Vessel Name")==True].to_list()
    
    df_list=[]
    
    
    for i in range(0,len(Split_list)):
        if i==len(Split_list)-1:
            df_new=df.iloc[Split_list[i]:-3,:]
            df_new=df_new.dropna(axis='columns',how='all')#remove all nan columns
            df_new=df_new.dropna(thresh=2)
            df_new=df_new.replace(np.nan,'NA')
            df_new=df_new.replace('SKIP','NA')
            df_new=df_new.replace('-','NA')
            
            df_list.append(df_new)        
            
        elif i<len(Split_list)-1:
            df_new=df.iloc[Split_list[i]:(Split_list[i+1]-3),:]
            df_new=df_new.dropna(axis='columns',how='all')
            df_new=df_new.dropna(thresh=2)
            df_new=df_new.replace(np.nan,'NA')
            df_new=df_new.replace('SKIP','NA')
            df_new=df_new.replace('-','NA')
            df_list.append(df_new)  
    
    
    
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
    
    
    
    for dfs in df_list:
    
        sampleDf=dfs
        
        sampleDf.columns=sampleDf.iloc[0,:]
              
        Vessel_Name=sampleDf.iloc[0,1:].to_list()   
        Voyage_No=sampleDf.iloc[1,1:].to_list()
        Ramp_Capacity=sampleDf.iloc[2,1:].to_list()
        rampheight=sampleDf.iloc[3,1:].to_list()
          
        
        sampleDf=sampleDf.iloc[5:,:]
        
        
        for index,row in sampleDf.iterrows():
            port_name=row[0]
            if port_name!="NA":
                print(port_name)
                for i in range(1,len(Voyage_No)+1):
        
                    data_dict['Carrier'].append("Hyundai Glovis")
                    data_dict['Vessel Name'].append(Vessel_Name[i-1])
                    data_dict['Voyage Number'].append(Voyage_No[i-1])
                    data_dict['Port Name'].append(port_name.lower())
        
                    data_dict['Date of Arrival (ETA)'].append(clean_Date(str(row[i])))
                    data_dict['Date of Departure (ETD)'].append("NA")
        
                    data_dict['Vessel Capacity (in MT)'].append(Ramp_Capacity[i-1])
                    data_dict['Vessel Ramp Height (in meters)'].append(rampheight[i-1])
                    data_dict['Route Code'].append("NA")
                #print("_____________________________________________________________________")
           
          
    MasterDf=pd.DataFrame(data_dict)      
        
      
    indexNames = MasterDf[(MasterDf['Date of Arrival (ETA)'] =="NA")].index
        # Delete these row indexes from dataFrame
    MasterDf.drop(indexNames , inplace=True)
    
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
    MasterDf=MasterDf[['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)']]
    
    MasterDf.to_csv("a4.csv",index=False)  
    os.remove('a4.xlsx')
except Exception as e:
	print(e)
	pass
















  


