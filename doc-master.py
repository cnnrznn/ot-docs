#!/usr/bin/python

import json
import socket

import document.py

def initialize():
    sk = socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', 3333))
    sk.listen(10)

    # TODO load IP's of worker nodes

    # TODO load metadata of existing documents

    return sk, workers, dict()

def main_loop(sk, workers, docs):
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

    while True:
        res = dict()
        conn, addr, = sk.accept()

        data = json.load(conn)

        if data['op'] == 'OPEN':
            next_id += 1

            if data['docfn'] not in docs:
                docs[data['docfn']] = Document(data['docfn'])

            ip = docs[data['docfn']].open(next_id)

            res['ip'] = ip
            res['pid'] = next_id
            res['op'] = 'OK'

        else if data['op'] == 'CLOSE':
            docs[data['docfn']].close(data['pid'])

            res['op'] = 'OK'

        json.dump(res, conn)

        conn.close()

if __name__ == '__main__':
    main_loop(initialize())
