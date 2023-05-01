import os
import re
import subprocess
import webbrowser

#Created by Fetti.Wop, Augmented data construction using AI.

# Define function to perform nmap scan, here you can switch around flags to fully suit your needs. These are my Default.
def nmap_scan(target_ip):
    print(f"Performing nmap scan on {target_ip}...")
    nmap_command = f"nmap -sV -O -p- --spoof-mac Apple -oN nmap_scan.txt {target_ip}"
    subprocess.run(nmap_command, shell=True)
    print("Scan complete.")

# Define function to prompt user for aggressive scan and perform it if requested. The Idea here is, Discovery on first scan, then, utilizing that data, really hammer the open ports for service fingerprinting.
def aggressive_scan(target_ip):
    open_ports = []
    with open("nmap_scan.txt") as f:
        for line in f:
            match = re.search(r"^\d+/tcp\s+open\s+\S+", line)
            if match:
                port = match.group(0).split("/")[0]
                open_ports.append(port)
    if open_ports:
        print(f"The following ports were found to be open in the initial scan: {', '.join(open_ports)}")
        response = input("Would you like to perform an aggressive scan on these ports? (y/n): ")
        if response.lower() == "y":
            print("Performing aggressive scan...")
            nmap_command = f"sudo nmap -sS -sV -O -p {','.join(open_ports)} --script vuln -oN aggressive_scan.txt {target_ip}"
            subprocess.run(nmap_command, shell=True)
            print("Aggressive scan complete.")
            search_cves("aggressive_scan.txt")
    else:
        print("No open ports found.")

# Define function to search for CVEs in nmap scan output and output links to web browser
def search_cves(scan_file):
    cve_list = []
    with open(scan_file) as f:
        for line in f:
            match = re.search(r"^(CVE-\d{4}-\d{4})", line)
            if match:
                cve_list.append(match.group(1))
    if cve_list:
        print("The following CVEs were found:")
        for cve in cve_list:
            print(cve)
            webbrowser.open(f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve}")
    else:
        print("No CVEs found.")

# Get user input for target IP address
target_ip = input("Welcome to the FettiWop Scanner using NMAP. Enter target IP address: ")

# Perform nmap scan and prompt user for aggressive scan
nmap_scan(target_ip)
aggressive_scan(target_ip)
