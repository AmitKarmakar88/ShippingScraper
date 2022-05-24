import pandas as pd
from datetime import datetime
import csv
import os

import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication

smtp_server = "mail.metaorigins.com"
port = 25  # For starttls
sender_email = "noreply@metaorigins.com"

#-------------------call the python script------------------------------
os.chdir("/var/www/html/Shipping-Scraper/scraper/")

print("Scraping ACL")
os.system("python3 acl_new.py")
print("ACL Scraping complete")


print("Scraping HOG")
os.system("python3 hog.py")
print("HOG Scraping complete")

print("Scraping MOL")
os.system("python3 mol.py")
print("MOL Scraping complete")


print("Scraping LGL")
os.chdir("LGL_complete")
print(os.getcwd())
os.system("sudo bash run_all_py.sh")
print("LGL Scraping complete")

print("Scraping K Line")
os.chdir("./../K_LINE_comoplete")
print(os.getcwd())
os.system("sudo bash run_all_py.sh")
print("K Line Scraping complete")

print("Scraping Glovis")
os.chdir("./../glovis")
print(os.getcwd())
os.system("sudo bash run_all_py.sh")
print("Glovis Scraping complete")

#-------------clean the data and load in final excel--------------------
os.chdir("./../")

print(os.getcwd())

mol_csv = pd.read_csv('mol.csv')
mol_csv["Voyage Number"] = mol_csv.apply(lambda x:x["Voyage Number"].replace(x["Vessel Name"],"").strip(),axis=1)
mol_csv["Route Code"] = mol_csv.apply(lambda x:x["Route Code"].replace("(MOL OPERATED)","").strip(),axis=1)
hog_csv = pd.read_csv('hog.csv')
spcial_char_map = {ord('Ö'):'O'}
hog_csv["Vessel Name"] = hog_csv["Vessel Name"].str.translate(spcial_char_map)
hog_csv["Vessel Name"] = hog_csv["Vessel Name"] .str.replace("HOEGH","")
lgl_csv = pd.read_csv('Complete_LGL.csv')
glovis_csv = pd.read_csv('Glovis.csv')
acl_csv = pd.read_csv('acl.csv')
kline_csv = pd.read_csv('K_LINE_complete.csv')
df=pd.concat([mol_csv, hog_csv, lgl_csv, glovis_csv,acl_csv,kline_csv])
df['']=''
df['Refreshed_Date']=datetime.now()
filename="Competitor_Vessel_schedule.xlsx"
df['Vessel Ramp Height (in meters)']=df['Vessel Ramp Height (in meters)'].apply(lambda h:h.replace(',','.') if isinstance(h,str) else h)

def convert_date_fmt(d):
    if isinstance(d, datetime):
        return datetime.strftime(d,"%Y/%m/%d")
    elif isinstance(d, str):
        try:
            return datetime.strftime(datetime.strptime(d,"%d/%m/%Y"),'%Y/%m/%d')
        except:
            return d
    else:
        return ''
        

df['Date of Arrival (ETA)']=df['Date of Arrival (ETA)'].apply(lambda x:convert_date_fmt(x))
df['Date of Departure (ETD)']=df['Date of Departure (ETD)'].apply(lambda x:convert_date_fmt(x))
df['Refreshed_Date']=df['Refreshed_Date'].apply(lambda x:convert_date_fmt(x))
df.to_excel(filename,index=False)

#---------------------email the final excel---------------------------------------

def send_attachment_mail(rec_email,file_url):
    message = MIMEMultipart('mixed')
    FROM = sender_email
    TO = rec_email
    message['From'] = FROM
    message['To'] = TO
    message['Cc'] = 'akshay@metaorigins.com'
    message['Subject'] = 'Power BI'

    msg_content = 'PFA'
    body = MIMEText(msg_content, 'html')
    message.attach(body)

    attachmentPath = file_url
    try:
        with open(attachmentPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(),_subtype="model/gltf-binary")	
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath) 
            message.attach(p)
    except Exception as e:
        print(str(e))

    msg_full = message.as_string()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  
        server.starttls()
        server.ehlo()
        server.sendmail(FROM ,TO,msg_full )
        server.quit()

    print("email sent out successfully")                                          
    return

send_attachment_mail(['breno.march@walwil.com',
'yasuyuki.sakurai@walwil.com',
'Stephanie.Mazzotta@walwil.com',
'jhseo@walwil.com',
'Rider.Liu@walwil.com',
'akshay@metaorigins.com',
'Per-Aage.Aasness@2wglobal.com',
'Pradeep.Garg@2wglobal.com',
'supp_inv_prod@walwil.com',
'Anjalie.Salunke@2wglobal.com',
'alice.legrand@sinay.fr',
'ahcene.sadi@sinay.fr',
'ww-upload@sinay.fr'],filename)