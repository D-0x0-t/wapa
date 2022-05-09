#!/usr/bin/env python
import time
import os
import argparse
import sys

#Variables
#Arguments for CMD
#scan1 -- commands
scan1_channel = ""
scan1_bssid = ""
scan1_database = ""
scan1_show_database = ""
scan1_verbose = ""
scan1_interval = ""
#scan2 -- commands
scan2_write = ""
scan2_bssid = ""
scan2_essid = ""
scan2_channel = ""

#Argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Select between airodump scan (better for handshake capture) and table scan", choices=["airodump", "table"])
parser.add_argument("interface", help="Interface to use (MUST be set in monitor mode)")
parser.add_argument("-i", "--interval", help="Interval (in seconds) to refresh table (ONLY FOR TABLE MODE)")
parser.add_argument("-c", "--channel", help="Capture on a specific channel")
parser.add_argument("-b", "--bssid", help="Filter by BSSID")
parser.add_argument("-db", "--database", help="Store data in a database (if not used with -s or --show, -db will just store the data without showing any output)", action="store_true")
parser.add_argument("-s", "--show", help="Show the data stored in the database", action="store_true")
parser.add_argument("-e", "--essid", help="Filter by ESSID (only works with 'airodump' mode)")
parser.add_argument("-w", "--write", help="Write captured handshake into directory 'handshake/<filename>'")
parser.add_argument("-v", help="Verbose mode (debug)", action="store_true")
arg = parser.parse_args()
mode = arg.mode
intf = arg.interface

#Mode dependant execution
if mode == "table":
	if arg.interval is None:
		os.system("python wapascan.py --help")
		print("")
		print("[!] System exception:")
		sys.exit("Argument -i must be defined in order to set the refresh interval. Try using -i 0.5")
	else:
		scan1_interval = arg.interval
	if arg.channel is not None:
		scan1_channel = ("-c %s"% arg.channel)
	if arg.bssid is not None:
		scan1_bssid = ("--bssid %s"% arg.bssid)
	if arg.database is True:
		scan1_database = "--database"
	if arg.show is True:
		scan1_show_database = "--show"
	if arg.v is True:
		scan1_verbose = "-v"
	scan1_command = ("python wapascan-scripts/scan1.py %s %s %s %s %s %s %s"% (intf, scan1_interval, scan1_channel, scan1_bssid, scan1_database, scan1_show_database, scan1_verbose))
	os.system(scan1_command)
if mode == "airodump":
	if arg.channel is not None:
		scan2_channel = ("-c %s"% arg.channel)
	if arg.essid is not None:
		scan2_essid = ("--essid %s"% arg.essid)
	if arg.bssid is not None:
		scan2_bssid = ("--bssid %s"% arg.bssid)
	if arg.write is not None:
		scan2_write = ("--write %s"% arg.write)
	scan2_command = ("python wapascan-scripts/scan2.py %s %s %s %s %s"% (intf, scan2_channel, scan2_essid, scan2_bssid, scan2_write))
	os.system(scan2_command)
