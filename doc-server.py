#!/usr/bin/python

import json
import socket
import subprocess as sp

def main():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', 3333))
    sk.listen(10)

    while True:
        conn, addr = sk.accept()

        msg = json.loads(conn.recv(2048))

        name = msg['docfn']
        port = msg['port']

        sp.call(['./server', port], stdout=open(name, 'w'))

        conn.close()

if __name__ == '__main__':
    main()
