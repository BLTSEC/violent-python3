#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import os
import sys


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return


def check_vulns(banner, filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in banner:
                print('[+] Server is vulnerable: ' +\
                    banner.strip('\n'))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('[-] ' + filename +\
                ' does not exist.')
            exit(0)
        if not os.access(filename, os.R_OK):
            print('[-] ' + filename +\
                ' access denied.')
            exit(0)
    else:
        print('[-] Usage: ' + str(sys.argv[0]) +\
            ' <vuln filename>')
        exit(0)

    portlist = [21, 22, 25, 80, 110, 443]
    for x in range(147, 150):
        ip = '192.168.95.' + str(x)
        for port in portlist:
            banner = ret_banner(ip, port)
            if banner:
                print('[+] ' + ip + ' : ' + banner)
                check_vulns(banner, filename)
