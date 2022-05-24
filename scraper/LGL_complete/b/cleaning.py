#clean date and same format
#if date have two split 
#port code
import os
import glob
import pandas as pd
import re
import tabula

def port_code_substring(x):
    x=re.sub('[^A-Za-z()]+',' ', x)
    
    if len(x.split(','))>1:
        x=x.split(',')[0].strip()
        return x.lower()[3:-2]
        
        #now remove white space and comma
    
    elif len(x.split(' '))>1:
        x=x.split(' ')[0].strip()

        return x.lower()[3:-2]
        
    
    elif '(' in x:
        x=re.sub(r'\([^)]*\)', '', x)
        return x.lower()[3:-2]



def clean_vassel(string):
    vassel_name=re.sub('[^A-Za-z]+',' ', string)
    if len(vassel_name)>1:
        return vassel_name
    else:
        return 'NAN'

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
    
    


def clean_df_with_port_code(masterDf):
    
    if masterDf.columns.str.contains('Unnamed').argmax()==0:
        masterDf=masterDf.iloc[:,1:]
    
    #now cleaning Vassel_name
    masterDf['Vessel Name']=masterDf['Vessel Name'].apply(lambda x: clean_vassel(x))    
        
    masterDf['Date of Arrival (ETA)']=masterDf['Date of Arrival (ETA)'].apply(lambda x: Date_clean(x))
    
    # Get names of indexes for which column Age has value 30
    indexNames = masterDf[(masterDf['Date of Arrival (ETA)'] =="NAN") | (masterDf['Date of Arrival (ETA)'] =="-2020")].index
    # Delete these row indexes from dataFrame
    masterDf.drop(indexNames , inplace=True)
    
    #delete eta that have NAN
    
    masterDf.to_csv('new.csv',index=False)
    
    #print(masterDf.shape)
    #print("*************************************************************")
    port_df=pd.read_csv("port.csv")
    df=pd.read_csv("new.csv")
    port_list=[]
    
    
    
    for index,row in df.iterrows():
        port_name=port_code_substring(row['Port Name'])
        #port_list.append(port_name)
        if port_df[port_df['portName'].str.contains(port_name)].shape[0]>0:
            portCode=port_df[port_df['portName'].str.contains(port_name)]['CODE'].values
            if portCode.shape[0]>0:            
                port_list.append(portCode[0])
            else:
                port_list.append("NA")
    
    
    df['port_code']=pd.Series(port_list)
    
    df.to_csv("LGL_first_pdf.csv",index=False)

    





