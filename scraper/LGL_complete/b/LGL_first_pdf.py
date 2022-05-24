
#http://libertygl.com/routeschedtable/view-schedule/us-flag-service.html
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
from time import sleep
import wget
import tabula
import os
import pandas as pd
import os
import numpy as np
import re
from cleaning import clean_df_with_port_code


#url="http://libertygl.com/wp-content/uploads/2020/06/LGL-SAILING-SCHEDULE-12-June-2020-US-FLAG.pdf"
#use curl command

print("begning Lgl_first")
try:

	def date_clean(string):
		CheckDate=re.sub('[^A-Za-z0-9-]+',' ', string)
		if len(CheckDate)>1:
			return CheckDate
		else:
			return 'NAN'

	def clean_voyage(x):
		p=re.sub('[^0-9]+',' ', x)
		p=p.strip()
		p=p.split(' ')[0]
		return p
		
	def insert_portCode(df):
		prot_df=pd.read_csv("port.csv")
		port_list=[]

		for index,row in df.iterrows():
			if prot_df[prot_df['portName'].str.contains(row['Port Name'])].shape[0]>0:
				portCode=prot_df[prot_df['portName'].str.contains(row['Port Name'])]['CODE'].values
				if portCode.shape[0]>0:            
					port_list.append(portCode[0])
				else:
					port_list.append("NA")
			elif len(row['Port Name'].split(' '))>0:#space cheacking then take first string  
				#check someone have , or (  remove it
				portName=re.sub('[^A-Za-z0-9]+', '', row['Port Name'].split(' ')[0])
				portCode=prot_df[prot_df['portName'].str.contains(portName)]['CODE'].values
				if portCode.shape[0]>0:            
					port_list.append(portCode[0])
				else:
					port_list.append("NA")
			else:
				df['port_code'].append("NA")
			
		df['port_code']=pd.Series(port_list)
		return df
		


	def pdf_to_csv(Westbound_voyage_index,Westbound_df):
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
		if len(Westbound_voyage_index)>1:
			for i in range(0,len(Westbound_voyage_index)):
				if i==(len(Westbound_voyage_index)-1): 
					sample_df=Westbound_df.iloc[Westbound_voyage_index[i]:]
					#print(sample_df.shape) 
					Vassel_names=sample_df.columns[1:].to_list()            
					
					Voyage_list=sample_df.iloc[0,1:].to_list()   
					
					Port_name=sample_df.iloc[:,0][1:].to_list()            
					print(Port_name)		
					Voyage_no=[clean_voyage(x) for x in Voyage_list]            
						   
					
					for ind, column in enumerate(sample_df.columns[1:]):
						data_dict['Vessel Name'].extend([Vassel_names[ind] for x in range(1,(sample_df.shape[0]))])
						data_dict['Voyage Number'].extend([Voyage_no[ind] for x in range(1,(sample_df.shape[0]))])
						data_dict['Port Name'].extend(Port_name)
						
						data_dict['Date of Arrival (ETA)'].extend(date_clean(ETA) for ETA in sample_df.iloc[:,ind+1][1:].to_list())
						data_dict['Carrier'].extend(["LIBERTY GLOBAL LOGISTICS" for x in  range(1,(sample_df.shape[0]))])
						data_dict['Date of Departure (ETD)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Route Code'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Vessel Capacity (in MT)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Vessel Ramp Height (in meters)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
		
		
					#print("************************************************************\n")
				else:

					sample_df=Westbound_df.iloc[Westbound_voyage_index[i]:Westbound_voyage_index[i+1]]
					#print(sample_df.shape) 
							   
					Vassel_names=sample_df.columns[1:].to_list()            
					
					Voyage_list=sample_df.iloc[0,1:].to_list()   
					
					Port_name=sample_df.iloc[:,0][1:].to_list()            
					print(Port_name)		
					Voyage_no=[clean_voyage(x) for x in Voyage_list]            
						   
					
					for ind, column in enumerate(sample_df.columns[1:]):
						data_dict['Vessel Name'].extend([Vassel_names[ind] for x in range(1,(sample_df.shape[0]))])
						data_dict['Voyage Number'].extend([Voyage_no[ind] for x in range(1,(sample_df.shape[0]))])
						data_dict['Port Name'].extend(Port_name)
						data_dict['Date of Arrival (ETA)'].extend(date_clean(ETA) for ETA in sample_df.iloc[:,ind+1][1:].to_list())
						data_dict['Carrier'].extend(["LIBERTY GLOBAL LOGISTICS" for x in  range(1,(sample_df.shape[0]))])
						data_dict['Date of Departure (ETD)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Route Code'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Vessel Capacity (in MT)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
						data_dict['Vessel Ramp Height (in meters)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
		
					#print("****************************************************************\n")
			return data_dict
			
		else:
		
			sample_df=Westbound_df  
			#print(sample_df.shape)                 
			Vassel_names=sample_df.columns[1:].to_list()            
			
			Voyage_list=sample_df.iloc[0,1:].to_list()   
			
			Port_name=sample_df.iloc[:,0][1:].to_list()            
			print(Port_name)			
			Voyage_no=[clean_voyage(x) for x in Voyage_list]            
				   
			
			for ind, column in enumerate(sample_df.columns[1:]):
				data_dict['Vessel Name'].extend([Vassel_names[ind] for x in range(1,(sample_df.shape[0]))])
				data_dict['Voyage Number'].extend([Voyage_no[ind] for x in range(1,(sample_df.shape[0]))])
				data_dict['Port Name'].extend(Port_name)
				##print(sample_df.iloc[:,ind][1:].to_list())
				data_dict['Date of Arrival (ETA)'].extend(date_clean(ETA) for ETA in sample_df.iloc[:,ind+1][1:].to_list())
				data_dict['Carrier'].extend(["LIBERTY GLOBAL LOGISTICS" for x in  range(1,(sample_df.shape[0]))])
				data_dict['Date of Departure (ETD)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
				data_dict['Route Code'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
				data_dict['Vessel Capacity (in MT)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
				data_dict['Vessel Ramp Height (in meters)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])

			#print("****************************************************************\n")
			return data_dict


	URL = 'http://libertygl.com/routeschedtable/view-schedule/us-flag-service.html'
	
	content = requests.get(URL)
	
	soup = BeautifulSoup(content.text, 'lxml')
	
	pdf_link=soup.find_all('iframe')[0]['src']
	wget.download(pdf_link,'pdf1.pdf')

	sleep(5)

	df_dataset = tabula.read_pdf('pdf1.pdf',multiple_tables = True,encoding='utf-8',pages='all')
	
	for i in range(0,len(df_dataset)):
		if df_dataset[i].shape[0]>1:
			df_dataset=df_dataset[i]
			break
			
	sleep(5)
	df=df_dataset.copy()

	df=df.replace(np.nan,'NAN')

	split_index= df[df.iloc[:,1].str.contains('Liberty')].index[0]

	Eastbound_df=df.iloc[:split_index:]


	Eastbound_voyage_index=Eastbound_df[Eastbound_df.iloc[:,1].str.contains('Voyage')].index.to_list()

	sleep(2)
	#check also of east bound

	######################################################################################################
	Westbound_df=df.iloc[split_index:]
	#now column create in westbound
	Westbound_df.columns=Westbound_df.iloc[0,:]
	Westbound_df=Westbound_df.iloc[1:].reset_index(drop=True)

	Westbound_voyage_index=Westbound_df[Westbound_df.iloc[:,1].str.contains('Voyage')].index.to_list()

	##################################
	Eastbound_csv=pdf_to_csv(Eastbound_voyage_index,Eastbound_df)  


	Westbound_csv=pdf_to_csv(Westbound_voyage_index,Westbound_df)  


	sleep(2)
	Eastbound_csv_df=pd.DataFrame(Eastbound_csv)

	Eastbound_csv_df.to_csv('Eastbound.csv')


	Westbound_csv_df=pd.DataFrame(Westbound_csv)

	Westbound_csv_df.to_csv('Westbound.csv')


	#now combined both files

	sleep(2)
	all_filenames=['Eastbound.csv','Westbound.csv']
	#combine all files in the list
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
	#export to csv
	combined_csv.to_csv( "lgl_1.csv", index=False, encoding='utf-8-sig')

	#remove file


	masterDf=pd.read_csv('lgl_1.csv')
	clean_df_with_port_code(masterDf)

	all_filenames=['Eastbound.csv','Westbound.csv','new.csv','lgl_1.csv']

	[os.remove(file) for file in all_filenames]
	sleep(2)

except Exception as e:
	#print(e)
	pass


















			 
			
			
			
			



			