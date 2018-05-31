# Import Libraries
from termcolor import colored # needed for colored print
import socket
import xlwt
import whois


# Author Zach
# 12/04/2018

''' 
This script will take a list of domains from a txt file, and lookup there ip. It will then add these to an excel file
'''
# Variables needed at start of program that will be used during runtime 
manual_recheck_list = []


# Info about program --> Display to the user
print colored (30 * "-", 'cyan')
print colored("\nDomain Lookup To Excel File", 'cyan',  attrs=['bold'])
print colored (30 * "-", 'cyan')
print colored("Author: Zach Fleming", 'yellow')
print colored("Date: 12/04/18", 'green')
print colored("\nDescription: This script will take a list of IP's from a txt file, and lookup there Domain name. It will then add these to an excel file\n",'cyan')
print colored("Output folder should be: /results.xls\n",'cyan')

# Get the file with domain names from user
filename = raw_input("Please Enter Path To File Containing IP's [Might be easier to drag and drop] ")

# Create Excel File
print colored("Creating Excel Sheet... [OK]",'cyan')
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
sheet1.write(0, 0, "IP") # create header for first column
sheet1.write(0, 1, "Domain") # Create Header For Second Column
sheet1.write(0, 2, "Organization") # Create Header For Second Column

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
		client = ip_list[i-1]	# i is used to iterate through the list of clients 
		client = client.strip() # strip whitespace
		
		try:
			client_ip = socket.gethostbyaddr(client)[0]

		except Exception as e:
			print e
			print colored("[!!] Error Processing " + client + " --> Adding to list for manual inspection later\n", 'red',attrs=['bold'])
			manual_recheck_list.append(client)
			i+=1
			
		else:
			organization = client_ip.split(".",1)[1]
			organization = whois.whois(organization)

			if organization.org is None:
				organization = organization.name_servers[0]
				organization = organization.split(".",1)[1]
			else:
				organization = str(organization.org)

			print colored ("Adding to excel sheet:\nIP Address: " + client + "\nDomain Name: " + client_ip + "\nOrganization: "  + organization + "\n",'yellow')
			sheet1.write(i,0,client)
			sheet1.write(i,1,client_ip)
			sheet1.write(i,2,organization)
			i+=1
			
	except Exception as e:
		print e
		print colored("[!!] Error Processing " + client + " --> Adding to list for manual inspection later\n", 'red',attrs=['bold'])
		manual_recheck_list.append(client)
		i+=1
	
book.save("results.xls")
print colored("Output Written to /root/results.xls",'yellow')

if len(manual_recheck_list) !=0:
	print colored("These Domains Need To Be Manually Rechecked", 'red',attrs=['bold'])
	for element in manual_recheck_list:
		print element
	 
	
	
