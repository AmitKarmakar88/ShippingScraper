
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

print("begning LGL_second_pdf")

try:
	def only_no(x):
		p=re.sub('[^0-9.]+',' ', x)
		return p.strip()

	def Date_clean(x):
		if len(x)>3:#it means Date is no null
			x=x.split(' ')[0]
			p=re.sub('[^A-Za-z0-9-]+',' ', x)
			if not '2020' in p and len(p)>1:
				return p+'-2020'
			elif len(p)==0:
				return "NAN"
			return p
		else:
			return "NAN"
	   
	def port_code_substring(x):
		x=re.sub('[^A-Za-z()]+',' ', x)
		
		if len(x.split(','))>1:
			x=x.split(',')[0].strip()
			return x.lower()[1:-2]
			
			#now remove white space and comma
		
		elif len(x.split(' '))>1:
			x=x.split(' ')[0].strip()

			return x.lower()[1:-2]
			
		
		elif '(' in x:
			x=re.sub(r'\([^)]*\)', '', x)
			return x.lower()[1:-2]
		else:
			return "NA"


	URL = 'http://libertygl.com/routeschedtable/view-schedule/commercial-service.html'
	
	content = requests.get(URL)
	
	soup = BeautifulSoup(content.text, 'lxml')
	
	pdf_link=soup.find_all('iframe')[0]['src']
	wget.download(pdf_link,'pdf2.pdf')
	sleep(5)
	df_dataset = tabula.read_pdf('pdf2.pdf',multiple_tables = True,encoding='utf-8',pages='all')
	
	for i in range(0,len(df_dataset)):
		if df_dataset[i].shape[0]>1:
			df_dataset=df_dataset[i]
			break
	sleep(3)
	df=df_dataset.copy()

	df.columns=df.iloc[0,:].reset_index()

	df=df.replace(np.nan,"NAN")

	#df.to_csv('demo.csv',index=False)

	total_vassel_list=df.columns[1:].to_list()#in this list total column but we want only for Vassel name

	if total_vassel_list:

		total_vassel_list=total_vassel_list[:len(total_vassel_list)//2]#removed nan column from list
			
		Vassel_name,Voyage_no = zip(*(s[1].split("\r") for s in total_vassel_list))
		
		Voyage_no=[only_no(x) for x in Voyage_no]

	sleep(2)

	weight_height_list=[x for i, x in enumerate(df.iloc[1,1:].to_list()) if x!="NAN"]#find weith and height

	if weight_height_list:
		
		Max_height,Max_weight= zip(*(s.split("/") for s in weight_height_list))
			
		Max_weight=[only_no(x) for x in Max_weight]
		
		Max_height=[only_no(x) for x in Max_height]



	Cutoff_column_indexs=[i for i, x in enumerate(df.iloc[2,:].str.contains("Cut Off")) if x]


	df = df.drop(df.columns[Cutoff_column_indexs],axis=1)

	#now we create columns as vassel name
	columns=[column for column in Vassel_name]
	columns.insert(0,"portName")

	df.columns=columns

	df=df.iloc[3:,:]

	sleep(2)
	#now we will split Dataframe so we remove all data after apart containing

	for i in range(1,df.shape[1]):
		if any(df.iloc[:,i].str.contains("Email")):
			#print(df[df.iloc[:,2].str.contains("Email")].index)
			crop=(df[df.iloc[:,2].str.contains("Email")].index[0]-5)
			#now crop dataframe
			df=df.iloc[:crop]

	#also remove portname column NAN
	port_empty=[i for i, x in enumerate(df.iloc[:,0].str.contains("NAN")) if x]
		   
	df = df[~df.portName.str.contains("NAN")] 

	df.reset_index(drop=True, inplace=True)


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


	sample_df=df.copy()


	Port_name=sample_df.iloc[:,0][1:].to_list()
	print(Port_name)
	for ind, column in enumerate(sample_df.columns[1:]):
		data_dict['Vessel Name'].extend([Vassel_name[ind] for x in range(1,(sample_df.shape[0]))])
		data_dict['Voyage Number'].extend([Voyage_no[ind] for x in range(1,(sample_df.shape[0]))])
		data_dict['Port Name'].extend(Port_name)
		
		data_dict['Date of Arrival (ETA)'].extend(Date_clean(ETA) for ETA in sample_df.iloc[:,ind+1][1:].to_list())
		data_dict['Carrier'].extend(["LIBERTY GLOBAL LOGISTICS" for x in  range(1,(sample_df.shape[0]))])
		data_dict['Date of Departure (ETD)'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
		data_dict['Route Code'].extend(["NAN" for x in range(1,(sample_df.shape[0]))])
		data_dict['Vessel Capacity (in MT)'].extend([Max_weight[ind] for x in range(1,(sample_df.shape[0]))])
		data_dict['Vessel Ramp Height (in meters)'].extend([Max_height[ind] for x in range(1,(sample_df.shape[0]))])


	MasterDf=pd.DataFrame(data_dict)

	indexNames = MasterDf[(MasterDf['Date of Arrival (ETA)'] =="----") | (MasterDf['Date of Arrival (ETA)']=='-----2020')].index
	# Delete these row indexes from dataFrame
	MasterDf.drop(indexNames , inplace=True)

	#MasterDf.to_csv( "Second_pdf.csv", index=False, encoding='utf-8-sig')
	sleep(2)


	port_df=pd.read_csv("port.csv")
	port_list=[]
	for index,row in MasterDf.iterrows():
		port_name=port_code_substring(row['Port Name'])
		#port_list.append(port_name)
		if port_df[port_df['portName'].str.contains(port_name)].shape[0]>0:
			portCode=port_df[port_df['portName'].str.contains(port_name)]['CODE'].values
			if portCode.shape[0]>0:            
				port_list.append(portCode[0])
			else:
				port_list.append("NA")


	MasterDf['port_code']=pd.Series(port_list)

	MasterDf.to_csv("LGL_second_pdf.csv",index=False)

	sleep(2)

except Exception as e:
	#print(e)
	pass










