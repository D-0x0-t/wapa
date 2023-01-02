#!/usr/bin/python3
import subprocess
import signal
import sys
import os
from time import sleep

intf = sys.argv[1]

devnull = open("/dev/null", 'w')

cmd = (f"wapa -m scan -i {intf} -c 1 -db")

process = subprocess.Popen(cmd, stdout=devnull, shell=True)

pid = process.pid

sleep(30)

os.kill(pid, signal.SIGINT)
