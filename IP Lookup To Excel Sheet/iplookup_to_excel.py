# Import Libraries
from termcolor import colored # needed for colored print
import socket
import requests
import xlwt
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Author Zach
# 12/04/2018

''' 
This script will take a list of domains from a txt file, and lookup there ip. It will then add these to an excel file
'''
# Variables needed at start of program that will be used during runtime 
manual_recheck_list = []


# Info about program --> Display to the user
print colored (30 * "-", 'cyan')
print colored("\nIP To Excel File", 'cyan',  attrs=['bold'])
print colored (30 * "-", 'cyan')
print colored("Author: Zach Fleming", 'yellow')
print colored("Date: 12/04/18", 'green')
print colored("\nDescription: This script will take a list of domains from a txt file, and lookup there ip. It will then add these to an excel file\n",'cyan')
print colored("Output folder should be: /results.xls\n",'cyan')

# Get the file with domain names from user
filename = raw_input("Please Enter Path To File Containing IP's [Might be easier to drag and drop] ")

# Create Excel File
print colored("Creating Excel Sheet... [OK]",'cyan')
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 0, "Domain") # create header for first column
sheet1.write(0, 1, "IP") # Create Header For Second Column

# Open File Containing The Domains
try:
	with open(eval(filename), 'r') as f:
		ip_list = f.readlines()
except:
	try:
		with open(filename, 'r') as f:
			ip_list = f.readlines()
	except Exception as e:
		print e
	
i = 1
# While loop to iterate through the client list and test is it vulnerable to the beast attack
while i<len(ip_list):
	try:
		client = ip_list[i]	# i is used to iterate through the list of clients 
		client = client.strip() # strip whitespace
		r = requests.get(client, allow_redirects=True,stream=True,verify=False)
		
		# monkey patch
		try:
			client_ip = r.raw._connection.sock.getpeername()[0]
		except Exception as e:
			try:
				client_ip = r.raw._connection.sock.socket.getpeername()[0]
			except Exception as e:
				print e

		print colored ("Adding " + client + " : " + client_ip + " to excel sheet",'yellow')
		sheet1.write(i,0,client)
		sheet1.write(i,1,client_ip)
		i+=1
	except Exception as e:
		print e
		print colored("[!!] Error Processing " + client + " --> Adding to list for manual inspection later", 'red',attrs=['bold'])
		manual_recheck_list.append(client)
		i+=1
	
book.save("results.xls")
print colored("Output Written to /root/results.xls",'yellow')

if len(manual_recheck_list) !=0:
	print colored("These Domains Need To Be Manually Rechecked", 'red',attrs=['bold'])
	for element in manual_recheck_list:
		print element
	 
	
	
