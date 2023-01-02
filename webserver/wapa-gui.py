#!/usr/bin/python3
# -.- coding: utf-8 -.-
import os
import sys
import re
from termcolor import colored
from random import randint
from time import sleep
import signal

#####################################################################

sys.tracebacklimit=0

def handler(signum, frame):
	os.system("tput cnorm")
	print("")
	print("")
	print("")
	msg = "[!] Ctrl-C pressed, exitting..."
	print(msg, end="")
	os.system("killall php > /dev/null 2>&1 &")
	exit(0)

#####################################################################

os.system("tput civis")
random_title=randint(1,2)
colores = ["red", "green", "yellow", "blue", "cyan", "magenta", "yellow", "white"]
random_color_title=randint(0,7)
titulo1="""
 __     __     ______     ______   ______
/\ \  _ \ \   /\  __ \   /\  == \ /\  __ \ 
\ \ \/ ".\ \  \ \  __ \  \ \  _-/ \ \  __ \ 
 \ \__/".~\_\  \ \_\ \_\  \ \_\    \ \_\ \_\ 
  \/_/   \/_/   \/_/\/_/   \/_/     \/_/\/_/

"""
titulo2="""
███       ███╗  █████████╗  ████████╗  █████████╗
███  ▄▄▄  ███║  ███   ███║  ███  ███║  ███   ███║
███  ███  ███║  █████████║  ████████║  █████████║
███▄▄███▄▄███║  ███╔══███║  ███╔════╝  ███╔══███║
█████████████║  ███║  ███║  ███║       ███║  ███║
╚════════════╝  ╚══╝  ╚══╝  ╚══╝       ╚══╝  ╚══╝
"""
if random_title == 1:
	print(colored(titulo1,colores[random_color_title]))
else:
	print(colored(titulo2,colores[random_color_title]))

#####################################################################

path = "/var/www/wapa"

isdir = os.path.isdir(path)

signal.signal(signal.SIGINT, handler)

if isdir is True:
    len_args = len(sys.argv)
    if len_args == 2:
        ip_arg = sys.argv[1]
        regex_ip = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
        match = regex_ip.search(ip_arg)
        if match is None:
            print("")
            print(colored("[!] Please, introduce a valid IP address", "red"))
            os.system("tput cnorm")
            sys.exit(1)
        else:
            ip = match.group(0)
    elif len_args == 1:
        ip = "127.0.0.1"
    else:
        print("")
        print(colored("[!] Usage is: wapa-gui ip_address or simply wapa-gui for using localhost", "red"))
        print(colored("Check the command syntax and try again!", "red"))
        os.system("tput cnorm")
        sys.exit(1)
else:
    print("")
    print(colored("[!] Please, execute setup.py or manually move web files to '/var/www/wapa'", "red"))
    os.system("tput cnorm")
    sys.exit(1)


#####################################################################

def webserver():

    os.system(f"php -S {ip}:31337 -t {path} > /dev/null 2>&1 &")

#####################################################################


print("""
       ╭────────────────────────────╮
       │      WAPA Browser GUI      │
       ╰────────────────────────────╯

""")
print("[+] Generating web server on "+ip+":31337")
print("")
print("Open an HTML browser on the remote host and paste this URL in it:")
print("")
if ip == "127.0.0.1":
    print("    http://localhost:31337")
    print("             or")
    print("    http://127.0.0.1:31337")
else:
    print("    http://"+ip+":31337")
print("")
print("Keep this process running and use <ctrl-c> to exit")

webserver()
while True:
    sleep(1000)
