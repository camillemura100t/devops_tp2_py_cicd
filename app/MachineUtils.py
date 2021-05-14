import json
from Machine import *

#Utilitary method to manage the creation of the list of sizes that will be added to the sizeHdd key. 
#@param int nbrHdd the number of hdds whose sizes must be filled in. 
#@return list listSizeHdd a list of sizes for each hdd of the machine.
def manageSizeHdd(nbrHdd):
    listSizeHdd = []
    for i in range(nbrHdd):
        print("Entrez la valeur de la dimension du disque dur numéro "+str(i+1)+" : ")
        listSizeHdd.append(input())
    return listSizeHdd

#Utilitary method to manage the creation of the dictionnary of the versions of OS that will be added to the versionsOs
#key.
#@return dictionnary osParams the dictionnary with all the different versions of all the os on the machine.
def manageVersionsOs():
    os = "start"
    osParams = {}
    while not os == "Q":
        print("Entrez le nom de l'OS que vous voulez renseignez, tapez 'Q' si vous voulez quitter ce menu.")
        os = input()
        if not os =="Q":
            versionsList = []
            version = "start"
            while not version == "Q":
                print("Entrez la version de l'OS "+os+" que vous voulez renseignez, tapez 'Q' si vous voulez quitter ce menu.")
                version = input()
                if not version == "Q":
                    versionsList.append(version)
            osParams[os] = versionsList
    return osParams

#Read the machines.json file and retrieve the list of all the machines and their information.
#@return dictionnary data dictionnary that contains the list of machines within the machines key (iso machines.json file).
def listMachines():
    data = {'machines':[]}
    try:
        with open('machines.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print('Il n\'y a pour l\'instant pas de fichier contenant la liste des machines du parc de votre entreprise.')
        print('Commencez par créer ce fichier avant de vouloir lister les machines')
    return data

#Read the machines.json file and retrieve the specific machine specified by hostname, if it exists.
#@param string hostname the hostname of the machine you want to get intel on.
#@return dictionnary data a json like dictionnary with the parameters of the wanted machine filled in.
def getMachineFromHostname(hostname):
    machines = listMachines()['machines']
    data = {}
    for machine in machines:
        if machine['hostname'] == hostname:
            return machine
    return data

#Add a new machine to the list in the machines.json file
#@param Machine machine the Machine object corresponding to the machine you want to add.
def addMachine(machine):
    machineJson = machine.toJson()
    data = {}
    try:
        with open('machines.json') as json_file:
            data = json.load(json_file)
            data['machines'].append(machineJson)
    except FileNotFoundError:
        data['machines'] = [machineJson]
    with open('machines.json','w') as outfile:
        json.dump(data,outfile)

#Removes a machine from the machines.json file based on its hostname, if the hostname exists.
#@param string hostname the hostname of the machine to remove.
def removeMachineFromHostname(hostname):
    try:
        with open('machines.json') as json_file:
            data = json.load(json_file)
            for machine in data['machines']:
                if machine['hostname'] == hostname:
                    data['machines'].remove(machine)
        with open('machines.json','w') as outfile:
            json.dump(data,outfile)
    except FileNotFoundError:
        print('Il n\'y a pour l\'instant pas de fichier contenant la liste des machines du parc de votre entreprise.')
        print('Commencez par créer ce fichier avant de vouloir supprimer des machines')

#Update a machine intel based on its hostname, if the hostname exists in the machines.json file.
#@param string hostname the hostname of the machine you need to update.
def updateMachine(hostname):
    try:
        with open('machines.json') as json_file:
            data = json.load(json_file)
            for machine in data['machines']:
                if machine['hostname'] == hostname:
                    i = data['machines'].index(machine)
                    tmpMachine = Machine(machine)
                    changes = buildMachineChanges(tmpMachine)
                    tmpMachine.changeMachineInfo(changes)
                    machineJson = tmpMachine.toJson()
                    data['machines'].remove(machine)
                    data['machines'].insert(i,machineJson)
    except FileNotFoundError:
        print('Il n\'y a pour l\'instant pas de fichier contenant la liste des machines du parc de votre entreprise.')
        print('Commencez par créer ce fichier avant de vouloir mettre à jour des machines')
    with open('machines.json','w') as outfile:
        json.dump(data,outfile)

#Utilitary method that checks in a hostname corresponds to an existing machine in the machines.json file.
#@param string hostname the hostname to check.
#@return True if the hostname exists, False otherwise.
def checkHostnameExists(hostname):
    try:
        with open('machines.json') as json_file:
            data = json.load(json_file)
            for machine in data['machines']:
                if machine['hostname'] == hostname:
                    return True
    except FileNotFoundError:
        print('Il n\'y a pour l\'instant pas de fichier contenant la liste des machines du parc de votre entreprise.')
        print('Ce hostname ne peut donc pas encore exister. Vous pouvez utiliser n\'importe quel hostname pour créer votre première machine')
    return False

#Creates the dictionnary with keys corresponding to all the attributes in the 
# Machine class, and their corresponding values.
#@param string hostname the hostname of the machine you want to build the parameters for.
#@return dictionnary params the json like dictionnary with all attributes of the Machine class 
# used as keys, and their values.
def buildMachineParams(hostname):
    params = {}
    for key in ["hostname","ip","nbrCpu","ramSize","nbrHdd","sizeHdd","versionsOs"]:
        if key =="hostname":
            params[key] = hostname
        if key in ["ip","nbrCpu","ramSize","nbrHdd"]:
            print("Entrez la valeur que vous voulez affecter au paramètre "+key+" : ")
            params[key] = input()
        elif key == "sizeHdd":
            params['sizeHdd'] = manageSizeHdd(int(params['nbrHdd']))
        elif key == "versionsOs":
            params['versionsOs'] = manageVersionsOs()
    return params

#Creates the dictionnary with keys corresponding to some or all the attributes in the 
# Machine class, and their corresponding values, depending on which key has to be updated.
#@param string hostname the hostname of the machine you want to build the parameters for.
#@return dictionnary params the json like dictionnary with some or all attributes of the Machine class 
# used as keys, and their values.
def buildMachineChanges(machine):
    params = {}
    hddUpdate = False
    for key in ["ip","nbrCpu","ramSize","nbrHdd","sizeHdd","versionsOs"]:
        print("Voulez-vous mettre à jour ce paramètre : "+key+" ? (Y/N) ")
        yes = input() == "Y"
        if yes:
            if key in ["ip","nbrCpu","ramSize","nbrHdd"]:
                print("Entrez la valeur que vous voulez affecter au paramètre "+key+" : ")
                params[key] = input()
                if key == "nbrHdd":
                    hddUpdate = True
                    params['sizeHdd'] = manageSizeHdd(int(params['nbrHdd']))
            elif key == "sizeHdd" and not hddUpdate:
                params['sizeHdd'] = manageSizeHdd(int(machine.nbrHdd))
            elif key == "versionsOs":
                params['versionsOs'] = manageVersionsOs()
    return params




                
