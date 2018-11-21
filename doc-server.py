#!/usr/bin/python

import json
import socket
import subprocess as sp

def main():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', 4444))
    sk.listen(10)

    while True:
        conn, addr = sk.accept()
        msg = json.loads(conn.recv(2048))
        conn.close()

        # TODO check if msg/document is legit

        name = msg['docfn']
        port = msg['port']

        print('Received {}'.format(msg))

        sp.Popen(['./server', str(port)], stdout=open(name, 'w'))

    return

if __name__ == '__main__':
    main()
