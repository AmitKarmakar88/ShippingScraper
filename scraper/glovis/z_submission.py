import glob, os, os.path
import pandas as pd
from time import sleep
import shutil
from datetime import date, timedelta
import numpy as np
from datetime import datetime, timedelta,date
import time
import re

def OnlyNumbersRampHeight_RampCapacity(x):
	x=re.sub('[^0-9,. ]+',' ', str(x))
	return x

try:

	Calendra_dict={'jan':1,'feb':2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

	def Date_new(x):
		try:
			if len(x)>3:
				x=x.split('/')
				# print(x)
				if len(x)==3:
					return x[0]+'/'+str(Calendra_dict[x[1].strip().lower()])+'/'+x[-1]
				else:
					return ''	
			else:
				return ''
		except:
			return ''

	def removeDuplicate(x):
		if type(x)==np.float:
			return ''
		else:
			x=re.sub('[^A-Za-z()]+',' ', x)
			x=x.split('(')
			return x[0]
		
	def fun1(x):
		if x=="paranagua brazil":
			return x.split()[0]
		elif x=="santos brazil":
			return x.split()[0]
		else:
			return x
				



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
	 


	
	Destination=os.path.abspath(os.getcwd()).replace('glovis','')

	pdflist = glob.glob(os.path.join("*.pdf"))
	for f in pdflist:
		os.remove(f)


	#combined all csv file and name LGL_complete.csv
	#after sending message and email remove all file except port.csv
	csvlist = glob.glob(os.path.join("*.csv"))
	csvlist.remove('port.csv')
	csvlist.remove('NewPortCode.csv')
	df = pd.concat([pd.read_csv(f'{f}') for f in csvlist ],ignore_index=True)
	   
	# df=df.iloc[:,1:]
	df=df.replace(np.nan,'')
	df=df.replace('NA','')
	# df['Date of Arrival (ETA)']=df['Date of Arrival (ETA)'].apply(lambda x:Date_new(x))
	df=df[['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)']]
	
	df.reset_index(drop=True, inplace=True)
	
	DelDateCol1=df['Date of Arrival (ETA)'].apply(lambda x:CurrentDate_upto(x))
	DelDateColIndex1=[x for x in range(0,len(DelDateCol1)) if DelDateCol1[x]]

	DelDateColIndex=list(set(DelDateColIndex1))

	df.drop(DelDateColIndex , inplace=True)
	df['Port Name']=df['Port Name'].apply(lambda x:removeDuplicate(x))
	df['Port Name']=df['Port Name'].apply(lambda x :fun1(x))
	
	for index,row in df.iterrows():
		#print(row['Port Name'],row['port_code'])
		if type(row['Port Name'])!=type(np.nan):
			print(row['Port Name'])
			if row['Port Name'].lower().strip()=='cartagena':
				df['port_code'][index]="CO CTG"



	for index,row in df.iterrows():
		if type(row['Port Name'])==type(np.nan):
			df['Port Name'][index]=""
			df['port_code'][index]=""
			
			
		else:
			
			
			if "baltimore" in row['Port Name'].lower():
				df['Port Name'][index]="baltimore".title()
				df['port_code'][index]="US BAL"
			
			elif "'aqaba" in row['Port Name'].lower() or "aqaba" in row['Port Name'].lower() :
				df['Port Name'][index]="Aqaba".title()
				df['port_code'][index]="JO AQJ"
				 
			elif "brunswick" in row['Port Name'].lower():
				df['Port Name'][index]="brunswick".title()
				df['port_code'][index]=""
				
			elif "borusan" in row['Port Name'].lower():
				df['Port Name'][index]="borusan".title()
			
			elif "cartagena" in row['Port Name'].lower():
				df['Port Name'][index]="cartagena".title()
			
			elif "charleston" in row['Port Name'].lower():
				df['Port Name'][index]="charleston".title()
			
			elif "freeport" in row['Port Name'].lower():
				df['Port Name'][index]="freeport".title()
			
			elif "galveston" in row['Port Name'].lower():
				df['Port Name'][index]="galveston".title()
			
			elif "hamad" in row['Port Name'].lower():
				df['Port Name'][index]="hamad".title()

			elif "jeddah" in row['Port Name'].lower():
				df['Port Name'][index]="jeddah".title()
				df['port_code'][index]="SA JED"
			
			elif "kuwait" in row['Port Name'].lower():
				df['Port Name'][index]="kuwait".title()
				df['port_code'][index]="KW KWI"
				
			elif "masan" in row['Port Name'].lower():
				df['Port Name'][index]="masan".title()
				df['port_code'][index]="KR MAS"
			
			elif "manzanillo" in row['Port Name'].lower():
				df['Port Name'][index]="manzanillo".title()
			
			
			elif "newark" in row['Port Name'].lower():
				df['Port Name'][index]="newark".title()
			

			elif "new york" in row['Port Name'].lower() or "newyork" in row['Port Name'].lower() :
				df['Port Name'][index]="new york".title()
				df['port_code'][index]="US NYC"
					
			
			elif "newcastle" in row['Port Name'].lower():
				df['Port Name'][index]="newcastle".title()
			
			elif "paranagua" in row['Port Name'].lower():
				df['Port Name'][index]="paranagua".title()
			
			elif "philadelphia" in row['Port Name'].lower():
				df['Port Name'][index]="philadelphia".title()
			
			elif "puerto caldera" in row['Port Name'].lower():
				df['Port Name'][index]="puerto caldera".title()
				df['port_code'][index]="CL PMC"
			
			elif "puerto cortes" in row['Port Name'].lower():
				df['Port Name'][index]="puerto cortes".title()
				df['port_code'][index]="HN PCR"
			
			elif "puerto limon" in row['Port Name'].lower():
				df['Port Name'][index]="puerto limon".title()
				df['port_code'][index]=""
			
			elif "san lorenzo" in row['Port Name'].lower():
				df['Port Name'][index]="san lorenzo".title()
				df['port_code'][index]="HN SLO"
				
			elif "santo domingo" in row['Port Name'].lower():
				df['Port Name'][index]="santo domingo".title()
				df['port_code'][index]="DO SDQ"
				
			elif "santos" in row['Port Name'].lower():
				df['Port Name'][index]="santos".title()
				df['port_code'][index]="BR SSZ"

			elif "shanghai" in row['Port Name'].lower():
				df['Port Name'][index]="shanghai".title()
				df['port_code'][index]="CN SHA"
			

			elif "tacoma" in row['Port Name'].lower():
				df['Port Name'][index]="tacoma".title()
				df['port_code'][index]="US ACI"
			

			elif "wilmington" in row['Port Name'].lower():
				df['Port Name'][index]="wilmington".title()
			
			elif "altamira" in row['Port Name'].lower():
				df['Port Name'][index]="altamira".title()
				df['port_code'][index]="MX ATM"
				
			elif "aratu" in row['Port Name'].lower():
				df['Port Name'][index]="aratu".title()
			
			elif "zarate" in row['Port Name'].lower():
				df['Port Name'][index]="zarate".title()
			
			elif "altamira" in row['Port Name'].lower():
				df['Port Name'][index]="altamira".title()
				df['port_code'][index]="MX ATM"
				
			elif "new westminster" in row['Port Name'].lower():
				df['Port Name'][index]="new westminster".title()
				df['port_code'][index]="" 
	  
			elif "abu dhabi" in row['Port Name'].lower() or "abu" in row['Port Name'].lower():
				df['Port Name'][index]="abu dhabi".title()
				df['port_code'][index]=""   

			elif "ad dammam" in row['Port Name'].lower():
				df['Port Name'][index]="ad dammam".title()
				df['port_code'][index]=""     
				
			elif "bahrain" in row['Port Name'].lower():
				df['Port Name'][index]="bahrain".title()
				df['port_code'][index]="BH KBS"

				
			elif "corpus" in row['Port Name'].lower():
				df['Port Name'][index]="corpus".title()
				df['port_code'][index]="US CRP"

			elif "eca ent.point usec jxv/buw/svn" in row['Port Name'].lower():
				df['Port Name'][index]="eca ent.point usec jxv/buw/svn".title()
				df['port_code'][index]=""
				
			elif "el iskandariya (alexandria)" in row['Port Name'].lower():
				df['Port Name'][index]="el iskandariya (alexandria)".title()
				df['port_code'][index]=""
				
			elif "fort de france" in row['Port Name'].lower():
				df['Port Name'][index]="fort de france".title()
				df['port_code'][index]="MQ FDF"
				
			elif "hai phong" in row['Port Name'].lower():
				df['Port Name'][index]="hai phong".title()
				df['port_code'][index]=""
				
			elif "ho chi minh" in row['Port Name'].lower():
				df['Port Name'][index]="ho chi minh".title()
				df['port_code'][index]="VN SGN"
				
			elif "honolulu" in row['Port Name'].lower():
				df['Port Name'][index]="honolulu".title()
				df['port_code'][index]="US HNL"
				
			elif "houston" in row['Port Name'].lower():
				df['Port Name'][index]="houston".title()
				df['port_code'][index]="US HOU"            
				
			elif "huangpu" in row['Port Name'].lower():
				df['Port Name'][index]="huangpu".title()
				df['port_code'][index]=""              
				
			elif "jakarta" in row['Port Name'].lower():
				df['Port Name'][index]="jakarta".title()
				df['port_code'][index]="ID TPP"   

			elif "jebel" in row['Port Name'].lower():
				df['Port Name'][index]="jebel".title()
				df['port_code'][index]="AE JEA"   

			elif "keelung" in row['Port Name'].lower():
				df['Port Name'][index]="keelung".title()
				df['port_code'][index]="TW KEL"   

			elif "kingston" in row['Port Name'].lower():
				df['Port Name'][index]="kingston".title()
				df['port_code'][index]="JM KIN"   

			elif "koper" in row['Port Name'].lower():
				df['Port Name'][index]="koper".title()
				df['port_code'][index]="SI KOP"   

			elif "lehavre" in row['Port Name'].lower().strip() or "le havre" in row['Port Name'].lower():
				df['Port Name'][index]="le havre".title()
				df['port_code'][index]="FR LEH"   
				
			elif "lian yun gang" in row['Port Name'].lower():
				df['Port Name'][index]="lian yun gang".title()
				df['port_code'][index]=""   

			elif "livorno" in row['Port Name'].lower():
				df['Port Name'][index]="livorno".title()
				df['port_code'][index]="IT LIV"   

			elif "long beach" in row['Port Name'].lower():
				df['Port Name'][index]="long beach".title()
				df['port_code'][index]="US LGB"   

			elif "mobile" in row['Port Name'].lower():
				df['Port Name'][index]="mobile".title()
				df['port_code'][index]="US MOB"   
				
			elif "mumbai" in row['Port Name'].lower():
				df['Port Name'][index]="mumbai".title()
				df['port_code'][index]="IN BOM"   

																
			elif "nagoya" in row['Port Name'].lower():
				df['Port Name'][index]="nagoya".title()
				df['port_code'][index]="JP NGO"   

			elif "port elizabeth" in row['Port Name'].lower():
				df['Port Name'][index]="port elizabeth".title()
				df['port_code'][index]="ZA PLZ"   

			elif "port everglades" in row['Port Name'].lower():
				df['Port Name'][index]="port everglades".title()
				df['port_code'][index]="US PEF"   

				
			elif "port hueneme" in row['Port Name'].lower():
				df['Port Name'][index]="port hueneme".title()
				df['port_code'][index]=""   

			elif "port kelang" in row['Port Name'].lower() or "port klang" in row['Port Name'].lower():
				df['Port Name'][index]="port kelang".title()
				df['port_code'][index]="MY PKL"   

			elif "port kembla" in row['Port Name'].lower():
				df['Port Name'][index]="port kembla".title()
				df['port_code'][index]=""   

			elif "port of spain" in row['Port Name'].lower():
				df['Port Name'][index]="port of spain".title()
				df['port_code'][index]=""   

			elif "port louis" in row['Port Name'].lower():
				df['Port Name'][index]="port louis".title()
				df['port_code'][index]="MU PLU"   

			elif "port moresby" in row['Port Name'].lower():
				df['Port Name'][index]="port moresby".title()
				df['port_code'][index]="PG POM"   

			elif "port reunion" in row['Port Name'].lower():
				df['Port Name'][index]="port reunion".title()
				df['port_code'][index]="RE PDG"   

			elif "port sudan" in row['Port Name'].lower():
				df['Port Name'][index]="port sudan".title()
				df['port_code'][index]="SD PZU"   

			elif "port-au-prince" in row['Port Name'].lower():
				df['Port Name'][index]="port-au-prince".title()
				df['port_code'][index]=""   

			elif "pt elizabeth" in row['Port Name'].lower():
				df['Port Name'][index]="pt elizabeth".title()
				df['port_code'][index]="ZA PLZ"   

			elif "puerto" in row['Port Name'].lower():
				df['Port Name'][index]="puerto".title()
				df['port_code'][index]="HN PCR"   

			elif "qingdao" in row['Port Name'].lower():
				df['Port Name'][index]="qingdao".title()
				df['port_code'][index]="CN TAO"   

			elif ("rio de janeiro" in row['Port Name'].lower()) or ("rio" == row['Port Name'].lower()):
				df['Port Name'][index]="rio de janeiro".title()
				df['port_code'][index]="BR RIO"   

			elif "rio grande" in row['Port Name'].lower():
				df['Port Name'][index]="rio grande".title()
				df['port_code'][index]="BR RIG"   

			elif "rio haina" in row['Port Name'].lower():
				df['Port Name'][index]="rio haina".title()
				df['port_code'][index]="DO HAI"   

			elif ("san antonio" in row['Port Name'].lower()) or ("san" == row['Port Name'].lower()):
				df['Port Name'][index]="san antonio".title()
				df['port_code'][index]="CL SAI"   
				
			elif "san diego" in row['Port Name'].lower():
				df['Port Name'][index]="san diego".title()
				df['port_code'][index]=""   
				
			elif "san juan" in row['Port Name'].lower():
				df['Port Name'][index]="san juan".title()
				df['port_code'][index]="NI SJS"  
				
			elif ("santa" == row['Port Name'].lower()) or ("santa marta" == row['Port Name'].lower()):
				df['Port Name'][index]="santa marta".title()
				df['port_code'][index]="AR SFN"   
				
			elif "savannah" in row['Port Name'].lower():
				df['Port Name'][index]="savannah".title()
				df['port_code'][index]="US SAV"   
				
			elif "st john's" in row['Port Name'].lower():
				df['Port Name'][index]="st john's (ant)".title()
				df['port_code'][index]=""   

			elif "st. petersburg" in row['Port Name'].lower():
				df['Port Name'][index]="st. petersburg".title()
				df['port_code'][index]="RU LED"   

			elif "suape" in row['Port Name'].lower():
				df['Port Name'][index]="suape".title()
				df['port_code'][index]=""   

			elif "tamatave" in row['Port Name'].lower():
				df['Port Name'][index]="tamatave".title()
				df['port_code'][index]="MG TOA"   

			elif "Tianjin" in row['Port Name'].lower():
				df['Port Name'][index]="Tianjin".title()
				df['port_code'][index]="CN TSN"   

			elif "toyohashi" in row['Port Name'].lower():
				df['Port Name'][index]="toyohashi".title()
				df['port_code'][index]=""   

			elif "veracruz" in row['Port Name'].lower():
				df['Port Name'][index]="veracruz".title()
				df['port_code'][index]="MX VER"   

			elif "xingang" in row['Port Name'].lower():
				df['Port Name'][index]="xingang".title()
				df['port_code'][index]=""   
			#add fri 17-jul
			elif ("goteborg" in row['Port Name'].lower()) or ("gothenburg" in row['Port Name'].lower().strip()):
				df['Port Name'][index]="Gothenburg".title()
				df['port_code'][index]="SE GOT"

			elif ("antwerp" in row['Port Name'].lower().strip()) or ("antwerpen" in row['Port Name'].lower().strip()):
				df['Port Name'][index]="Antwerpen".title()
				df['port_code'][index]="BE ANR"
			#end		


			elif ("zeebrugge" in row['Port Name'].lower().strip()):
				df['Port Name'][index]="zeebrugge".title()
				df['port_code'][index]="BE ZEE"
			#end		
																																																																										
			else:
				#print(df['Port Name'][index])
				df['Port Name'][index]=df['Port Name'][index].title()


		
	index1=list(df.index[df['Port Name']=="Port"]) 
		
	index2=list(df.index[df['Port Name']=="New"]) 
	index3=list(df.loc[pd.isna(df["Port Name"]), :].index)
	totalDel=index1+index2+index3
	totalDel=list(set(totalDel))
	df.drop(totalDel , inplace=True)

	#----------------------------------------new code for port code-----------------------------------------------
	 
	df=df.replace(np.nan,'')

	port_df1=pd.read_csv("NewPortCode.csv")

	port_df1['Port Name']=port_df1['Port Name'].apply(lambda x :x.strip())


	for index,row in df.iterrows():
		if len(row['port_code'])<4 and len(row['port_code'])!=2:
			if port_df1[port_df1['Port Name']==row['Port Name'].strip()].shape[0]>0:
				portCode=port_df1[port_df1['Port Name']==row['Port Name'].strip()]['Port_code'].values
				df['port_code'][index]=portCode[0]


	df=df.drop_duplicates(subset=['Carrier','Route Code','Vessel Name','Vessel Capacity (in MT)','Vessel Ramp Height (in meters)','Voyage Number','Port Name','port_code','Date of Arrival (ETA)'])



	index1=list(df.index[df['Port Name']==""]) 
		
	index2=list(df.index[df['port_code']==""]) 

	#index3=list(df.index[df['Date of Arrival (ETA)']==""]) 


	totalDel=index2+index1

	totalDel=list(set(totalDel))

	df.drop(totalDel , inplace=True)

	df.reset_index(drop=True, inplace=True)    

	#----------------------------------------------------------- End  ---------------------------------------------------

	df['Vessel Capacity (in MT)']=df['Vessel Capacity (in MT)'].apply(lambda x :OnlyNumbersRampHeight_RampCapacity(x))

	df['Vessel Ramp Height (in meters)']=df['Vessel Ramp Height (in meters)'].apply(lambda x :OnlyNumbersRampHeight_RampCapacity(x))


	df.to_csv("Glovis.csv",index=False)

	shutil.move("Glovis.csv",Destination+"Glovis.csv")
	print("Glovis complete ..")
	#now send email code and remove all csv file
	#csvlist.append('Complete_LGL.csv')#after sending email

	for f in csvlist:
		os.remove(f)
except Exception as e:
	print(e)
	pass