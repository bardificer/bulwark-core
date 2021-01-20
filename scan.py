import xml.etree.ElementTree as et #import dependencies
import sqlite3

def scan_file(filename): #translate NMAP scan to python
    items = []
    tree = et.parse(filename)
    root = tree.getroot()

    for n in range(3,len(root)-2): #get ipv4 address, hostname, and open ports
        temp = {}
        try:
            temp['ipv4'] = root[n][1].attrib['addr']
        except:
            temp['ipv4'] = ''

        try:
            temp['hostname'] = root[n][3][0].attrib['name']
        except:
            temp['hostname'] = ''

        try:
            port = ''
            for each in root[n][4]:
                port+=':' + each.attrib['portid'] + '-' + each[1].attrib['name']
            temp['ports'] = port + ':'
        except:
            temp['ports'] = ''

        items.append(temp)

    return items

def testscan(filename): #tests reading file
    print(scan_file(filename))