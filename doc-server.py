#!/usr/bin/python3

import json
import select
import socket
import subprocess as sp

import messenger as msgr

__next_pid = 0

def next_pid():
    global __next_pid

    __next_pid += 1

    return __next_pid

def line2msg(line):
    data = line.split(',')

    msg = dict()
    msg['pid'] = int(data[0])
    msg['rev'] = int(data[1])
    msg['type'] = int(data[2])
    msg['c'] = data[3]
    msg['pos'] = int(data[4])

    return msg

def op_perform(buf, msg):
    typ = msg['type']
    c = msg['c']
    pos = msg['pos']

    if 1 == typ:
        if len(buf) < pos:
            buf.extend([' '] * (pos - len(buf)))
        buf.insert(pos, c)
    elif 2 == typ:
        buf.pop(pos)

    return buf

def main():
    revision = 0
    buf = []

    # start engine
    engine = sp.Popen(['./server'], stdin=sp.PIPE, stdout=sp.PIPE)

    lsk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsk.bind(('', 4444))
    lsk.listen(10)

    sockets = set([lsk])

    while True:
        rlist, _, _ = select.select(sockets, [], [])

        ct = 0

        for rsk in rlist:
            if rsk == lsk:
                conn, addr = lsk.accept()

                msg = dict()
                msg['rev'] = revision
                msg['pid'] = next_pid()

                msgr.safe_send(conn, json.dumps(msg))
                msgr.safe_send(conn, ''.join(buf))

                sockets.add(conn)
            else:
                packet = msgr.safe_recv(rsk)
                if 0 == len(packet):
                    sockets.remove(rsk)
                else:
                    msg = json.loads(packet)
                    engine.stdin.write('{},{},{},{},{}\n'.format(msg['pid'], msg['rev'],
                                                            msg['type'], msg['c'], msg['pos']))
                    ct += 1

        for i in range(ct):
            revision += 1

            data = engine.stdout.readline()
            msg = line2msg(data)
            buf = op_perform(buf, msg)

            for sk in sockets[1:]:
                msgr.safe_send(sk, json.dumps(msg))

if __name__ == '__main__':
    main()
