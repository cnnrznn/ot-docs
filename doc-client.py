#!/usr/bin/python

import argparse
import json
import socket
import subprocess as sp

import document

ADDR = '35.237.247.180'
PORT = 3333

def main(args):
    pid = -1
    ip = ''

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((ADDR, PORT))

    msg = dict()
    msg['op'] = 'OPEN'
    msg['docfn'] = args.name

    sk.send(json.dumps(msg))
    res = json.loads(sk.recv(2048))
    print(msg)
    print(res)
    print()

    sk.close()

    pid = res['pid']
    ip = res['ip']
    port = res['port']

    if 'NOK' == res['op']:
        return 1

    sp.call(['./client', ip, str(port)], stdout=sp.PIPE, stderr=sp.PIPE)

    # cleanup
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((ADDR, PORT))

    msg = dict()
    msg['op'] = 'CLOSE'
    msg['docfn'] = args.name
    msg['pid'] = pid

    sk.send(json.dumps(msg))
    res = json.loads(sk.recv(2048))
    print(msg)
    print(res)
    print()

    sk.close()

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name',
                        help='Name of document to open')

    main(parser.parse_args())
