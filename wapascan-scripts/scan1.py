#!/usr/bin/python
from scapy.all import *
from threading import Thread
from threading import Lock
import pandas
import time
import os
import argparse
import sqlite3
import sys

#Variables
do_channel_hop = 0 # 0=execute channelhopping, 1=listen on X channel
filter_bssid = 0
#filter_essid = 0
database_on = 0
show_database = 0
verbose = 0

#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("interface", help="Determine interface to use (must be set in monitor mode)")
parser.add_argument("interval", help="Time to refresh SSIDs", type=float)
parser.add_argument("-c", "--channel", help="Capture on a specific channel", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
parser.add_argument("-b", "--bssid", help="Filter (output, not scan) by BSSID")
parser.add_argument("-db", "--database", help="Store data in a database (by default, it just stores the data, but doesn't show it)", action="store_true")
parser.add_argument("-s", "--show", help="Show the data stored in the database (must be used with --database/-db)", action="store_true")
parser.add_argument("-v", help="Verbosity", action="store_true")
#parser.add_argument("-e", "--essid", help="Filter (output) by ESSID")
args = parser.parse_args()
intf = args.interface
arg_channel = args.channel
arg_bssid = args.bssid
#arg_essid = args.essid
interval = args.interval

#Modify variables if optional arguments were specified
if args.channel is not None:
	do_channel_hop = 1

if args.bssid is not None:
	filter_bssid = 1

#if args.essid is not None:
#	filter_essid = 1

if args.database is True:
	database_on = 1
	exists_directory = os.path.exists("./database")
	if exists_directory == False: #create database directory if not exists
		os.system("mkdir database")
	else:
		os.system("rm database/wapascan.db")
	ap_list = [ ]

if args.show is True:
	show_database = 1

if args.v is True:
	verbose = 1

#Pandas output
networks = pandas.DataFrame(columns=["BSSID", "ESSID", "Signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)

#SQLite3 params
if database_on == 1:
	db_path = "database/wapascan.db"
	con = sqlite3.connect(db_path, check_same_thread=False)
	cursor = con.cursor()
	# check number of tables existing in the database
	#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	#original_stdout = sys.stdout #Saving system standard output
	#with open('database/tables.tmp', 'w') as f:
	#	sys.stdout = f
	#	print(cursor.fetchall())
	#	sys.stdout = original_stdout
	#number_of_tables = os.system("cat database/tables.tmp | tr -d '[]' | wc -w")
	#number_of_tables += 1  # if there are no tables, first one would be <tablename>1, second one will be <tablename>2...
	#os.system("rm database/tables.tmp")
	################################################ DDL ################################################
	#tablename_holder = "SCAN"
	#tablename = tablename_holder+str(number_of_tables)
	if verbose == 1:
		print("[*] Creating table SCAN...")
	cursor.execute("CREATE TABLE SCAN (bssid TEXT PRIMARY KEY NOT NULL, essid TEXT, signal TEXT, channel TEXT, crypto TEXT)")
	if verbose == 1:
		print("[*] Table created successfully")
	lock = Lock()


#Functions
def PacketHandler(pkt):
	if pkt.haslayer(Dot11Beacon):
		bssid = pkt[Dot11].addr2
#		bssid = bssid.upper() # no tiene sentido poner la mac en uppercase
		essid = pkt[Dot11Elt].info.decode()
		if essid != "":
			essid = essid
		else:
			essid = "<null ESSID>"
		try:
			signal = pkt.dBm_AntSignal
		except:
			signal = " - "
		stats = pkt[Dot11Beacon].network_stats()
		channel = stats.get("channel")
		crpt = stats.get("crypto")
		if filter_bssid == 1:
			if bssid == arg_bssid or bssid.upper() == arg_bssid: #added upper condition to avoid conflict with other Dot11 network scanners, which usually print MACs with uppercase.
				networks.loc[bssid] = (essid, signal, channel, crpt)
#		elif filter_essid == 1:
#			if essid == arg_bssid:
#				networks.loc[bssid] = (essid, signal, channel, crpt)
		else:
			networks.loc[bssid] = (essid, signal, channel, crpt)

def PacketHandler_database(pkt):
	if pkt.haslayer(Dot11Beacon):
		bssid = pkt[Dot11].addr2
		if bssid not in ap_list:
			ap_list.append(bssid)
			essid = pkt[Dot11Elt].info.decode()
			if essid != "":
				essid = essid
			else:
				essid = "null ESSID"
			try:
				signal = pkt.dBm_AntSignal
			except:
				signal = "N/A"
			stats = pkt[Dot11Beacon].network_stats()
			channel = stats.get("channel")
			crypto = stats.get("crypto")
			#format_crypto = ("echo %s | tr -d '{}'" % crypto)
			#crypto_parsed = os.system(format_crypto)
			format_crypto = str(crypto)
			crypto_parsed = format_crypto[1:-1]
			# export to database
			data = (bssid, essid, signal, channel, crypto_parsed)
#			print(data)
#			time.sleep(3)
			lock.acquire(True)
			cursor.execute("INSERT INTO SCAN VALUES(?, ?, ?, ?, ?)", data)
			lock.release()
			if verbose == 1 and show_database != 1:
				print("Inserted new value in SCAN with BSSID: %s" % bssid)
			con.commit()

def printer_func():
	while True:
		os.system("clear")
		print(networks)
		time.sleep(interval)

def channel_hop():
	ch = 1
	while True:
		os.system(f"iwconfig {intf} channel {ch}")
		ch = ch % 14 + 1
		time.sleep(interval)

def show_database_function():
	while True:
		command_create_blank_file = ("echo '' > database/show.tmp")
		os.system(command_create_blank_file)
		lock.acquire(True)
		cursor.execute("SELECT * FROM SCAN")
		rows = cursor.fetchall()
		for row in rows:
			f = open("database/show.tmp", "a")
			f.write(str(row))
			f.write("\n")
			f.close()
		lock.release()
		time.sleep(interval)

def show_database_data():
	while True:
		os.system("clear")
		if filter_bssid == 0:
			os.system("cat database/show.tmp")
		else:
			command_arg_bssid = ("cat database/show.tmp | grep %s" % arg_bssid)
			os.system(command_arg_bssid)
		time.sleep(interval)

if database_on == 0:
	printer = Thread(target=printer_func)
	printer.daemon = True
	printer.start()
	if do_channel_hop == 0:
		channel_hopper = Thread(target=channel_hop)
		channel_hopper.daemon = True
		channel_hopper.start()
	else:
		ch = args.channel
		os.system(f"iwconfig {intf} channel {ch}")
	sniff(prn=PacketHandler, iface=intf)
elif database_on == 1:
	# show database?
	if show_database == 1:
		show_db = Thread(target=show_database_function)
		show_db.daemon = True
		show_db.start()
		show_data = Thread(target=show_database_data)
		show_data.daemon = True
		show_data.start()
	if do_channel_hop == 0:
		channel_hopper = Thread(target=channel_hop)
		channel_hopper.daemon = True
		channel_hopper.start()
	else:
		ch = args.channel
		os.system(f"iwconfig {intf} channel {ch}")
	if verbose == 1:
		print("Starting sniffer on interface %s..." % intf)
		time.sleep(2)
	sniff(prn=PacketHandler_database, iface=intf)
