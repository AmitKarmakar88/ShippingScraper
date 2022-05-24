import pandas as pd
from selenium import webdriver
import os
from time import sleep
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import date, timedelta
from selenium.webdriver import ActionChains
import time
import datetime
import re


#FOR HEADLESS BROWSER
from selenium.webdriver.chrome.options import Options

start_time = time.time()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--log-level=0")

url = "https://myacl.aclcargo.com/sspkg/iSched.html"

driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)

driver.get(url)

port_df=pd.read_csv("port.csv")

port_df = port_df.rename(columns = {"portName":"Port Name","CODE":"port_code"})

port_df_new=pd.read_csv("NewPortCode.csv")

port_df_new=port_df_new.rename(columns={"Port_code":"port_code"})

port_df1 = pd.concat([port_df, port_df_new], axis=0,ignore_index=True)

port_df1['Port Name']=port_df1['Port Name'].apply(lambda x :x.strip())

acl_df=pd.DataFrame()

def convert_to_date(s):
    
    today=datetime.datetime.today()
    
    date = re.search(',(.*)@', s).group(1).lstrip()
    
    year = str(today.year)
    
    arrival =  datetime.datetime.strptime(date+year,"%b %d %Y")
    
    # if arrival<today:
    #         arrival = datetime.datetime(arrival.year+1,arrival.month,arrival.day)
    
    arrival=datetime.datetime.strftime(arrival,'%Y/%m/%d')
    
    return arrival


driver.implicitly_wait(30)

driver.find_element_by_id("roro_type").click()

sleep(3)

week_list = driver.find_element_by_id('noOfWeeks')

for option in week_list.find_elements_by_tag_name('option'):
    if option.text == '8 Weeks':
        option.click() # select() in earlier versions of webdriver
        break
        
sleep(2)

el = driver.find_element_by_xpath('//*[@id="pol"]')

final_df=pd.DataFrame()

for option in el.find_elements_by_tag_name('option')[1:]:
    option.click() # select() in earlier versions of webdriver
    
    origin=option.text
    
    sleep(5)
    
    driver.find_element_by_xpath('//*[@id="scheduleHeader"]/tbody/tr[2]/td/table/tbody/tr/td[2]/input[2]').click()
    
    sleep(10)
    
    html_source = driver.page_source
    
    df = pd.read_html(html_source,attrs = {'id': 'scheduleTable'})[0]
    
    df = df[~df[0].str.contains('Departs',na=False)]
    
    final_df = final_df.append(df, ignore_index=True)
    
    driver.find_element_by_xpath('//*[@id="scheduleFooter"]/tbody/tr/td/input').click()
    
    sleep(2)

driver.quit()

final_df = final_df.ffill(axis = 0)

final_df.columns = ["voyage","port","Departs On"]

final_df["Voyage_Name"]=final_df["voyage"].apply(lambda x: x.replace("Voyage",'').strip() if "Voyage" in x else None)

final_df["Vessel_Name"]=final_df["voyage"].apply(lambda x: x.replace("Vessel",'').strip() if "Vessel" in x else None)

final_df['Vessel_Name']=final_df['Vessel_Name'].shift(-1)

final_df["port"] = final_df["port"].apply(lambda x:x.replace("on",'').replace("Departs","").strip())

final_df = final_df.ffill(axis = 0)

                          
final_df=final_df[final_df.voyage.apply(lambda x: False if "Vessel" in x else True)]

                          
final_df["Date of Departure (ETD)"]=''
                          
final_df["Date of Arrival (ETA)"]=final_df.apply(lambda x:convert_to_date(x["Departs On"]) , axis=1)


                          # final_df["Date of Departure (ETD)"]=final_df.apply(lambda x:convert_to_date(x["Departs On"]) if x["voyage"].strip()!="Arrives\xa0at" else '', axis=1) #treat ETD as ETA for originating port
final_df = final_df.rename(columns = {"port":"Port Name","Voyage_Name":"Voyage Number","Vessel_Name":"Vessel Name"})
                          
