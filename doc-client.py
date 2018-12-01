#!/usr/bin/python3

import argparse
import json
import socket
import subprocess as sp

import document
import messenger as msgr

#ADDR = '35.237.247.180'
ADDR = 'localhost'
PORT = 4444

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

        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect((ip, port))

        msg = json.loads(msgr.safe_recv(self.sk))

        self.pid = msg['pid']
        self.revision = msg['rev']
        self.initial_state = msgr.safe_recv(self.sk)

        print(msg)
        print(self.initial_state)

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

    def get_initial_state(self):
        return self.initial_state

    def send_op(self, op):
        self.engine.stdin.write('-1,0,{},{},{}\n'.format(op[0], op[1], op[2]))
        return

    def recv_ops(self):
        ops = []
        messages = []

        while True:
            rlist = [self.sk]
            rlist, _, _ = select.select(rlist, [], [])
            if 0 == len(rlist):
                break
            messages.append(json.loads(msgr.safe_recv(self.sk)))

        for msg in messages:
            self.engine.stdin.write('{},{},{},{},{}\n'.format(msg['pid'], msg['rev'], msg['type'],
                                                                msg['c'], msg['pos']))
        messages.clear()

        while True:
            rlist = [self.engine.stdout]
            rlist, _, _ = select.select(rlist, [], [])
            if 0 == len(rlist):
                break
            data = self.engine.stdout.readline().split[',']
            msg = dict()
            msg['pid'] = int(data[0])
            msg['rev'] = int(data[1])
            msg['type'] = int(data[2])
            msg['c'] = data[3]
            msg['pos'] = int(data[4])

            if -1 == msg['pid']:
                ops.append((msg['type'], msg['c'], msg['pos']))
            else:
                messages.append(msg)

        for msg in messages:
            msgr.safe_send(self.sk, json.dumps(msg))

        return ops

if __name__ == '__main__':
    client = DocClient("myfile", ADDR, PORT)

    # TODO enter some text

    del(client)
