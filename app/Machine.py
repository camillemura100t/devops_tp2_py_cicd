class Machine:
    hostname=""
    ip=""
    nbrCpu=0
    ramSize=0
    nbrHdd=0
    sizeHdd=[]
    versionsOs={}

    #The constructor of the class.
    def __init__(self,machine):
        self.__updateAttributes(machine)

    #Updates all attributes of the class that are also defined in the machine object.
    #@param dictionnary machine : a dictionnary with part or all attributes of the Machine class set as keys.
    def __updateAttributes(self,machine):
        self.hostname = machine['hostname']
        self.ip = machine['ip']
        self.nbrCpu = machine['nbrCpu']
        self.ramSize = machine['ramSize']
        self.nbrHdd = machine['nbrHdd']
        self.sizeHdd = self.sizeHdd + machine['sizeHdd']
        self.versionsOs = machine['versionsOs']

    #Sends a json based on keys corresponding to the Machine class attributes and values based on their values in this instance of the class.
    #returns a json like dictionnary with the attributes of the class all usd as keys.  
    def toJson(self):
        res = {}
        res['hostname'] = self.hostname
        res['ip'] = self.ip
        res['nbrCpu'] = self.nbrCpu
        res['ramSize'] = self.ramSize
        res['nbrHdd'] = self.nbrHdd
        res['sizeHdd'] = self.sizeHdd
        res['versionsOs'] = self.versionsOs
        return res

    #Once the class has been instanciated, this methods allows to update large number of attributes at once.
    #@params dictionnary changes a dictionnary with part or all attributes of the Machine class set as keys. 
    # These keys corredpond to the attributes that will be updated in the class.
    def changeMachineInfo(self,changes):
        machineParams = self.toJson()
        for key in changes.keys():
            machineParams[key] = changes[key]
        self.__updateAttributes(machineParams)
        

