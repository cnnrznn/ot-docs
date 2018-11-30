#!/usr/bin/python

import argparse
import json
import socket
import subprocess as sp

import document
import messenger as msgr

ADDR = '35.237.247.180'
PORT = 3333

class DocClient:

    def __init__(self, name, ip, port):
        #msg = dict()
        #msg['op'] = 'OPEN'
        #msg['docfn'] = name
        #msg = json.dumps(msg)

        #sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sk.connect((ADDR, PORT))

        #msgr.safe_send(sk, msg)
        #res = json.loads(msgr.safe_recv(sk))

        #sk.close()

        self.sk = socket.socket.(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect((ip, port))

        res = json.loads(msgr.safe_recv(sk))

        self.pid = res['pid']
        self.revision = res['revision']

        self.engine = sp.Popen(['./client', str(self.pid), str(self.revision)], stdin=sp.PIPE, stdout=sp.PIPE)

        return

    def __del__(self):
        ## cleanup
        #sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sk.connect((ADDR, PORT))

        #msg = dict()
        #msg['op'] = 'CLOSE'
        #msg['docfn'] = self.name
        #msg['pid'] = self.pid

        #sk.send(json.dumps(msg))
        #res = json.loads(sk.recv(2048))

        #sk.close()

        self.engine.kill()
        self.sk.close()

        return

    def __str__(self):
        return 'Not implemented OMEGALUL'

    def send_op():
        pass

    def recv_ops():
        pass

if __name__ == '__main__':
    client = DocClient("myfile", ADDR, PORT)

    # TODO enter some text

    del(client)
