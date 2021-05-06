# EmailAutomationDemo
# 
# EmailAutomationDemo is a sample python script that allows you to send send a filled out template email via outlook. 
# 
# Python packages used -
#	- smtplib
#	- getpass
#	- json
#	- jinja2

#
# Note: Current configuration will not run successfully. After downloading the repo, the following files need to be edited - 
#
# EmailParams.json
#	- Line 7 - Please replace the default value with a functioning email.
#	- Line 15 - This default email address also will need to be replaced.
#
# TenantAccessEmailScript.py
#	- Line 96 - Change the SMTP server to match your current mail server
#		- Example A) mailserver = smtplib.SMTP('smtp.gmail.com',587)
#		- Example B) mailserver = smtplib.SMTP('smtp.office365.com',587)
#
# Additional Configuration Details
#
#	If using gmail as an SMTP server, follow the instructions in the link below to temporarily enable access to your gmail account. 
#
#	https://support.google.com/accounts/answer/6010255#zippy=%2Cif-less-secure-app-access-is-on-for-your-account
#
# For security reasons, it is recommended that you disable this access after using this script.
#
