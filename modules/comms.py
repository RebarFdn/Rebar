#coding = 'utf-8'
# Rebar Messaging and email module  comms.py | Ian Moncrieffe | january 28 2023

import smtplib, ssl
import win32com.client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 


copy_email = "miplan@outlook.com"
receiver_email = "rebar.conn@gmail.com"


outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)


# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")


mail.To = receiver_email
mail.Subject = 'Sample Email'
mail.HTMLBody = html
mail.Body = text
#mail.Attachments.Add('c:\\sample.xlsx')
#mail.Attachments.Add('c:\\sample2.xlsx')
mail.CC = copy_email

mail.Send()