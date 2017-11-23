#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile
import argparse
from threading import Thread


def extract_file(zfile, password):
    try:
        zfile.extractall(pwd=password)
        print('[+] Found Password ' + password + '\n')
    except:
        pass


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser("Usage %prog " +\
        "-f <zipfile> -d <dictionary>")
    PARSER.add_argument('-f', dest='zname', type='string',\
        help='specify zip file')
    PARSER.add_argument('-d', dest='dname', type='string',\
        help='specify dictionary file')
    (OPTIONS, ARGS) = PARSER.parse_args()
    if (OPTIONS.zname is None) | (OPTIONS.dname is None):
        print(PARSER.usage)
        exit(0)
    else:
        ZNAME = OPTIONS.zname
        DNAME = OPTIONS.dname

    ZFILE = zipfile.ZipFile(ZNAME)
    with open(DNAME, 'r') as pass_file:
        for line in pass_file.readlines():
            password = line.strip('\n')
            t = Thread(target=extract_file, args=(ZFILE, password))
            t.start()
