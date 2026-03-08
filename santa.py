import datetime
import json
import random
import os
import sys

def secret_santa(names):
    # Ensure the number of participants is even
  

    while True:
        # Make a copy of the list to shuffle
        shuffled_names = list(names)
        random.shuffle(shuffled_names)

        # Create pairs
        pairs = []
        for i in range(len(names)):
            giver = names[i]
            receiver = shuffled_names[(i + 1) % len(names)]

            # Ensure the giver and receiver are not the same person
            if giver != receiver:
                pairs.append([giver, receiver])
            else:
                # Regenerate pairs if giver and receiver are the same
                break
        else:
            # If the loop completes without a break, all pairs are valid
            return pairs

pairs = []
try:
    emails = open("EMAILS.json")
    emails = json.load(emails)

    currentDate = datetime.datetime.now()

    fileName = (currentDate.strftime("%d") + "-" + currentDate.strftime("%b") + "-" + currentDate.strftime("%H") + "PM" + currentDate.strftime("%M"))
    while fileName+".txt" in os.listdir():
        fileName += "(1)"
        
    f = open(fileName+".txt","w")


    names = [items.strip().title() for items in emails]
    pairs = secret_santa(names)


    f.writelines([items[0]+" is buying "+items[1]+"\n" for items in pairs])
    f.close()

except Exception as ee:
    print(ee)
    sys.exit()

    #send emails here to emails[items[0]]

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 587  # For SSL
smpt_server = "smtp.gmail.com"
email_from = "email"
pwd = "password"
subject = "Secret Santa Time!"
# Create a secure SSL context
context = ssl.create_default_context()
image = open("SSE.png",'rb')
img = MIMEImage(image.read(), name='santa.png',_subtype="png")
img.add_header('Content-Disposition', 'attachment', filename='santa.png')
simple_email_context = ssl.create_default_context()

try:
    TIE_server = smtplib.SMTP(smpt_server,port)
    TIE_server.starttls(context=simple_email_context)
    TIE_server.login(email_from,pwd)
    for items in pairs:
        message = "Hello "+ items[0] +"! In the this year's Secret Santa, you will be buying a gift to "+ items[1]+"!"
       
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = emails[items[0]] ##change this
        msg['Subject'] = subject
        body = f"""
%s

(Please don't spend more than $x on your gifts!)"""%(message)
        msg.attach(MIMEText(body,'plain'))
        msg.attach(img)
        TIE_server.send_message(msg)
        print("EMAIL SENT TO ",emails[items[0]])
except Exception as e:
    print(e)

finally:
    TIE_server.quit()
#debugging
print(pairs)
