def safe_send(sk, buf):
    total = 0
    size = len(buf)

    sk.send(size.to_bytes(8, byteorder='little'))

    while total < size:
        total += sk.send(buf[total:])

    return

def safe_recv(sk):
    buf = ''
    size = int.from_bytes(sk.recv(8), bytorder='little')

    while len(buf) < size:
        buf += sk.recv(size - total)

    return buf
