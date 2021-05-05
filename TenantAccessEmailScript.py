"""
Tenant Access Email Script 
"""


import smtplib
import getpass
import json

from jinja2 import Template
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#load param file
with open('EmailParams.json',) as f: 
    data =json.load(f)

class SenderCredentials:
	def __init__(self, email, password):
		self.email = email
		self.password = password

class Customer:
	def __init__(self, name, url, domain):
		self.name = name
		self.url = url
		self.domain = domain
		

class ClientUser:
	def __init__(self, clientUserFullName, clientUserEmail, clientUserPassword):
		self.clientUserFullName = clientUserFullName
		self.clientUserEmail = clientUserEmail
		self.clientUserPassword = clientUserPassword
	def formatName(self):
		return self.firstName + self.lastName[0].upper()

def configureMessage(senderEmail,customer,user,json_data):
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['From'] = senderEmail
	msg['Subject'] = customer.name + " Tenant Access Details"

	#Initialize body filler variables
	Bundle_html = ""
	Bundle_text = ""
	Product1_html = ""
	Product1_text = ""
	Product2_html = ""
	Product2_text = ""

	#pull in data from param file and fill text_body and html_body based on output
	data = json_data

	#check products purchased and edit template accordingly
	Purchased_Products = data["productsPurchased"]
	if Purchased_Products == [True,True,True]:
		Bundle_text = "Brief introduction and demo of Product Bundle"
		Bundle_html = """<li>Brief introduction and demo of Product Bundle</li>"""
	if Purchased_Products[0] == True:
		Product1_text = "Product 1 Webinar Demo"
		Product1_html = """<li style="margin-top: 4px;">Product 1 Webinar Demo</li>"""
	if Purchased_Products[1] == True:
		Product2_text = "Product 2 Webinar Demo"
		Product2_html = """<li style="margin-top: 4px;">Product 2 Webinar Demo</li>"""
	
	clientusers = data["customerUsers"]

	template = open("TenantAccessEmail.html",).read().replace('\n','')
	text = open("TenantAccessEmail.txt",).read()
	jinja_template = Template(template)
	#print(clientusers)
	replace_html = jinja_template.render(companyName = customer.name, customerURL = customer.url, clientUserFullName = clientusers[0][0], username = clientusers[0][1],password = clientusers[0][2],Bundle = Bundle_html, SIO = Product1_html, SDP = Product2_html)
	
		
	msg['To'] = user.clientUserEmail
	
	#replace variables in text with values based on user input
	replace_text = text.format(clientUserFullName = clientusers[0][0], username = clientusers[0][1],password = clientusers[0][2],companyName = customer.name, customerURL = customer.url, Bundle = Bundle_text, Product1 = Product1_text, Product2 = Product2_text)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(replace_text, 'plain')
	part2 = MIMEText(replace_html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)
	return msg

def sendEmail (credentials,targetEmail,message):
	# Send the message via local SMTP server.
	mailserver = smtplib.SMTP('smtp.office365.com',587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.login(credentials.email, credentials.password)
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	mailserver.sendmail(credentials.email, targetEmail, message)
	#End the mailserver session after all emails have been sent
	mailserver.quit()

#collect common info

customerName = data['companyName']
customerURL = data['customerURL']
customerDomain = data['customerDomain']

customer = Customer(customerName,customerURL,customerDomain)



#pull in product data from param file
Purchased_Products = data["productsPurchased"]

users =[]

for user in data['customerUsers']:
	# Collect user details
	clientUserFullName = user[0]
	clientUserEmail = user[1]
	clientUserPassword = user[2]

	#Create instance of User class and pass in above variabe values
	user = ClientUser(clientUserFullName,clientUserEmail,clientUserPassword)

	users.append(user)

#collect sender info
senderEmail = data['senderEmail']
print(senderEmail)
senderPassword = getpass.getpass(prompt="Sender Password: ", stream=None)

senderCredentials = SenderCredentials(senderEmail,senderPassword)


for user in users:
	

	#pull together message elements into one object
	msg = configureMessage(senderCredentials.email,customer,user,data)
	
	#send the email with all previously compiled values
	sendEmail(senderCredentials,user.clientUserEmail,msg.as_string())