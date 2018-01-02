#!/usr/bin/env python3
import argparse
from paramiko import SSHClient, AutoAddPolicy

botnet = []


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = SSHClient()
            s.set_missing_host_key_policy(AutoAddPolicy())
            s.connect(self.host, port=22, username=self.user,
                      password=self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        stdin, stdout, stderr = self.session.exec_command(cmd)
        return stdout.read()


def botnet_command(command):
    for client in botnet:
        output = client.send_command(command)
        print('[*] Output from ' + client.host)
        print('[+] ' + output.decode())


def add_client(host, user, password):
    client = Client(host, user, password)
    botnet.append(client)


add_client('127.0.0.1', 'dfadmin', '')
botnet_command('uname -v')
botnet_command('ifconfig')
