# import wget
# import tabula
# import os
# import pandas as pd
# import numpy as np
# from time import sleep
# import re


# def clean_Date(x):
#     p=re.sub('[^0-9-]+',' ', x).strip()
#     if len(p)>1:
#         if p in x:
#             return x+'-2020'
#         else:
#            return "NA"
#     else:
#         return "NA"        
  


# def clean_ramp(x):
#     p=re.sub('[^0-9.,]+',' ', x)
#     return p

    
# def port_code_substring(x):
#     x=re.sub('[^A-Za-z(), ]+',' ', x)
    
#     if len(x.split(','))>1:
#         x=x.split(',')[0].strip()
#         return x.lower()
        
#     elif '(' in x:
#         x=re.sub(r'\([^)]*\)', '', x)
#         return x.lower()

#         #now remove white space and comma
    
#     elif len(x.split(' '))>1:
#         x=x.split(' ')[0].strip()

#         return x.lower()
        
    

#     elif len(x)>3:
#         return x.lower()

    
#     else:
#         return "NA"

  
# data_dict={}
# data_dict['Vessel Name']=[]
# data_dict['Voyage Number']=[]
# data_dict['Port Name']=[]
# data_dict['Carrier']=[]
# data_dict['Date of Arrival (ETA)']=[]
# data_dict['Date of Departure (ETD)']=[]
# data_dict['Route Code']=[]
# data_dict['Vessel Capacity (in MT)']=[]
# data_dict['Vessel Ramp Height (in meters)']=[]    



# df=pd.read_html("a8.html")[0]

# df=df.replace(np.nan,'NA')
# df=df.replace('SKIP','NA')
# df=df.replace('-','NA')
  


# Ramp_capacity=[data.replace('Tons Ramp /','').strip() for data in df.iloc[1,:] if 'Tons Ramp /' in str(data)]

# Max_Deck_Height =[500,500,500,500]

# Vessel_Name=['WESTERN HIGWHAY','WESTERN HIGWHAY','IVORY ARROW','WESTERN HIGWHAY']

# Voyage_No=[data for data in df.iloc[4,:][1:] if "NA" not in data]

# columnsName=list(df.columns)
# columnsName=[columnsName[i] for i in range(0,len(columnsName)) if i%2!=0 or i==0]

# df=df[columnsName]

# df=df.iloc[5:,]
# df.reset_index(drop=True, inplace=True)

# for index,row in df.iterrows():
#     port_name=row[0]
#     #print(port_name)
#     for i in range(1,len(Voyage_No)+1):
#         data_dict['Carrier'].append("K-LINE")
#         data_dict['Vessel Name'].append(Vessel_Name[i-1])
#         data_dict['Voyage Number'].append(Voyage_No[i-1])
#         data_dict['Port Name'].append(port_name.lower())
#         data_dict['Date of Arrival (ETA)'].append(row[i])
#         data_dict['Date of Departure (ETD)'].append("NA")
#         data_dict['Vessel Capacity (in MT)'].append(Ramp_capacity[i-1])
#         data_dict['Vessel Ramp Height (in meters)'].append(Max_Deck_Height[i-1])
#         data_dict['Route Code'].append("NA-SA")
#     #print("_____________________________________________________________________")
   
    
    
    
# MasterDf=pd.DataFrame(data_dict)


# MasterDf['Date of Arrival (ETA)']=MasterDf['Date of Arrival (ETA)'].apply(lambda x :clean_Date(x))

# MasterDf['Vessel Capacity (in MT)']=MasterDf['Vessel Capacity (in MT)'].apply(lambda x:clean_ramp(x))



# indexNames = MasterDf[(MasterDf['Date of Arrival (ETA)'] =="NA")].index
#     # Delete these row indexes from dataFrame
# MasterDf.drop(indexNames , inplace=True)

# port_df=pd.read_csv("port.csv")

# port_list=[]
# for index,row in MasterDf.iterrows():
#     port_name=port_code_substring(row['Port Name']) 
#     if port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)].shape[0]>0:
#         portCode=port_df[port_df['portName'].str.contains(port_name, na=False, regex=True,flags=re.IGNORECASE)]['CODE'].values
#         #print('len=',len(port_name),port_name,portCode[0])
#         port_list.append(portCode[0])
#     else:
#         #print('len=',len(port_name),'NO-----------------')
#         port_list.append("NA")


# MasterDf['port_code']=np.array(port_list)

# MasterDf=MasterDf.replace("NA",'')

# MasterDf.to_csv("a8.csv",index=False)




































