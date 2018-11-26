#!/usr/bin/python

import argparse
import json
import socket
import subprocess as sp

import document

ADDR = '35.237.247.180'
PORT = 3333

class DocClient:

    def __init__(self, name):
        msg = dict()
        msg['op'] = 'OPEN'
        msg['docfn'] = name

        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((ADDR, PORT))

        sk.send(json.dumps(msg))
        res = json.loads(sk.recv(2048))

        sk.close()

        self.pid = res['pid']
        self.ip = res['ip']
        self.port = res['port']
        self.name = name

        self.engine = sp.Popen(['./client'], stdin=sp.PIPE, stdout=sp.PIPE)

        return

    def __del__(self):
        # cleanup
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((ADDR, PORT))

        msg = dict()
        msg['op'] = 'CLOSE'
        msg['docfn'] = self.name
        msg['pid'] = self.pid

        sk.send(json.dumps(msg))
        res = json.loads(sk.recv(2048))

        sk.close()

        self.engine.kill()

        return

client = DocClient("a file") # TODO get document name from vim command
