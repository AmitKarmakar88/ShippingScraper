
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

#==============================================================

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
	fileName='1-2_north_america_and_mexico_gulf_to_europe_schedule.pdf'

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

	if os.path.exists(fileName):
		os. remove(fileName)

	driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
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
	sleep(2)
	el = driver.find_element_by_id('MainContent_comboOutput')
	for option in el.find_elements_by_tag_name('option'):
		if option.text=='Microsoft Excel (xlsx)':
			option.click()

	sleep(7)
	Submitbutton = driver.find_element_by_xpath('//*[@id="MainContent_btnOCRConvert"]')
	driver.execute_script("arguments[0].click();", Submitbutton)

	sleep(7)
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


	#start of main code after download xls
	df=pd.read_excel("1-2_north_america_and_mexico_gulf_to_europe_schedule.xlsx",engine="openpyxl")
	# df=pd.read_excel("ka2.xlsx")

	df=df.replace(np.nan,'NA')
	df=df.replace('SKIP','NA')
	df=df.replace('-','NA')
	  

	Split_list=df.index[df.iloc[:,0].str.contains("VESSEL NAME")==True].to_list()
	  
	        
	del df['Unnamed: 1']  
	            

	indexNames=df[df[df.columns[0]]=='NA'].index.values

	df.drop(indexNames , inplace=True)

	sampleDf=df.copy()


	Vessel_Name=sampleDf.iloc[0,1:].to_list() 
	Vessel_Name=[i.split('\n')[0]+" "+i.split('\n')[1] if len(i.split('\n'))==2 else i for i in Vessel_Name]  
	Voyage_No=sampleDf.iloc[1,1:].to_list()
	Voyage_No=["NN" if i=='NA' else i for i in Voyage_No]
	Ramp_Capacity=sampleDf.iloc[2,1:].to_list()
	rampheight=sampleDf.iloc[3,1:].to_list()
	  

	sampleDf=sampleDf.iloc[4:,:]
	sampleDf.reset_index(drop=True, inplace=True)


	  
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
				data_dict['Vessel Name'].append(Vessel_Name[i-1].replace(',',' ').replace('\n',' '))
				data_dict['Voyage Number'].append(Voyage_No[i-1])
				data_dict['Port Name'].append(port_name.lower())
				data_dict['Date of Arrival (ETA)'].append(datetimeFunction(Date))
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
	sleep(2)
	os.remove('1-2_north_america_and_mexico_gulf_to_europe_schedule.xlsx')
	# driver.quit()

except Exception as e:
	print(e)
	pass