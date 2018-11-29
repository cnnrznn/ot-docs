#from pysyncobj import SyncObj
#from pysyncobj.batteries import ReplList

class ReplDocument:

    def __init__(self, name, ip, port, replicas):
        self.name = name

        replicas -= ip
