
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import os
# from time import sleep
# import wget
# import shutil
# import wget
# # import tabula

# import os
# import pandas as pd
# import numpy as np
# import urllib.request
# from time import sleep
# import re
# from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
# import requests
# from time import sleep

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait as wait

# try:

# 	def month_number_to_string(string):
# 		m = {1:['jan',2021],2:['feb',2021],3:['mar',2021],4:['apr',2021],5:['may',2021], 6:['jun',2021],7:['jul',2021],8:['aug',2021],9:['sep',2021],10:['oct',2021],11:['nov',2020],12:['dec',2020]}
# 		return m[string]

# 	def split_date_no(x): 
# 		x=x.split("/")
# 		if len(x)>1:
# 			return x[0]+"-"+month_number_to_string(int(x[1]))[0]+'-'+str(month_number_to_string(int(x[1]))[1])
# 		else:
# 			return "NA"


# 	def clean_ramp(x):
# 		p=re.sub('[^0-9.,]+',' ', x)
# 		return p


# 	def port_code_substring(x):
# 		x=re.sub('[^A-Za-z, ]+',' ', x)
		
# 		if len(x.split(','))>1:
# 			x=x.split(',')[0].strip()
# 			return x.lower()
			
# 			#now remove white space and comma
# 		elif '(' in x:
# 			x=re.sub(r'\([^)]*\)', '', x)
# 			return x.lower()

# 		elif len(x.split(' '))>1:
# 			x=x.split(' ')[0].strip()

# 			return x.lower()
			
# 		elif len(x)>3:
# 			return x.lower()

		
# 		else:
# 			return "NA"



# 	fileName='3-1_north_america_to_asia_australia_express(nax).pdf'
# 	# DOWNLOAD PDF
# 	download_dir = os.getcwd()
# 	print(download_dir)


# 	# chrome_options.add_argument("--headless")
# 	# chrome_options.add_argument('--headless')
# 	# chrome_options.add_argument('--disable-dev-shm-usage')
# 	# chrome_options.add_argument("--window-size=1920x1080")
# 	# chrome_options.add_argument("--disable-notifications")
# 	# chrome_options.add_argument('--no-sandbox')
# 	# chrome_options.add_argument('--verbose')
# 	chrome_options = Options()
# 	chrome_options.add_experimental_option("prefs", {
# 		"download.default_directory": download_dir,
# 		"download.prompt_for_download": False,
# 		"download.directory_upgrade": True,
# 		"safebrowsing_for_trusted_sources_enabled": False,
# 		"safebrowsing.enabled": False,
# 		"plugins.always_open_pdf_externally": True #I
# 	})
# 	driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)
# 	#for local running on windows uncomment above line if using linux and commen below line of code

# 	if os.path.exists(fileName):
# 		os. remove(fileName)
		
# 	url = 'https://www.klineglobalroro.com/schedules.html'
# 	driver.get(url)
# 	driver.find_element(By.XPATH,f'//a[contains(@href,"{fileName}")]').click()

# 	sleep(10)

# 	# if not os.path.exists(fileName):
# 	# 	wget.download(url,fileName)

# 	driver.quit()

# 	# function to take care of downloading file
# 	def enable_download_headless(browser,download_dir):
# 		browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
# 		params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
# 		browser.execute("send_command", params)

# 	# instantiate a chrome options object so you can set the size and headless preference
# 	# some of these chrome options might be uncessary but I just used a boilerplate
# 	# change the <path_to_download_default_directory> to whatever your default download folder is located
# 	chrome_options = Options()
# 	# chrome_options.add_argument("--headless")
# 	chrome_options.add_argument('--headless')
# 	chrome_options.add_argument('--disable-dev-shm-usage')
# 	chrome_options.add_argument("--window-size=1920x1080")
# 	chrome_options.add_argument("--disable-notifications")
# 	chrome_options.add_argument('--no-sandbox')
# 	chrome_options.add_argument('--verbose')
# 	chrome_options.add_experimental_option("prefs", {
# 			"download.default_directory": download_dir,
# 			"download.prompt_for_download": False,
# 			"download.directory_upgrade": True,
# 			"safebrowsing_for_trusted_sources_enabled": False,
# 			"safebrowsing.enabled": False
# 	})
# 	chrome_options.add_argument('--disable-gpu')
# 	chrome_options.add_argument('--disable-software-rasterizer')

# 	# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
# 	# driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

# 	#for local running on windows uncomment above line if using linux and commen below line of code
# 	driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)

# 	# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file

# 	# function to handle setting up headless download
# 	enable_download_headless(driver, download_dir)


# 	sleep(1)

# 	driver.get("https://www.onlineocr.net/")
# 	sleep(4)
# 	completeFile=download_dir+"/"+fileName
# 	driver.find_element_by_id("fileupload").send_keys(completeFile)
# 	sleep(10)
# 	el = driver.find_element_by_id('MainContent_comboOutput')
# 	for option in el.find_elements_by_tag_name('option'):
# 		if option.text=='Microsoft Excel (xlsx)':
# 			option.click()

