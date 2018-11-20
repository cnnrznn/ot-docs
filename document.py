class Document:
    def __init__(self, name, port, workers):
        self.name = name
        self.sites = list(workers)
        self.replicas = list(workers)       # TODO change to subset of workers
        self.collabs = set()
        self.ip = ''
        self.port = port

        # TODO spawn servers on replicas on port 'port'

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

    def checkup(self):
        """
        Perform a checkup by sending heartbeats to all sites.

        Three cases:
            - self.ip fails
            - self.replica[i] fails
            - self.sites[j] fails
        """
        pass
