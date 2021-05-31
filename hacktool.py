import random
import time
import os
from tqdm import tqdm
import random

RED   = "\033[1;31m" 

def loading():
	os.system('cls')
	for index in tqdm(range(100), desc = "configuring the attack..."):
		time.sleep(0.09)

	os.system('cls')
	for index in tqdm(range(50), desc = "extracting libraries..."):
		time.sleep(0.1)

	os.system('cls')
	for index in tqdm(range(100), desc = "starting attack..."):
		time.sleep(0.2)

	pss = random.randint(11111111, 9999999999)
	for i in range(11111111, pss):
		print(RED, i)

	print("the password is:", pss)
	input("press any key to exit...")

def end():
	os.system('cls')
	print("okk!! bye...")
	exit()


def menu():
	os.system('cls')
	input("enter ip address:")
	os.system('cls')
	print("starting the hunt...")
	time.sleep(2)
	os.system('cls')

	loading()
	end()

menu()