final_df=final_df[["Vessel Name","Voyage Number","Port Name","Date of Arrival (ETA)","Date of Departure (ETD)"]]
                          
final_df["Carrier"]="ACLCARGO"
                          
final_df["port_code"]=""

for index,row in final_df.iterrows():
    if "baltimore" in row['Port Name'].lower():
        final_df['Port Name'][index]="baltimore".title()
        final_df['port_code'][index]="US BAL"

    elif "'aqaba" in row['Port Name'].lower() or "aqaba" in row['Port Name'].lower() :
        final_df['Port Name'][index]="Aqaba".title()
        final_df['port_code'][index]="JO AQJ"

    elif "brunswick" in row['Port Name'].lower():
        final_df['Port Name'][index]="brunswick".title()
        final_df['port_code'][index]=""

    elif "borusan" in row['Port Name'].lower():
        final_df['Port Name'][index]="borusan".title()

    elif "cartagena" in row['Port Name'].lower():
        final_df['Port Name'][index]="cartagena".title()

    elif "charleston" in row['Port Name'].lower():
        final_df['Port Name'][index]="charleston".title()

    elif "freeport" in row['Port Name'].lower():
        final_df['Port Name'][index]="freeport".title()

    elif "galveston" in row['Port Name'].lower():
        final_df['Port Name'][index]="galveston".title()

    elif "hamad" in row['Port Name'].lower():
        final_df['Port Name'][index]="hamad".title()

    elif "jeddah" in row['Port Name'].lower():
        final_df['Port Name'][index]="jeddah".title()
        final_df['port_code'][index]="SA JED"

    elif "kuwait" in row['Port Name'].lower():
        final_df['Port Name'][index]="kuwait".title()
        final_df['port_code'][index]="KW KWI"

    elif "masan" in row['Port Name'].lower():
        final_df['Port Name'][index]="masan".title()
        final_df['port_code'][index]="KR MAS"

    elif "manzanillo" in row['Port Name'].lower():
        final_df['Port Name'][index]="manzanillo".title()


    elif "newark" in row['Port Name'].lower():
        final_df['Port Name'][index]="newark".title()


    elif "new york" in row['Port Name'].lower() or "newyork" in row['Port Name'].lower() :
        final_df['Port Name'][index]="new york".title()
        final_df['port_code'][index]="US NYC"


    elif "newcastle" in row['Port Name'].lower():
        final_df['Port Name'][index]="newcastle".title()

    elif "paranagua" in row['Port Name'].lower():
        final_df['Port Name'][index]="paranagua".title()

    elif "philadelphia" in row['Port Name'].lower():
        final_df['Port Name'][index]="philadelphia".title()

    elif "puerto caldera" in row['Port Name'].lower():
        final_df['Port Name'][index]="puerto caldera".title()
        final_df['port_code'][index]="CL PMC"

    elif "puerto cortes" in row['Port Name'].lower():
        final_df['Port Name'][index]="puerto cortes".title()
        final_df['port_code'][index]="HN PCR"

    elif "puerto limon" in row['Port Name'].lower():
        final_df['Port Name'][index]="puerto limon".title()
        final_df['port_code'][index]=""

    elif "san lorenzo" in row['Port Name'].lower():
        final_df['Port Name'][index]="san lorenzo".title()
        final_df['port_code'][index]="HN SLO"

    elif "santo domingo" in row['Port Name'].lower():
        final_df['Port Name'][index]="santo domingo".title()
        final_df['port_code'][index]="DO SDQ"

    elif "santos" in row['Port Name'].lower():
        final_df['Port Name'][index]="santos".title()
        final_df['port_code'][index]="BR SSZ"

    elif "shanghai" in row['Port Name'].lower():
        final_df['Port Name'][index]="shanghai".title()
        final_df['port_code'][index]="CN SHA"


    elif "tacoma" in row['Port Name'].lower():
        final_df['Port Name'][index]="tacoma".title()
        final_df['port_code'][index]="US ACI"


    elif "wilmington" in row['Port Name'].lower():
        final_df['Port Name'][index]="wilmington".title()

    elif "altamira" in row['Port Name'].lower():
        final_df['Port Name'][index]="altamira".title()
        final_df['port_code'][index]="MX ATM"

    elif "aratu" in row['Port Name'].lower():
        final_df['Port Name'][index]="aratu".title()

    elif "zarate" in row['Port Name'].lower():
        final_df['Port Name'][index]="zarate".title()

    elif "altamira" in row['Port Name'].lower():
        final_df['Port Name'][index]="altamira".title()
        final_df['port_code'][index]="MX ATM"

    elif "new westminster" in row['Port Name'].lower():
        final_df['Port Name'][index]="new westminster".title()
        final_df['port_code'][index]="" 

    elif "abu dhabi" in row['Port Name'].lower() or "abu" in row['Port Name'].lower():
        final_df['Port Name'][index]="abu dhabi".title()
        final_df['port_code'][index]=""   

    elif "ad dammam" in row['Port Name'].lower():
        final_df['Port Name'][index]="ad dammam".title()
        final_df['port_code'][index]=""     

    elif "bahrain" in row['Port Name'].lower():
        final_df['Port Name'][index]="bahrain".title()
        final_df['port_code'][index]="BH KBS"


    elif "corpus" in row['Port Name'].lower():
        final_df['Port Name'][index]="corpus".title()
        final_df['port_code'][index]="US CRP"

    elif "eca ent.point usec jxv/buw/svn" in row['Port Name'].lower():
        final_df['Port Name'][index]="eca ent.point usec jxv/buw/svn".title()
        final_df['port_code'][index]=""

    elif "el iskandariya (alexandria)" in row['Port Name'].lower():
        final_df['Port Name'][index]="el iskandariya (alexandria)".title()
        final_df['port_code'][index]=""

    elif "fort de france" in row['Port Name'].lower():
        final_df['Port Name'][index]="fort de france".title()
        final_df['port_code'][index]="MQ Ffinal_df"

    elif "hai phong" in row['Port Name'].lower():
        final_df['Port Name'][index]="hai phong".title()
        final_df['port_code'][index]=""

    elif "ho chi minh" in row['Port Name'].lower():
        final_df['Port Name'][index]="ho chi minh".title()
        final_df['port_code'][index]="VN SGN"

    elif "honolulu" in row['Port Name'].lower():
        final_df['Port Name'][index]="honolulu".title()
        final_df['port_code'][index]="US HNL"

    elif "houston" in row['Port Name'].lower():
        final_df['Port Name'][index]="houston".title()
        final_df['port_code'][index]="US HOU"            

    elif "huangpu" in row['Port Name'].lower():
        final_df['Port Name'][index]="huangpu".title()
        final_df['port_code'][index]=""              

    elif "jakarta" in row['Port Name'].lower():
        final_df['Port Name'][index]="jakarta".title()
        final_df['port_code'][index]="ID TPP"   

    elif "jebel" in row['Port Name'].lower():
        final_df['Port Name'][index]="jebel".title()
        final_df['port_code'][index]="AE JEA"   

    elif "keelung" in row['Port Name'].lower():
        final_df['Port Name'][index]="keelung".title()
        final_df['port_code'][index]="TW KEL"   

    elif "kingston" in row['Port Name'].lower():
        final_df['Port Name'][index]="kingston".title()
        final_df['port_code'][index]="JM KIN"   

    elif "koper" in row['Port Name'].lower():
        final_df['Port Name'][index]="koper".title()
        final_df['port_code'][index]="SI KOP"   

    elif "lehavre" in row['Port Name'].lower().strip() or "le havre" in row['Port Name'].lower():
        final_df['Port Name'][index]="le havre".title()
        final_df['port_code'][index]="FR LEH"   

    elif "lian yun gang" in row['Port Name'].lower():
        final_df['Port Name'][index]="lian yun gang".title()
        final_df['port_code'][index]=""   

    elif "livorno" in row['Port Name'].lower():
        final_df['Port Name'][index]="livorno".title()
        final_df['port_code'][index]="IT LIV"   

    elif "long beach" in row['Port Name'].lower():
        final_df['Port Name'][index]="long beach".title()
        final_df['port_code'][index]="US LGB"   

    elif "mobile" in row['Port Name'].lower():
        final_df['Port Name'][index]="mobile".title()
        final_df['port_code'][index]="US MOB"   

    elif "mumbai" in row['Port Name'].lower():
        final_df['Port Name'][index]="mumbai".title()
        final_df['port_code'][index]="IN BOM"   


    elif "nagoya" in row['Port Name'].lower():
        final_df['Port Name'][index]="nagoya".title()
        final_df['port_code'][index]="JP NGO"   

    elif "port elizabeth" in row['Port Name'].lower():
        final_df['Port Name'][index]="port elizabeth".title()
        final_df['port_code'][index]="ZA PLZ"   

    elif "port everglades" in row['Port Name'].lower():
        final_df['Port Name'][index]="port everglades".title()
        final_df['port_code'][index]="US PEF"   


    elif "port hueneme" in row['Port Name'].lower():
        final_df['Port Name'][index]="port hueneme".title()
        final_df['port_code'][index]=""   

    elif "port kelang" in row['Port Name'].lower() or "port klang" in row['Port Name'].lower():
        final_df['Port Name'][index]="port kelang".title()
        final_df['port_code'][index]="MY PKL"   

    elif "port kembla" in row['Port Name'].lower():
        final_df['Port Name'][index]="port kembla".title()
        final_df['port_code'][index]=""   

    elif "port of spain" in row['Port Name'].lower():
        final_df['Port Name'][index]="port of spain".title()
        final_df['port_code'][index]=""   

    elif "port louis" in row['Port Name'].lower():
        final_df['Port Name'][index]="port louis".title()
        final_df['port_code'][index]="MU PLU"   

    elif "port moresby" in row['Port Name'].lower():
        final_df['Port Name'][index]="port moresby".title()
        final_df['port_code'][index]="PG POM"   

    elif "port reunion" in row['Port Name'].lower():
        final_df['Port Name'][index]="port reunion".title()
        final_df['port_code'][index]="RE PDG"   

    elif "port sudan" in row['Port Name'].lower():
        final_df['Port Name'][index]="port sudan".title()
        final_df['port_code'][index]="SD PZU"   

    elif "port-au-prince" in row['Port Name'].lower():
        final_df['Port Name'][index]="port-au-prince".title()
        final_df['port_code'][index]=""   

    elif "pt elizabeth" in row['Port Name'].lower():
        final_df['Port Name'][index]="pt elizabeth".title()
        final_df['port_code'][index]="ZA PLZ"   

    elif "puerto" in row['Port Name'].lower():
        final_df['Port Name'][index]="puerto".title()
        final_df['port_code'][index]="HN PCR"   

    elif "qingdao" in row['Port Name'].lower():
        final_df['Port Name'][index]="qingdao".title()
        final_df['port_code'][index]="CN TAO"   

    elif ("rio de janeiro" in row['Port Name'].lower()) or ("rio" == row['Port Name'].lower()):
        final_df['Port Name'][index]="rio de janeiro".title()
        final_df['port_code'][index]="BR RIO"   

    elif "rio grande" in row['Port Name'].lower():
        final_df['Port Name'][index]="rio grande".title()
        final_df['port_code'][index]="BR RIG"   

    elif "rio haina" in row['Port Name'].lower():
        final_df['Port Name'][index]="rio haina".title()
        final_df['port_code'][index]="DO HAI"   

    elif ("san antonio" in row['Port Name'].lower()) or ("san" == row['Port Name'].lower()):
        final_df['Port Name'][index]="san antonio".title()
        final_df['port_code'][index]="CL SAI"   

    elif "san diego" in row['Port Name'].lower():
        final_df['Port Name'][index]="san diego".title()
        final_df['port_code'][index]=""   

    elif "san juan" in row['Port Name'].lower():
        final_df['Port Name'][index]="san juan".title()
        final_df['port_code'][index]="NI SJS"  

    elif ("santa" == row['Port Name'].lower()) or ("santa marta" == row['Port Name'].lower()):
        final_df['Port Name'][index]="santa marta".title()
        final_df['port_code'][index]="AR SFN"   

    elif "savannah" in row['Port Name'].lower():
        final_df['Port Name'][index]="savannah".title()
        final_df['port_code'][index]="US SAV"   

    elif "st john's" in row['Port Name'].lower():
        final_df['Port Name'][index]="st john's (ant)".title()
        final_df['port_code'][index]=""   

    elif "st. petersburg" in row['Port Name'].lower():
        final_df['Port Name'][index]="st. petersburg".title()
        final_df['port_code'][index]="RU LED"   

    elif "suape" in row['Port Name'].lower():
        final_df['Port Name'][index]="suape".title()
        final_df['port_code'][index]=""   

    elif "tamatave" in row['Port Name'].lower():
        final_df['Port Name'][index]="tamatave".title()
        final_df['port_code'][index]="MG TOA"   

    elif "Tianjin" in row['Port Name'].lower():
        final_df['Port Name'][index]="Tianjin".title()
        final_df['port_code'][index]="CN TSN"   

    elif "toyohashi" in row['Port Name'].lower():
        final_df['Port Name'][index]="toyohashi".title()
        final_df['port_code'][index]=""   

    elif "veracruz" in row['Port Name'].lower():
        final_df['Port Name'][index]="veracruz".title()
        final_df['port_code'][index]="MX VER"   

    elif "xingang" in row['Port Name'].lower():
        final_df['Port Name'][index]="xingang".title()
        final_df['port_code'][index]=""   
    #add fri 17-jul
    elif ("goteborg" in row['Port Name'].lower()) or ("gothenburg" in row['Port Name'].lower().strip()):
        final_df['Port Name'][index]="Gothenburg".title()
        final_df['port_code'][index]="SE GOT"

    elif ("antwerp" in row['Port Name'].lower().strip()) or ("antwerpen" in row['Port Name'].lower().strip()):
        final_df['Port Name'][index]="Antwerpen".title()
        final_df['port_code'][index]="BE ANR"

    elif ("norfolk" in row['Port Name'].lower().strip()) or ("antwerpen" in row['Port Name'].lower().strip()):
        final_df['Port Name'][index]="Norfolk".title()
        final_df['port_code'][index]="US HNV"
    #end		
    else:
        #print(final_df['Port Name'][index])
        final_df['Port Name'][index]=final_df['Port Name'][index].title()
