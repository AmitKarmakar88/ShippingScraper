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



def CurrentDate_upto(x):
	if len(x)>2:
		CurrentDate = days_before = (date.today()-timedelta(days=60)).strftime('%d/%m/%Y')
		date1 = CurrentDate
		date2 = x
		newdate1 = time.strptime(date1, "%d/%m/%Y")
		newdate2 = time.strptime(date2, "%d/%m/%Y")
		if newdate1 > newdate2:
			return True
		else:
			return False
	else:
		return False
 
def removeDuplicate(x):
	print(x)
	if type(x)==np.float:
		return ''
	else:
		x=re.sub('[^A-Za-z]+',' ', x)
		x=x.split()
		return x[0]

def OnlyNumbersRampHeight_RampCapacity(x):
	x=re.sub('[^0-9,. ]+',' ', str(x))
	return x

	
Calendra_dict={'jan':1,'feb':2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

def Date_new(x):
	if len(x)>3:
		x=x.split('-')
		# print(x)
		if len(x)==3:
			# print(str(Calendra_dict[x[1][0:3].strip().lower()]))
			return x[0]+'/'+str(Calendra_dict[x[1][0:3].strip().lower()])+'/'+x[-1]
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




try:
	url = "https://www.hoeghautoliners.com/sailing-schedule#?schedule=vessel"


	#driver = webdriver.Chrome("C:/Users/rohit/Downloads/chromedriver_win32/chromedriver.exe")
	#driver = webdriver.Firefox()
	# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
	driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

	#for local running on windows uncomment above line if using linux and commen below line of code
	# driver = webdriver.Chrome('C:\\Windows\\chromedriver.exe',chrome_options=chrome_options)
	#driver = webdriver.Chrome(header=True)

	driver.get(url)    # Opening the submission url

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



	sleep(3)
	
	el = driver.find_element_by_xpath('//*[@id="main"]/div/article/div/section/div/div[3]/div[3]/div[1]/div[3]/div[1]/div[1]/select')
	for option in el.find_elements_by_tag_name('option')[3:]:
		option.click() # select() in earlier versions of webdriver
		print(option.text)
		html_source = driver.page_source

		df = pd.read_html(html_source)
		if len(df)>7:
			df=df[7]
			vassel_name=[]
			Voyage_No=[]
			
			for i in range(1,df.shape[1]):
				v_name=df.columns[i].split("/")[0]
				V_No=df.columns[i].split("/")[1].strip().replace("ETAETD", "")
				vassel_name.append(v_name)
				Voyage_No.append(V_No)  
				
				
			for index,row in df.iterrows():
				port_name=df.iloc[index,0]
				list_data=list(row)[1:]
				for j in range(0,len(list_data)):
					if len(list_data[j])>2:
						ETA=list_data[j].split("ETD")[0].replace("ETA","")
						ETD=list_data[j].split("ETD")[1]
						DateETA=ETA.split(' ')
						DateETA=DateETA[5]+'-'+DateETA[1]+'-'+DateETA[3]
						DateETD=ETD.split(' ')
						DateETD=DateETD[5]+'-'+DateETD[1]+'-'+DateETD[3]
						data_dict['Carrier'].append("HOG")
						data_dict['Vessel Name'].append(vassel_name[j]) 
						data_dict['Voyage Number'].append(Voyage_No[j])
						data_dict['Port Name'].append(port_name)
						data_dict['Date of Arrival (ETA)'].append(DateETA)
						data_dict['Date of Departure (ETD)'].append(DateETD)
						data_dict['Route Code'].append("NA")
						data_dict['Vessel Capacity (in MT)'].append("NA")
						data_dict['Vessel Ramp Height (in meters)'].append("NA")
		else:
			  pass
		sleep(4)
		#break
		
		
	MasterDf=pd.DataFrame(data_dict)

	# MasterDf['Port Name']=MasterDf['Port Name'].apply(lambda x:removeDuplicate(x))

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
	MasterDf['Date of Arrival (ETA)']=MasterDf['Date of Arrival (ETA)'].apply(lambda x:Date_new(x))
	MasterDf['Date of Departure (ETD)']=MasterDf['Date of Departure (ETD)'].apply(lambda x:Date_new(x))
	MasterDf=MasterDf[['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)','Date of Departure (ETD)']]
	print("total Data HOG=",MasterDf.shape)
	MasterDf.reset_index(drop=True, inplace=True)    

	DelDateCol1=MasterDf['Date of Arrival (ETA)'].apply(lambda x:CurrentDate_upto(x))
	DelDateColIndex1=[x for x in range(0,len(DelDateCol1)) if DelDateCol1[x]]

	DelDateCol2=MasterDf['Date of Departure (ETD)'].apply(lambda x:CurrentDate_upto(x))
	DelDateColIndex2=[y for y in range(0,len(DelDateCol2)) if DelDateCol2[y]]

	DelDateColIndex=list(set(DelDateColIndex1+DelDateColIndex2))

	MasterDf.drop(DelDateColIndex , inplace=True)

	for index,row in MasterDf.iterrows():
		if type(row['Port Name'])==type(np.nan):
			MasterDf['Port Name'][index]=""
			MasterDf['port_code'][index]=""
			
			
		else:
			
			
			if "baltimore" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="baltimore".title()
				MasterDf['port_code'][index]="US BAL"
			
			elif "'aqaba" in row['Port Name'].lower() or "aqaba" in row['Port Name'].lower() :
				 MasterDf['Port Name'][index]="Aqaba".title()
				 MasterDf['port_code'][index]="JO AQJ"
				 
			elif "brunswick" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="brunswick".title()
				MasterDf['port_code'][index]=""
				
			elif "borusan" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="borusan".title()
			
			elif "cartagena" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="cartagena".title()
			
			elif "charleston" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="charleston".title()
			
			elif "freeport" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="freeport".title()
			
			elif "galveston" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="galveston".title()
			
			elif "hamad" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="hamad".title()

			elif "jeddah" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="jeddah".title()
				MasterDf['port_code'][index]="SA JED"
			
			elif "kuwait" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="kuwait".title()
				MasterDf['port_code'][index]="KW KWI"
				
			elif "masan" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="masan".title()
				MasterDf['port_code'][index]="KR MAS"
			
			elif "manzanillo" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="manzanillo".title()
			
			
			elif "newark" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="newark".title()
			

			elif "new york" in row['Port Name'].lower() or "newyork" in row['Port Name'].lower() :
				MasterDf['Port Name'][index]="new york".title()
				MasterDf['port_code'][index]="US NYC"
					
			
			elif "newcastle" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="newcastle".title()
			
			elif "paranagua" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="paranagua".title()
			
			elif "philadelphia" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="philadelphia".title()
			
			elif "puerto caldera" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="puerto caldera".title()
				MasterDf['port_code'][index]="CL PMC"
			
			elif "puerto cortes" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="puerto cortes".title()
				MasterDf['port_code'][index]="HN PCR"
			
			elif "puerto limon" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="puerto limon".title()
				MasterDf['port_code'][index]=""
			
			elif "san lorenzo" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="san lorenzo".title()
				MasterDf['port_code'][index]="HN SLO"
				
			elif "santo domingo" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="santo domingo".title()
				MasterDf['port_code'][index]="DO SDQ"
				
			elif "santos" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="santos".title()
				MasterDf['port_code'][index]="BR SSZ"

			elif "shanghai" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="shanghai".title()
				MasterDf['port_code'][index]="CN SHA"
			

			elif "tacoma" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="tacoma".title()
				MasterDf['port_code'][index]="US ACI"
			

			elif "wilmington" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="wilmington".title()
			
			elif "altamira" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="altamira".title()
				MasterDf['port_code'][index]="MX ATM"
				
			elif "aratu" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="aratu".title()
			
			elif "zarate" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="zarate".title()
			
			elif "altamira" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="altamira".title()
				MasterDf['port_code'][index]="MX ATM"
				
			elif "new westminster" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="new westminster".title()
				MasterDf['port_code'][index]="" 
	  
			elif "abu dhabi" in row['Port Name'].lower() or "abu" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="abu dhabi".title()
				MasterDf['port_code'][index]=""   

			elif "ad dammam" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="ad dammam".title()
				MasterDf['port_code'][index]=""     
				
			elif "bahrain" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="bahrain".title()
				MasterDf['port_code'][index]="BH KBS"

				
			elif "corpus" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="corpus".title()
				MasterDf['port_code'][index]="US CRP"

			elif "eca ent.point usec jxv/buw/svn" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="eca ent.point usec jxv/buw/svn".title()
				MasterDf['port_code'][index]=""
				
			elif "el iskandariya (alexandria)" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="el iskandariya (alexandria)".title()
				MasterDf['port_code'][index]=""
				
			elif "fort de france" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="fort de france".title()
				MasterDf['port_code'][index]="MQ FDF"
				
			elif "hai phong" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="hai phong".title()
				MasterDf['port_code'][index]=""
				
			elif "ho chi minh" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="ho chi minh".title()
				MasterDf['port_code'][index]="VN SGN"
				
			elif "honolulu" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="honolulu".title()
				MasterDf['port_code'][index]="US HNL"
				
			elif "houston" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="houston".title()
				MasterDf['port_code'][index]="US HOU"            
				
			elif "huangpu" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="huangpu".title()
				MasterDf['port_code'][index]=""              
				
			elif "jakarta" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="jakarta".title()
				MasterDf['port_code'][index]="ID TPP"   

			elif "jebel" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="jebel".title()
				MasterDf['port_code'][index]="AE JEA"   

			elif "keelung" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="keelung".title()
				MasterDf['port_code'][index]="TW KEL"   

			elif "kingston" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="kingston".title()
				MasterDf['port_code'][index]="JM KIN"   

			elif "koper" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="koper".title()
				MasterDf['port_code'][index]="SI KOP"   

			elif "lehavre" in row['Port Name'].lower().strip() or "le havre" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="le havre".title()
				MasterDf['port_code'][index]="FR LEH"   
				
			elif "lian yun gang" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="lian yun gang".title()
				MasterDf['port_code'][index]=""   

			elif "livorno" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="livorno".title()
				MasterDf['port_code'][index]="IT LIV"   

			elif "long beach" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="long beach".title()
				MasterDf['port_code'][index]="US LGB"   

			elif "mobile" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="mobile".title()
				MasterDf['port_code'][index]="US MOB"   
				
			elif "mumbai" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="mumbai".title()
				MasterDf['port_code'][index]="IN BOM"   

																
			elif "nagoya" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="nagoya".title()
				MasterDf['port_code'][index]="JP NGO"   

			elif "port elizabeth" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port elizabeth".title()
				MasterDf['port_code'][index]="ZA PLZ"   

			elif "port everglades" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port everglades".title()
				MasterDf['port_code'][index]="US PEF"   

				
			elif "port hueneme" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port hueneme".title()
				MasterDf['port_code'][index]=""   

			elif "port kelang" in row['Port Name'].lower() or "port klang" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port kelang".title()
				MasterDf['port_code'][index]="MY PKL"   

			elif "port kembla" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port kembla".title()
				MasterDf['port_code'][index]=""   

			elif "port of spain" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port of spain".title()
				MasterDf['port_code'][index]=""   

			elif "port louis" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port louis".title()
				MasterDf['port_code'][index]="MU PLU"   

			elif "port moresby" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port moresby".title()
				MasterDf['port_code'][index]="PG POM"   

			elif "port reunion" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port reunion".title()
				MasterDf['port_code'][index]="RE PDG"   

			elif "port sudan" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port sudan".title()
				MasterDf['port_code'][index]="SD PZU"   

			elif "port-au-prince" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="port-au-prince".title()
				MasterDf['port_code'][index]=""   

			elif "pt elizabeth" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="pt elizabeth".title()
				MasterDf['port_code'][index]="ZA PLZ"   

			elif "puerto" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="puerto".title()
				MasterDf['port_code'][index]="HN PCR"   

			elif "qingdao" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="qingdao".title()
				MasterDf['port_code'][index]="CN TAO"   

			elif ("rio de janeiro" in row['Port Name'].lower()) or ("rio" == row['Port Name'].lower()):
				MasterDf['Port Name'][index]="rio de janeiro".title()
				MasterDf['port_code'][index]="BR RIO"   

			elif "rio grande" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="rio grande".title()
				MasterDf['port_code'][index]="BR RIG"   

			elif "rio haina" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="rio haina".title()
				MasterDf['port_code'][index]="DO HAI"   

			elif ("san antonio" in row['Port Name'].lower()) or ("san" == row['Port Name'].lower()):
				MasterDf['Port Name'][index]="san antonio".title()
				MasterDf['port_code'][index]="CL SAI"   
				
			elif "san diego" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="san diego".title()
				MasterDf['port_code'][index]=""   
				
			elif "san juan" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="san juan".title()
				MasterDf['port_code'][index]="NI SJS"  
				
			elif ("santa" == row['Port Name'].lower()) or ("santa marta" == row['Port Name'].lower()):
				MasterDf['Port Name'][index]="santa marta".title()
				MasterDf['port_code'][index]="AR SFN"   
				
			elif "savannah" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="savannah".title()
				MasterDf['port_code'][index]="US SAV"   
				
			elif "st john's" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="st john's (ant)".title()
				MasterDf['port_code'][index]=""   

			elif "st. petersburg" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="st. petersburg".title()
				MasterDf['port_code'][index]="RU LED"   

			elif "suape" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="suape".title()
				MasterDf['port_code'][index]=""   

			elif "tamatave" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="tamatave".title()
				MasterDf['port_code'][index]="MG TOA"   

			elif "Tianjin" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="Tianjin".title()
				MasterDf['port_code'][index]="CN TSN"   

			elif "toyohashi" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="toyohashi".title()
				MasterDf['port_code'][index]=""   

			elif "veracruz" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="veracruz".title()
				MasterDf['port_code'][index]="MX VER"   

			elif "xingang" in row['Port Name'].lower():
				MasterDf['Port Name'][index]="xingang".title()
				MasterDf['port_code'][index]=""   
			#add fri 17-jul
			elif ("goteborg" in row['Port Name'].lower()) or ("gothenburg" in row['Port Name'].lower().strip()):
				MasterDf['Port Name'][index]="Gothenburg".title()
				MasterDf['port_code'][index]="SE GOT"

			elif ("antwerp" in row['Port Name'].lower().strip()) or ("antwerpen" in row['Port Name'].lower().strip()):
				MasterDf['Port Name'][index]="Antwerpen".title()
				MasterDf['port_code'][index]="BE ANR"
			#end																																																																									
			else:
				#print(MasterDf['Port Name'][index])
				MasterDf['Port Name'][index]=MasterDf['Port Name'][index].title()


	index1=list(MasterDf.index[MasterDf['Port Name']=="Port"]) 
		
	index2=list(MasterDf.index[MasterDf['Port Name']=="New"]) 
	index3=list(MasterDf.loc[pd.isna(MasterDf["Port Name"]), :].index)
	totalDel=index1+index2+index3
	totalDel=list(set(totalDel))
	MasterDf.drop(totalDel , inplace=True)

	#----------------------------------------new code for port code-----------------------------------------------
	 
	MasterDf=MasterDf.replace(np.nan,'')

	port_MasterDf1=pd.read_csv("NewPortCode.csv")

	port_MasterDf1['Port Name']=port_MasterDf1['Port Name'].apply(lambda x :x.strip())


	for index,row in MasterDf.iterrows():
		if len(row['port_code'])<4 and len(row['port_code'])!=2:
			if port_MasterDf1[port_MasterDf1['Port Name']==row['Port Name'].strip()].shape[0]>0:
				portCode=port_MasterDf1[port_MasterDf1['Port Name']==row['Port Name'].strip()]['Port_code'].values
				MasterDf['port_code'][index]=portCode[0]


	MasterDf=MasterDf.drop_duplicates(subset=['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)'])



	# index1=list(MasterDf.index[MasterDf['Port Name']==""]) 
		
	index2=list(MasterDf.index[MasterDf['port_code']==""]) 

	#index3=list(MasterDf.index[MasterDf['Date of Arrival (ETA)']==""]) 


	totalDel=index2

	totalDel=list(set(totalDel))

	MasterDf.drop(totalDel , inplace=True)

	MasterDf.reset_index(drop=True, inplace=True)    

	#----------------------------------------------------------- End  ---------------------------------------------------
	MasterDf['Vessel Capacity (in MT)']=MasterDf['Vessel Capacity (in MT)'].apply(lambda x :OnlyNumbersRampHeight_RampCapacity(x))

	MasterDf['Vessel Ramp Height (in meters)']=MasterDf['Vessel Ramp Height (in meters)'].apply(lambda x :OnlyNumbersRampHeight_RampCapacity(x))


	MasterDf.to_csv("hog.csv", index=False)

	print("Complete Scrap hog")
	print("HOG completed--- %s seconds ---" % (time.time() - start_time))
	sleep(2)#after 10 second remove file
except Exception as e:
	print(e)
	pass   

	
driver.close();

driver.quit();


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	