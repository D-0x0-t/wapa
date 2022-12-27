# WAPA
Wireless Access Point Auditor
### What is WAPA?
**WAPA** is a tool designed for wireless pentesters.
It all started as a _FDP_ (final degree project), but now it can be used like any other tool to perform security tests (or just have fun) on wireless networks.

### Installation

WAPA requires the following:

1. Any Linux-based OS (preferably Kali/Parrot)
2. Python3
3. Wireless network adapter that accepts "monitor mode"
4. Free time :D

Step-by-step guide:

    ~ git clone https://github.com/D-0x0-t/wapa
    ~ cd wapa
    # bash setup.sh
   
After this, **wapa** and every single script used on the main program will be added to "/usr/sbin", making WAPA executable from anywhere in the system.

### Usage

The WAPA suite is divided in setup, scan and attack. The combination of those 3 sections is available on the main script (wapa).

#### Main script:

Execute it using:

    # wapa
    # wapa --help
    # wapa -m example
    
You can choose between:

- Scan mode: Capture packets to detect near networks.
- Crack mode: Crack a handshake stored in a file.
- Fuzz mode: Flood beacons to generate a large amount of fake APs.
- DOS mode: Perform a denial of service on an AP.
- EvilTwin mode: Automate the EvilTwin attack process (generate an access point, create a captive portal if needed, redirect the traffic to an output interface (ie. eth0)).
- Example mode: This mode prints two tables with pre-generated commands. Use them as a guide to perform better attacks in the future.

#### Setup script:

**wapamon** is used as an automation for the process of:

1. Stopping NetworkManager and wpa_supplicant services
2. Restarting the selected network adapter in monitor mode
3. Generate a new MAC address

Here are some examples of wapamon usage:

    # wapamon status wlan0
    # wapamon start wlan0
    # wapamon stop wlan0
    # wapamon status services
    
#### Scan script:

**wapascan** has 2 modes, so you can choose the one that fits better to you.

The first one uses airodump-ng to capture the packets. The second one combines Python Pandas, Scapy and SQLite.

    Capture all beacons sent through the 6th channel, show them in a table that updates every 0.25 seconds and store everything in a database:
    # wapascan table wlan0 -c 6 -i 0.25 -db -s -v
    
    Capture all the beacons sent in any channel. Write the output to handshake/capture.*:
    # wapascan airodump wlan0 -w capture
    
    Do the same, but filter for the BSSID = a8:e0:f1:9f:38:2b:
    # wapascan airodump wlan0 -w capture --bssid a8:e0:f1:9f:38:2b
    
#### Attack scripts:

The attack phase doesn't have any specified program. The attack that you want to perform is directly created on a script with the name wapattack_\<attack\>.
  
1. Crack: Crack the handshake stored in a file. There are two ways to perform this attack. The first one uses aircrack-ng, and the second one uses tshark, cap2hccapx and john the ripper. 
2. DOS: Denial of service using deauth packets or generating a flood of CTS/RTS.
3. Fuzzer: Fills the air with fake access points generated with random BSSIDs. You can also decide to use random ESSIDs or to use a wordlist with -f.
4. ET: Automate EvilTwin attack. First, create a new AP with the information specified. Modify iptables and allow packet forwarding if using an exit interface. Generate a captive portal (if requested) and authenticate every client that gives you any info. 

I highly recommend to execute the attacks via the main program. Thats all for me, now its your time to test, try again and try harder. I really hope you enjoy WAPA.
  

**Happy Hacking!!**
  
