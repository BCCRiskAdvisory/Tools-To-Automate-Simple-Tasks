# This script checks whether a port is open on localhost

# Import Libraries
from termcolor import colored # needed for colored print
import socket
import sys
import traceback
import os
import subprocess
import threading
import time
import schedule

# Gloabal used to pass between timer and list all
global j
j = 0


class Port_Checker():
	
	# Inititialize class
	def __init__(self,choice):
		self.choice = choice 
		
		if self.choice == "1":
			self.check_single_port()
			
		elif self.choice == "2":
			self.list_all()
			
		else:
			print colored("! Error Something Unexpected Occured " + str(e),'red',attrs=['bold'])
			print traceback.print_exc()
	
	# This function will check ig the chosen port is open or closed and if a service is listening on it or not 
	def check_single_port(self):
		try:
			os.system('cls' if os.name == 'nt' else 'clear') # Clear Screen
			
			# Ask the user for the target port
			while True:
				try:
					print colored("Please Enter Target Port Number",'cyan')
					target_port = raw_input("Port: ") # get url from the user
					target_port = int(target_port) # convert string to int 
					
					# Check if port is in range
					if (target_port < 0) or (target_port > 65535):
						os.system('cls' if os.name == 'nt' else 'clear') # Clear Screen
						print colored("! Invalid Option. Please Select Either Option 1 or Option 2",'red',attrs=['bold'])
						
					else:
						break
				
				
				except Exception as e:
					os.system('cls' if os.name == 'nt' else 'clear') # Clear Screen
					print colored("! Invalid Port Number. Please Enter Valid Port Number: (0-65535)",'red',attrs=['bold'])
					
				
			#Check If port is open and listening
			result = subprocess.check_output(["netstat -tulpn | grep :" + repr(target_port)],shell=True)
			port = subprocess.check_output(["netstat -tulpn | grep :" + repr(target_port) + " | awk '{ print $4}'"],shell=True)
			
			# Check if exact match -- Grep doesnt always do this it will match anything partial
			if int(port.rsplit(":",1)[1]) == target_port:
				if "LISTEN" in result:
					# Get other Variables
					protocol = subprocess.check_output(["netstat -tulpn | grep " + repr(target_port) + " | awk '{ print $NF}'"],shell=True)
					protocol = protocol.strip()
					print colored ("Status: Open",'green',attrs=['bold'])
					print colored("Protocol: " + str(protocol.split("/")[1]),'green',attrs=['bold'])
					print colored("Process ID: " + str(protocol.split("/")[0]), 'green',attrs=['bold'])
					
				else: 
					print colored ("Port: " + repr(target_port) + " is closed\n",'red',attrs=['bold'])

			else:
				print colored ("Port: " + repr(target_port) + " is closed\n",'red',attrs=['bold'])
				
		except Exception as e:
			if "zero" in str(e):
				print colored ("Port: " + repr(target_port) + " is closed\n",'red',attrs=['bold'])
			else:
				print colored("! Error Something Unexpected Occured " + str(e),'red',attrs=['bold'])
				print traceback.print_exc()
			
	# This function will check all ports to see if open or closed and if a service is listening on it or not 
	def list_all(self):
		global j
		open_ports = {}
		closed_ports = {}
		try:
			os.system('cls' if os.name == 'nt' else 'clear') # Clear Screen
			
			print colored("[*] Checking The Status & Services Of All Ports [*]",'cyan',attrs=['bold'])
			# While loop to iterate over every port
			i = 0
			
			schedule.every(30).seconds.do(self.time_remaining)
			while i < 65535:
				try:
					schedule.run_pending()
					j = i
					#Check If port is open and listening
					result = subprocess.check_output(["netstat -tulpn | grep :" + repr(i)],shell=True)
					port = subprocess.check_output(["netstat -tulpn | grep :" + repr(i) + " | awk '{ print $4}'"],shell=True)
					
					# Check if exact match -- Grep doesnt always do this it will match anything partial
					if int(port.rsplit(":",1)[1]) == i:
						
						if "LISTEN" in result:
							# Get other Variables
							protocol = subprocess.check_output(["netstat -tulpn | grep :" + repr(i) + " | awk '{ print $NF}'"],shell=True)
							protocol = protocol.strip()
							
							status = "Open"
							process_id = str(protocol.split("/")[0])
							protocol = str(protocol.split("/")[1])
							
							# Add to Dictionary
							open_ports[i] = [status,protocol,process_id]
						
					else:
						closed_ports[i] = "Closed" # Add To Dictionary
						
					# Increment I --> Go to next port number
					i+=1
					
					
					
				except Exception as e:
					if "zero" in str(e):
						closed_ports[i] = "Closed"
						i+=1
					elif "list index out of range" in str(e):
						closed_ports[i] = "Closed"
						i+=1
					else:
						print e
						
		except KeyboardInterrupt:
			print colored("Please Press Contol Z to Exit Program")
			pass
				
		except Exception as e:
			print colored("! Error Something Unexpected Occured " + str(e),'red',attrs=['bold'])
			print traceback.print_exc()
			
			
			
		# Print THe Results
		print colored("\n" + 70 * '-','blue')
		print colored('		RESULTS','cyan',attrs=['bold'])
		print colored(70 * '-','blue')
		
		# Print All Closed Ports
		print colored("\nClosed Ports;",'yellow',attrs=['bold'])
		for key, value in closed_ports.iteritems():
			print colored ("Port: " + repr(key), 'red',attrs=['bold']),
			print colored (" Status: " + value, 'red',attrs=['bold'])
				
		# Print All Open Ports
		print colored("Open Ports;",'yellow',attrs=['bold'])
		for key, value in open_ports.iteritems():
			print colored ("Port: " + repr(key), 'green',attrs=['bold'])
			print colored ("Status: " + value[0], 'green',attrs=['bold'])
			print colored ("Protocol: " + value[1], 'green',attrs=['bold'])
			print colored ("Process ID: " + value[2], 'green',attrs=['bold'])

			
	# This function will update user on time left 
	def time_remaining(self):
		global j
		remaining = 65535 - j
		print colored("\nCurrently Tested " + repr(j) + " Out Of 65535 [*]",'yellow', attrs = ['bold'])
		print colored(repr(remaining) + " To Be Tested",'yellow',attrs=['bold'])
		
