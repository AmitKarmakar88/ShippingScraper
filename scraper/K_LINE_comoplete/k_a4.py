#http://www.klineglobalroro.com/schedules/2-2_mercosul_service.pdf
import wget
import tabula
import os
import pandas as pd
import numpy as np
from time import sleep
import re
from tabula import read_pdf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
"""
#http://www.klineglobalroro.com/schedules/2-2_mercosul_service.pdf
import wget
import tabula
import os
import pandas as pd
import numpy as np
from time import sleep
import re

def clean_Date(x):
    p=re.sub('[^0-9-]+',' ', x).strip()
    if len(p)>1:
        if p in x:
            return x+'-2020'
        else:
           return "NA"
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



fileName='2-2_mercosul_service.xlsx'

df=pd.read_excel(fileName)

df=df.replace(np.nan,'-')
df=df.iloc[4:]
df.reset_index(drop=True, inplace=True)

df.columns=['col_{}'.format(i) for i in range(0,df.shape[1])]
df=df[['col_0','col_1','col_3', 'col_5','col_7','col_9','col_11','col_13']]

vassel_name=[i.split('\n')[0]+' '+i.split('\n')[1] for i in list(df.iloc[0,1:])]

Voyage_no=[i.split('\n')[2] for i in list(df.iloc[0,1:])]


"""




try:

	def clean_Date(x):
		p=re.sub('[^0-9-]+',' ', x).strip()
		if len(p)>1:
			if p in x:
				return x+'-2020'
			else:
			   return "NA"
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
	
	fileName='2-2_mercosul_service.pdf'
	print('Beginning mercosul_service file download.....')
	
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
	driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
	# driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)
	#for local running on windows uncomment above line if using linux and commen below line of code

	if os.path.exists(fileName):
		os. remove(fileName)
		
	url = 'https://www.klineglobalroro.com/schedules.html'
	driver.get(url)
	driver.find_element(By.XPATH,f'//a[contains(@href,"{fileName}")]').click()

	sleep(10)

	# if not os.path.exists(fileName):
	# 	wget.download(url,fileName)

	driver.quit()

				
	df_dataset =read_pdf(fileName,multiple_tables = True,encoding='utf-8',pages='all')[0]

	df=df_dataset.copy()
	df.columns = df.iloc[0]
	df = df[1:]
	df=df.replace(np.nan,'-')
	x=df.columns[1:]
	
	print(x)

	vassel_name=[x.split("\r")[0]+","+x.split("\r")[1] for x in df.columns[1:]]
	
	Voyage_Number=[x.split("\r")[2] for x in df.columns[1:]]
	
	
	print('here')
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
	
	
	if len(vassel_name) ==len(Voyage_Number):
		for index,row in df.iterrows():
			port_name=row[0]
			print(port_name)
			for i in range(1,len(vassel_name)+1):
				if len(row[i]) > 2: 
					##print(len(row[i]),"->",row[i].split("/"))
					date_list=row[i].split("/")
					ETA=date_list[0]+"-"+date_list[1][0:3]
					ETD=date_list[1][3:]+"-"+date_list[-1]
					data_dict['Carrier'].append("K-LINE")
					data_dict['Vessel Name'].append(vassel_name[i-1].replace('\n',' ').replace(',',' '))
					data_dict['Voyage Number'].append(Voyage_Number[i-1])
					data_dict['Port Name'].append(port_name.lower())
					data_dict['Date of Arrival (ETA)'].append(ETA)
					data_dict['Date of Departure (ETD)'].append(ETD)
					data_dict['Vessel Capacity (in MT)'].append("NA")
					data_dict['Vessel Ramp Height (in meters)'].append("NA")
					data_dict['Route Code'].append("NA")
	
			#print("------------------------------------")
			
			
	MasterDf=pd.DataFrame(data_dict)
			
	indexNames = MasterDf[MasterDf['Date of Arrival (ETA)'].str.contains("-ago")].index       
		
	MasterDf.drop(indexNames , inplace=True)
	
	MasterDf['Date of Arrival (ETA)']=MasterDf['Date of Arrival (ETA)'].apply(lambda x :clean_Date(x))
	MasterDf['Date of Departure (ETD)']=MasterDf['Date of Departure (ETD)'].apply(lambda x :clean_Date(x))
	
	
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
	
	MasterDf.to_csv('a4.csv',index=False)
	sleep(2)
	os.remove(fileName)

except Exception as e:
	print(e)
	pass




















