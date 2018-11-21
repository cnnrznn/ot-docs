import json
import socket

class Document:
    def __init__(self, name, port, workers):
        self.name = name
        self.sites = list(workers)
        self.replicas = list(workers)       # TODO change to subset of workers
        self.collabs = set()
        self.ip = ''
        self.port = port

        for r in self.replicas:
            self._activate_replica(r)

        return

    def open(self, pid):
        if pid in self.collabs:
            exit(1)                 # why openning twice?

        if 0 == len(self.collabs):
            # TODO load balance, pick worker to launch on
            self.ip = self.replicas[0]

        self.collabs.add(pid)

        return self.ip, self.port

    def close(self, pid):
        self.collabs.remove(pid)

        if 0 == len(self.collabs):
            self.ip = ''

        return

    def _activate_replica(self, replica):
        """
        Connect to document server at replica and tell
        it to start the server for this document at
        this port.
        """
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((replica, 3333))

        msg = dict()
        msg['op'] = 'ACTIVATE'
        msg['docfn'] = self.name
        msg['port'] = self.port

        sk.send(json.dumps(msg))

        sk.close()

        return

    def checkup(self):
        """
        Perform a checkup by sending heartbeats to all sites.

        Three cases:
            - self.ip fails
            - self.replica[i] fails
            - self.sites[j] fails
        """
        pass
