import MachineUtils
import json
from Machine import *

#Print in the terminal the intel about a specific machine, on a json-like format.
def manageGetMachinefromHostname() :
    print('Entrez un hostname s\'il-vous-plaît : ')
    hostname = input()
    print(MachineUtils.getMachineFromHostname(hostname))

#Removes a machine from the list of machines in the machines.json file, based on the hostname.
def manageRemoveMachine() :
    print('Entrez le hostname des machines à supprimer s\'il-vous-plaît : ')
    hostname = input()
    MachineUtils.removeMachineFromHostname(hostname)

#If the hostname does not already exist, this method add a new machine to the list of machines in the 
#machines.json file, according to data filed in by the user when asked by the app.
def manageAddMachine():
    print('Entrez le hostname de la machine à ajouter s\'il-vous-plaît : ')
    hostname = input()
    if MachineUtils.checkHostnameExists(hostname) :
        print('Ce hostname est déjà utilisé vous allez être redirigé sur le panneau de contrôle du parc machine')
        return 
    machineParams = MachineUtils.buildMachineParams(hostname)
    print(machineParams)
    machine = Machine(machineParams)
    MachineUtils.addMachine(machine)

#If the hostname already exists, this method allows the user to update the values of the parameters
#set up for this machine in the machines.json file.
def manageUpdateMachine():
    print('Entrez le hostname de la machine à mettre à jour s\'il-vous-plaît : ')
    hostname = input()
    if not MachineUtils.checkHostnameExists(hostname) :
        print('Ce hostname n\'existe pas. Aucune machine n\'a pu être trouvée et mise à jour. Vous allez être redirigé sur le panneau de contrôle du parc machine')
        return
    MachineUtils.updateMachine(hostname)

#General intelligence of the class of the machine side of the app. Allows the user to chose which action
#shall be done and to redirect to the correct management.
def manageMachines() :
    choiceMachines = "start"
    while choiceMachines != "Q":
        print('Voulez-vous : ')
        print('    - consulter la liste des machines du parc (tapez "list")')
        print('    - consulter les informations d\'une machine spécifique (tapez "machine")')
        print('    - supprimer une machine spécifique (tapez "supp")')
        print('    - mettre à jour les informations d\'une machine spécifique (tapez "maj")')
        print('    - ajouter une machine à la liste de machines du parc (tapez "ajouter")')
        print('    - quitter le panneau de contrôle du parc machine (tapez "Q")')
        choiceMachines = input()
        if choiceMachines == "list":
            print(MachineUtils.listMachines())
        elif choiceMachines == "machine":
            manageGetMachinefromHostname()
        elif choiceMachines == "supp":
            manageRemoveMachine()
        elif choiceMachines == "maj":
            manageUpdateMachine()
        elif choiceMachines == "ajouter":
            manageAddMachine()
        elif choiceMachines == "Q":
            print('Retour au panneau d\'accueil.')
            print('########################')
        else:
            print('S\'il vous plaît entrez un choix valide parmi les suivants.')

#General intelligence of the class on the applications' versions side of the app. Allows the user to chose which action
#shall be done and to redirect to the correct management.    
def manageApp():
    print("manageApp")

#This variable allows to loop on the first menu of the app. If set to Q will exit the app. Initial value set to start.
choice = "start"

#Loop corresponding to the first menu of the app.
while choice != "Q":
    print('Voulez-vous : ')
    print('    - travailler sur le parc de machines (tapez "M")')
    print('    - travailler sur les versions d\'applications (tapez "A")')
    print('    - quitter le logiciel (tapez "Q")')
    choice = input()
    if choice == "M":
        manageMachines()
    elif choice == "A":
        manageApp()
    elif choice == "Q":
        print('Fermeture du logiciel.')
        print('########################')
    else:
        print('S\'il vous plaît entrez un choix valide parmi les suivants.')