# 	sleep(10)
# 	Submitbutton = driver.find_element_by_xpath('//*[@id="MainContent_btnOCRConvert"]')
# 	driver.execute_script("arguments[0].click();", Submitbutton)

# 	sleep(10)

# 	button = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="MainContent_lnkBtnDownloadOutput"]')))
# 	button.click()
# 	sleep(3)
# 	os.remove(completeFile)
	
# 	driver.close();

# 	driver.quit();



# 	df=pd.read_excel("3-1_north_america_to_asia_australia_express(nax).xlsx")

# 	df=df.dropna(axis='columns',how='all')#remove all nan columns
# 	df=df.dropna(thresh=2)

# 	df=df.replace(np.nan,'NA')
# 	df=df.replace('SKIP','NA')
# 	df=df.replace('-','NA')
	  
# 	df=df.iloc[:,1:]

# 	df.reset_index(drop=True, inplace=True)

# 	columns=df.iloc[0,:]

# 	Vessel_Name=df.iloc[0,1:]

# 	df.columns=columns#new dataframe that contains tables only have Vassel_name heder

# 	VOYAGE_NUMBER=df.iloc[1,:].values[1:]

# 	RAMP_CAPACITY=df.iloc[2,:].values[1:]

# 	DECK_HEIGHT=df.iloc[4,:].values[1:]


# 	data_dict={}
# 	data_dict['Vessel Name']=[]
# 	data_dict['Voyage Number']=[]
# 	data_dict['Port Name']=[]
# 	data_dict['Carrier']=[]
# 	data_dict['Date of Arrival (ETA)']=[]
# 	data_dict['Date of Departure (ETD)']=[]
# 	data_dict['Route Code']=[]
# 	data_dict['Vessel Capacity (in MT)']=[]
# 	data_dict['Vessel Ramp Height (in meters)']=[]



# 	if len(VOYAGE_NUMBER) == len(Vessel_Name):
# 		for index,row in df.iterrows():
# 			port_name=row[0]
# 			if len(port_name)>3 and index>4:  
# 				for i in range(1,len(DECK_HEIGHT)+1):
# 					print(row[i])
# 					if len(str(row[i]))>2: 
						
# 						try:
# 							if "*" in row[i]:
# 								print(row[i])
# 								row_date=re.sub('[^0-9a-zA-Z-,]+',' ', row[i])  
# 								row_date=row_date.split("-")
# 								ETA=row_date[0]+'-'+row_date[1].lower().strip()+"-2020"
# 						except Exception as e:
# 								ETA=row[i].strftime("%d/%m/2020")
# 								ETA=split_date_no(ETA)
								
# 						data_dict['Carrier'].append("K-LINE")
# 						data_dict['Vessel Name'].append(Vessel_Name[i-1])
# 						data_dict['Voyage Number'].append(VOYAGE_NUMBER[i-1])
# 						data_dict['Port Name'].append(port_name.lower())
# 						data_dict['Date of Arrival (ETA)'].append(ETA)
# 						data_dict['Date of Departure (ETD)'].append("NA")
# 						data_dict['Vessel Capacity (in MT)'].append(RAMP_CAPACITY[i-1])
# 						data_dict['Vessel Ramp Height (in meters)'].append(DECK_HEIGHT[i-1])
# 						data_dict['Route Code'].append("NA-AS")
						
						




# 	MasterDf=pd.DataFrame(data_dict)

# 	# MasterDf['Date of Arrival (ETA)']=MasterDf['Date of Arrival (ETA)'].apply(lambda x:clean_Date(x))
# 	MasterDf['Vessel Ramp Height (in meters)']=MasterDf['Vessel Ramp Height (in meters)'].apply(lambda x:clean_ramp(x))
		
# 	MasterDf['Vessel Capacity (in MT)']=MasterDf['Vessel Capacity (in MT)'].apply(lambda x:clean_ramp(x))


# 	indexNames = MasterDf[MasterDf['Date of Arrival (ETA)'].str.contains("NA")].index       
		
# 	MasterDf.drop(indexNames , inplace=True)


			
# 	port_df=pd.read_csv("port.csv")

# 	port_list=[]
# 	for index,row in MasterDf.iterrows():
# 		port_name=port_code_substring(row['Port Name']) 
# 		##print(port_name)
# 		if port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)].shape[0]>0:
# 			portCode=port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)]['CODE'].values
# 			#print('len=',len(port_name),port_name,portCode[0])
# 			port_list.append(portCode[0])
# 		else:
# 			#print('len=',len(port_name),'NO-----------------')
# 			port_list.append("NA")


# 	MasterDf['port_code']=np.array(port_list)
# 	MasterDf=MasterDf.replace("NA",'')

# 	MasterDf.to_csv('a5.csv',index=False)
# 	os.remove("3-1_north_america_to_asia_australia_express(nax).xlsx")
# except Exception as e:
# 	print(e)
# 	pass


















