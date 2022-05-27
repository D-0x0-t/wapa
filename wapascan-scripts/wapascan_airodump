#!/usr/bin/env python
import os
import time
import argparse

#Variables
do_write = 0
do_bssid_filter = 0
do_essid_filter = 0
do_channel_filter = 0

#Variables for cmd
channel_argument = ""
bssid_argument = ""
essid_argument = ""
write_argument = ""

#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("interface", help="Determine interface to use (must be set in monitor mode)")
parser.add_argument("-c", "--channel", help="Airodump-ng CHANNEL filtering")
parser.add_argument("-b", "--bssid", help="Airodump-ng BSSID filtering")
parser.add_argument("-e", "--essid", help="Airodump-ng ESSID filtering")
parser.add_argument("-w", "--write", help="Write handshake captured into directory 'handshake/<filename>'")
args = parser.parse_args()
intf = args.interface

#Var manipulation
if args.channel is not None:
	do_channel_filter = 1
	channel_argument = ("-c %s"% args.channel)
if args.bssid is not None:
	do_bssid_filter = 1
	bssid_argument = ("--bssid %s"% args.bssid)
if args.essid is not None:
	do_essid_filter = 1
	essid_argument = ("--essid %s"% args.essid)
if args.write is not None:
	do_write = 1
	#Checkdir
	exists_dir = os.path.isdir("./handshake")
	if exists_dir is True:
		write_argument = ("--write handshake/%s"% args.write)
	else:
		os.system("mkdir handshake")
		write_argument = ("--write handshake/%s"% args.write)

sh_cmd = ("airodump-ng %s %s %s %s %s"% (intf, channel_argument, bssid_argument, essid_argument, write_argument))
os.system(sh_cmd)