# Main Function
def main():
	
	# Display tool info to the user
	print colored(30 * "-", 'cyan')
	print colored("\nOpen Port Checker", 'cyan',  attrs=['bold'])
	print colored(30 * "-", 'cyan')
	print colored("Author: Zach Fleming", 'yellow')
	print colored("Date: 20/04/18", 'green')
	print colored("\nDescription: Check For Open Ports & Services Running On Those Ports ",'cyan')

	# While loop to ask user to select which option with basic error sanitization
	while True:
		
		# Display Options To The User
		print colored("\nPlease Select One of The Following Options ",'cyan',attrs=['bold'])
		print colored("  1. Check Single Port",'yellow')
		print colored("  2. List All Open & Closed Ports",'yellow')
		print colored("  3. Exit Program",'yellow')
	
	
		choice = raw_input("\nOption 1, Option 2, or Option 3 ")
		
		# If user only wishes to test for one url
		if choice == "1":
			Port_Checker(choice)
		
		# If User wishes to scan a text file conataining a list of urls
		elif choice == "2":
			Port_Checker(choice)
			
		# If User wishes to scan a text file conataining a list of urls
		elif choice == "3":
			exit()
				
		else:
			os.system('cls' if os.name == 'nt' else 'clear') # Clear Screen
			print colored("! Invalid Option. Please Select Either Option 1, Option 2 or Option 3",'red',attrs=['bold'])
			
	
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted'
		sys.exit(0)
