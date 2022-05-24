
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

def clean_Date(x):
	p=re.sub('[^0-9A-Za-z-]+',' ', x).strip()
	return p+'-2020'


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

Calendra_dict={1:'jan',2:'feb',3:"mar",4:"apr",5:"may",6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"}

def clean_Date(x):
    x=re.sub('[^0-9A-Za-z-]+',' ', x).strip()    
    try:
        if x in "NA":
            return "NA"
        else:
            x=x.split('-')
            Date=x[0]+'-'+x[1]+'-2020'
            return Date
    except:
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

	# download_dir = os.getcwd()
	# print(download_dir)
		
	# url = 'http://www.klineglobalroro.com/schedules/1-1_europe_to_north_america_and_mexico_gulf_schedule.pdf'

	# fileName='1-1_europe-trans_atlantic_schedule.pdf'

	# if not os.path.exists(fileName):
	# 	wget.download(url,fileName)
		

	# print(url)
	# # function to take care of downloading file
	# def enable_download_headless(browser,download_dir):
	# 	browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
	# 	params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	# 	browser.execute("send_command", params)

	# # instantiate a chrome options object so you can set the size and headless preference
	# # some of these chrome options might be uncessary but I just used a boilerplate
	# # change the <path_to_download_default_directory> to whatever your default download folder is located
	# chrome_options = Options()
	# # chrome_options.add_argument("--headless")
	# chrome_options.add_argument('--headless')
	# chrome_options.add_argument('--disable-dev-shm-usage')
	# chrome_options.add_argument("--window-size=1920x1080")
	# chrome_options.add_argument("--disable-notifications")
	# chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument('--verbose')
	# chrome_options.add_experimental_option("prefs", {
	# 		"download.default_directory": download_dir,
	# 		"download.prompt_for_download": False,
	# 		"download.directory_upgrade": True,
	# 		"safebrowsing_for_trusted_sources_enabled": False,
	# 		"safebrowsing.enabled": False
	# })
	# chrome_options.add_argument('--disable-gpu')
	# chrome_options.add_argument('--disable-software-rasterizer')

	# # initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
	# driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

	# # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file

	# # function to handle setting up headless download
	# enable_download_headless(driver, download_dir)


	# sleep(1)

	# driver.get("https://www.onlineocr.net/")
	# sleep(4)
	# completeFile=download_dir+"/"+fileName
	# driver.find_element_by_id("fileupload").send_keys(completeFile)
	# sleep(2)
	# el = driver.find_element_by_id('MainContent_comboOutput')
	# for option in el.find_elements_by_tag_name('option'):
	# 	if option.text=='Microsoft Excel (xlsx)':
	# 		option.click()

	# sleep(5)
	# Submitbutton = driver.find_element_by_xpath('//*[@id="MainContent_btnOCRConvert"]')
	# driver.execute_script("arguments[0].click();", Submitbutton)

	# sleep(6)

	# DownloadFile=driver.find_element_by_xpath('//*[@id="MainContent_lnkBtnDownloadOutput"]')

	# DownloadFile.click()

	# sleep(3)
	# os.remove(completeFile)

	# driver.close();

	# driver.quit();



	# df=pd.read_excel("k2.xlsx")

	# df=df.replace(np.nan,'NA')
	# df=df.replace('SKIP','NA')
	# df=df.replace('-','NA')
	  

	# # Split_list=df.index[df.iloc[:,0].str.contains("VESSEL NAME")==True].to_list()
	  
	        
	# del df['Column8']  
	            
	# # df=df.iloc[1:,:]
	# #df.reset_index(drop=True, inplace=True)

	# #indexNames=df[df[df.columns[0]]=='NA'].index.values

	# #df.drop(indexNames , inplace=True)
	# #df.reset_index(drop=True, inplace=True)


	# #df=df.iloc[3:-1,:]
	# #df.reset_index(drop=True, inplace=True)

	# sampleDf=df.copy()

	# Vessel_Name=sampleDf.iloc[0,1:].to_list() 
	# Vessel_Name=[i.split('_x000D_\n')[0]+" "+i.split('\n')[1] if len(i.split('\n'))==2 else i for i in Vessel_Name]  
	# # Vessel_Name=[i.split('\n')[0]+" "+i.split('\n')[1] if len(i.split('\n'))==2 else i for i in Vessel_Name]  
	# Voyage_No=sampleDf.iloc[1,1:].to_list()
	# Voyage_No=["NN" if i=='NA' else i for i in Voyage_No]
	# Ramp_Capacity=sampleDf.iloc[2,1:].to_list()
	# rampheight=sampleDf.iloc[3,1:].to_list()
	  
	# sampleDf=sampleDf.iloc[4:,:]
	# sampleDf.reset_index(drop=True, inplace=True)

	df=pd.read_excel("k2.xlsx")


	del df['Column8']  
	del df['Service']  


	df_head=df.iloc[0:4]

	df_head=df_head.replace(np.nan,'NA')
	df_head=df_head.replace('SKIP','NA')
	df_head=df_head.replace('-','NA')
	del df_head['Column1']  

	df=df.dropna(subset=['Column1'])
	df=df.replace(np.nan,'NA')
	df=df.replace('SKIP','NA')
	df=df.replace('-','NA')
	  
	sampleDf=df.copy()

	Vessel_Name=df_head.iloc[0,1:].to_list() 
	Vessel_Name=[i.split('_x000D_\n')[0]+" "+i.split('\n')[1] if len(i.split('\n'))==2 else i for i in Vessel_Name]  
	# Vessel_Name=[i.split('\n')[0]+" "+i.split('\n')[1] if len(i.split('\n'))==2 else i for i in Vessel_Name]  
	Voyage_No=df_head.iloc[1,1:].to_list()
	Voyage_No=["NN" if i=='NA' else i for i in Voyage_No]
	Ramp_Capacity=df_head.iloc[2,1:].to_list()
	rampheight=df_head.iloc[3,1:].to_list()
	  
	sampleDf.reset_index(drop=True, inplace=True)

	# Split_list=df.index[df.iloc[:,0].str.contains("VESSEL NAME")==True].to_list()
	  
	  
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
	 
			
	for index,row in sampleDf.iterrows():
		port_name=row[0]
		print(port_name)
		if port_name!="NA":
			for i in range(1,len(Voyage_No)+1):
				Date=row[i]
				data_dict['Carrier'].append("K-LINE")
				data_dict['Vessel Name'].append(Vessel_Name[i-1])
				data_dict['Voyage Number'].append(Voyage_No[i-1])
				data_dict['Port Name'].append(port_name.lower())
				data_dict['Date of Arrival (ETA)'].append(clean_Date(Date))
				data_dict['Date of Departure (ETD)'].append("NA")
				data_dict['Vessel Capacity (in MT)'].append(Ramp_Capacity[i-1])
				data_dict['Vessel Ramp Height (in meters)'].append(rampheight[i-1])
				data_dict['Route Code'].append("EU-NA")
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
	MasterDf.to_csv("a2.csv",index=False)    
	# sleep(2)
	# os.remove('1-1_europe-trans_atlantic_schedule.xlsx')

except Exception as e:
	print(e)
	pass