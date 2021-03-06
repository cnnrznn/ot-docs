#!/usr/bin/python

import json
import socket

from document import Document

PORT = 3333

def initialize():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', PORT))
    sk.listen(10)

    # load IP's of worker nodes
    workers = []
    with open('.workers.txt', 'r') as inf:
        for line in inf:
            workers.append(line)
            print('loaded worker {}'.format(line))

    # TODO load metadata of existing documents

    return (sk, workers, dict())

def main(sk, workers, docs):
    # protocol:
    #   1. client connects with tcp
    #   2a. client sends OPEN <document>
    #       - server checks if document is already open
    #       - server sends (client ID, server IP) to client
    #   2b. client sends CLOSE <client ID> <document>
    #       - if client ID has handle on document, remove it
    #   4. client closes tcp connection

    heartbeats = [0 for w in workers]
    next_id = 0
    next_port = 10000

    while True:
        res = dict()
        conn, addr, = sk.accept()

        msg = json.loads(conn.recv(2048))

        if msg['op'] == 'OPEN':
            next_id += 1

            if msg['docfn'] not in docs:
                next_port += 1
                docs[msg['docfn']] = Document(msg['docfn'], next_port, workers)

            ip, port = docs[msg['docfn']].open(next_id)

            res['ip'] = ip
            res['port'] = port
            res['pid'] = next_id
            res['op'] = 'OK'

        elif msg['op'] == 'CLOSE':
            docs[msg['docfn']].close(msg['pid'])

            res['op'] = 'OK'

        conn.send(json.dumps(res))

        conn.close()

if __name__ == '__main__':
    main(*initialize())