# you can also use sheet_index [0,1,2..] instead of sheet name.
final_df=final_df.replace(np.nan,'')
# print(port_df1)
df_merged=pd.merge(final_df,port_df1,how="left",on="Port Name")


df_merged['port_code_x'] = df_merged.apply(lambda x: x['port_code_y'] if x['port_code_x']=='' and x['port_code_y']!='' else x['port_code_x'], axis=1)

df_merged=df_merged.rename(columns = {"port_code_x":"port_code"})

df_merged.columns

df_final = df_merged[['Vessel Name', 'Voyage Number', 'Port Name', 'Date of Arrival (ETA)','Date of Departure (ETD)',
    'Carrier', 'port_code']]

df_final["Vessel Capacity (in MT)"]="NA"
df_final["Vessel Ramp Height (in meters)"]="NA"
# if name in ["Baltimore","New York","Halifax","Norfolk"] :
#     df_final["Route Code"]="NA-EU"
# else: 
#     df_final["Route Code"]="EU-NA

df_final["Route Code"] = df_final['Port Name'].apply(lambda x:"NA-EU" if x in ["Baltimore","New York","Halifax","Norfolk"] else "EU-NA")
df_final=df_final[["Carrier","Route Code","Vessel Name","Vessel Capacity (in MT)","Vessel Ramp Height (in meters)","Voyage Number","Port Name","port_code","Date of Arrival (ETA)","Date of Departure (ETD)"]]
df_final.drop_duplicates(inplace=True)
df_final.to_csv('acl.csv',index=False)

print("ACL completed....")

