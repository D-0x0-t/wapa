#!/usr/bin/bash
#
#       		W.A.P.A.
#	Use this script to config WAPA before usage.
#	Executing ./setup.sh is MANDATORY because of
#	the directory configuration. Remember that some
#	programs will also be installed, thanks for
#	using WAPA.
#
tput civis
echo "[+] Preparing to set up W.A.P.A. config"
echo ""
echo "Please do NOT shut down the computer!"
echo ""
apt-get install hostapd -y > /dev/null 2>&1 &
apt-get install macchanger -y > /dev/null 2>&1 &
apt-get install dnsmasq -y > /dev/null 2>&1 &
apt-get install aircrack-ng -y > /dev/null 2>&1 &
apt-get install hashcat-utils -y > /dev/null 2>&1 &
apt-get install tshark -y > /dev/null 2>&1 &
sleep 2
echo "[+] Copying files to /usr/sbin..."
echo ""
p="/usr/sbin"
cp wapamon $p
cp wapascan $p
cp wapascan-scripts/wapascan_airodump $p
cp wapascan-scripts/wapascan_table $p
cp wapattack-scripts/wapattack_crack $p
cp wapattack-scripts/wapattack_dos $p
cp wapattack-scripts/wapattack_et $p
cp wapattack-scripts/wapattack_fuzzer $p
cp --recursive wapattack-scripts/mitm_webserver/ $p/mitm_webserver
cp wapa_animated_sequence $p
cp wapa $p
mkdir /srv/wapa_data
pip install pandas > /dev/null 2>&1 &
pip install scapy > /dev/null 2>&1 &
pip install argparse > /dev/null 2>&1 &
pip install termcolor > /dev/null 2>&1 &
pip install time > /dev/null 2>&1 &
pip install random > /dev/null 2>&1 &
pip install textwrap > /dev/null 2>&1 &
pip install signal > /dev/null 2>&1 &
pip install threading > /dev/null 2>&1 &
pip install sqlite3 > /dev/null 2>&1 &
pip install string > /dev/null 2>&1 &
sleep 2
echo "[+] WAPA is ready for usage..."
echo ""
echo "[-] DISCLAIMER: The Wireless Access Point Auditor is a hacking tool developed as a PoC and targeted for pentesters..."
echo "[-] Whatever you want to do, do it under your own risk!"
tput cnorm
