#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import binascii
import socket
import threading

screen_lock = threading.Semaphore(value=1)


def my_conn_scan(tgt_host, tgt_port):
    conn_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    error = conn_skt.connect_ex((tgt_host, tgt_port))
    screen_lock.acquire()
    if not error:
        print('[+] %d/tcp open' % tgt_port)
    else:
        print('[-] %d/tcp closed' % tgt_port)

    screen_lock.release()
    conn_skt.close()


def conn_scan(tgt_host, tgt_port):
    try:
        conn_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_skt.connect((tgt_host, tgt_port))
        conn_skt.send(b'ViolentPython3\r\n')
        # results = conn_skt.recv(50)
        screen_lock.acquire()
        print('[+] %d/tcp open' % tgt_port)
        # print('[+] ' + str(results))
    except:
        screen_lock.acquire()
        print('[-] %d/tcp closed' % tgt_port)
    finally:
        screen_lock.release()
        conn_skt.close()


def port_scan(tgt_host, tgt_ports):
    try:
        tgt_ip = socket.gethostbyname(tgt_host)
    except:
        print('[-] Cannot resolve "%s": Unkown host' % tgt_host)
        return

    try:
        tgt_name = socket.gethostbyaddr(tgt_ip)
        print('\n[+] Scan Results for: ' + tgt_name[0])
    except:
        print('\n[+] Scan Results for: ' + tgt_ip)

    socket.setdefaulttimeout(1)
    for tgt_port in tgt_ports:
        t = threading.Thread(target=my_conn_scan, args=(tgt_host, int(tgt_port)))
        t.start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='specify target host')
    parser.add_argument('-P', '--port',
                        help='specify target ports[s] separated by comma')
    args = parser.parse_args()

    tgt_host = args.host
    tgt_ports = str(args.port).split(',')

    if (tgt_host is None) | (tgt_ports[0] is None):
        parser.print_help()
        exit(0)

    port_scan(tgt_host, tgt_ports)


if __name__ == '__main__':
    main()
