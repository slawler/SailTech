#! /home/pi/python_path

import os

def WiFi_On():
	print('Turning on WiFi')
	cmd = 'ifconfig wlan0 on'
	os.system(cmd)
	print('Wireless Up and Running')


def WiFi_Off():
	print('Turning off WiFi')
	cmd = 'ifconfig wlan0 down'
	os.system(cmd)
	print('Wireless Down')


