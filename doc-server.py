#!/usr/bin/python3

import json
import select
import socket
import subprocess as sp
import multiprocess as mp

from repldoc import ReplDocument

def safe_send(sk, buf):
    total = 0
    size = len(buf)

    while total < size:
        total += sk.send(buf[total:])

    return

def safe_recv(sk, size):
    buf = ''

    while len(buf) < size:
        buf += sk.recv(size - len(buf))

    return

def replica(name, ip, port, replicas):
    rdoc = ReplDocument(name, ip, port, replicas)

    # protocol
    lsk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsk.bind(('', port))
    lsk.listen(10)

    rlist = [lsk]

    while True:
        rlist, _, _ = select.select(rlist, [], [])
        ops = set()

        for rsk in rlist:
            if lsk == rsk:
                #   1. connect to clients
                conn, addr = lsk.accept()
                rlist.append(conn)

                # send revision, document state
                data = dict()
                data = rdoc.get_state()
                buf = json.dumps(data)

                conn.send(len(buf).to_bytes(8, byteorder='little'))
                safe_send(conn, buf)
            else:
                #   2. receive operations from clients
                size = int.from_bytes(rsk.recv(8), byteorder='little')
                op = json.loads(safe_recv(sk, size))
                ops.add(op)

        # broadcast results
        newOps = rdoc.process_ops(ops)
        for op in newOps:
            buf = json.dumps(op)
            for sk in rlist[1:]:
                sk.send(len(buf).to_bytes(8, byteorder='little'))
                safe_send(sk, buf)

    return


def main():
    servers = dict()    # docfn -> Process mapping

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('', 4444))
    sk.listen(10)

    while True:
        conn, addr = sk.accept()
        msg = json.loads(conn.recv(1024))
        conn.close()

        # TODO check if msg/document is legit

        name = msg['docfn']
        ip = msg['ip']
        port = msg['port']
        replicas = msg['reps']

        print('Received {}'.format(msg))

        if name in servers:
            print('Already running that document server')
            continue

        servers[name] = mp.Process(target=replica, args=(name, ip, port, replicas))
        servers[name].start()

    return

if __name__ == '__main__':
    main()
