#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import crypt


def test_pass(cryptpass):
    salt = cryptpass[0:2]
    with open('dictionary.txt', 'r') as dict_file:
        for word in dict_file.readlines():
            word = word.strip('\n')
            crypt_word = crypt.crypt(word, salt)
            if crypt_word == crypt_pass:
                print('[+] Found Password: ' + word + '\n')
                return
        print('[-] Password Not Found.\n')
        return


if __name__ == '__main__':
    with open('passwords.txt', 'r') as pass_file:
        for line in pass_file.readlines():
            if ':' in line:
                user = line.split(':')[0]
                crypt_pass = line.split(':')[1].strip(' ')
                print('[*] Cracking Password For: ' + user)
                test_pass(crypt_pass)
    