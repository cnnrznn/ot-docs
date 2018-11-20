#!/usr/bin/python

import socket

def main():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', 3333))
    sk.listen(10)

    while True:
        conn, addr = sk.accept()

        conn.close()

if __name__ == '__main__':
    main()
