#!/usr/bin/env python3
import argparse
import nmap


def nmap_scan(tgt_host, tgt_port):
    nmscan = nmap.PortScanner()
    nmscan.scan(tgt_host, tgt_port)
    state = nmscan[tgt_host]['tcp'][int(tgt_port)]['state']
    print("[+] " + tgt_host + " tcp/" + tgt_port + " " + state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='specify target host')
    parser.add_argument('-P', '--port',
                        help='specify target port[s] separated by comma')
    args = parser.parse_args()

    tgt_host = args.host
    tgt_ports = str(args.port).split(',')

    if (tgt_host is None) | (tgt_ports[0] is None):
        parser.print_help()
        exit(0)
    for tgt_port in tgt_ports:
        nmap_scan(tgt_host, tgt_port)


if __name__ == '__main__':
    main()
