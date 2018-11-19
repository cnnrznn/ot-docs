#!/usr/bin/python

import argparse
import json
import socket

import document

PORT = 4444

def main(args):
    pid = -1

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(('35.229.114.130', PORT))

    msg = dict()
    msg['op'] = 'OPEN'
    msg['docfn'] = args.name

    sk.send(json.dumps(msg))
    res = json.loads(sk.recv(2048))
    print(res)

    sk.close()

    # TODO if success, spawn ot client and wait for death
    # TODO if failure, handle

    # cleanup
    sk.connect(('35.229.114.130', PORT))

    msg = dict()
    msg['op'] = 'CLOSE'
    msg['docfn'] = args.name
    msg['pid'] = pid

    sk.send(json.dumps(msg))
    res = json.load(sk.recv(2048))
    print(res)

    sk.close()

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name',
                        help='Name of document to open')

    main(parser.parse_args())
