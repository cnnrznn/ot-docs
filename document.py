class Document:
    def __init__(self, name, workers):
        self.name = name
        self.replicas = ['TODO']
        self.collabs = set()
        self.where = ''

        # TODO create empty document on all replicas

    def open(self, pid):
        if 0 == len(self.collabs):
            # load balance, pick worker to launch on
            self.where = self.replicas[0]

        self.collabs.add(pid)

        return self.where

    def close(self, pid):
        self.collabs.remove(pid)

        if 0 == len(self.collabs):
            self.where = ''

        return
