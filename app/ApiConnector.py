from flask import Flask, request
import ApplicationUtils
import MachineUtils
import Machine
import json

def launchApiConnector():

    def getMachineApi(host):
        MachineUtils.getMachineFromHostname(host)

    def patchMachineApi(hostname,changes):
        try:
            with open('machines.json') as json_file:
                data = json.load(json_file)
                for machine in data['machines']:
                    if machine['hostname'] == hostname:
                        i = data['machines'].index(machine)
                        tmpMachine = Machine(machine)
                        changes = MachineUtils.buildMachineChanges(tmpMachine)
                        tmpMachine.changeMachineInfo(changes)
                        machineJson = tmpMachine.toJson()
                        data['machines'].remove(machine)
                        data['machines'].insert(i,machineJson)
        except FileNotFoundError:
            print('Il n\'y a pour l\'instant pas de fichier contenant la liste des machines du parc de votre entreprise.')
            print('Commencez par créer ce fichier avant de vouloir mettre à jour des machines')
        with open('machines.json','w') as outfile:
            json.dump(data,outfile)
            print('')

    def deleteMachineApi(host):
        MachineUtils.removeMachineFromHostname(host)

    # Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
    app = Flask(__name__)

    @app.route('/apps', methods = ['GET'])
    def getApps():
        ApplicationUtils.listApplications()

    @app.route('/app', methods = ['POST'])
    def addApp():
        directory=request.args.get('directory')
        filepath=request.args.get('filepath')
        filenametodisplay=request.args.get('filenametodisplay')
        ApplicationUtils.addApplication(directory,filepath,filenametodisplay)

    @app.route('/machine/<hostname>', methods = ['GET','PATCH','DELETE'])
    def manageSingleMachineAction(hostname):
        if request.method == 'GET':
            getMachineApi(hostname)
        elif request.method == 'PATCH':
            content = request.json
            machineParams = {}
            if 'hostname' in content:
                machineParams['hostname'] = content['hostname']
            if 'ip' in content:
                machineParams['ip'] = content['ip']
            if 'nbrCpu' in content:
                machineParams['nbrCpu'] = content['nbrCpu']
            if 'ramSize' in content:
                machineParams['ramSize'] = content['ramSize']
            if 'nbrHdd' in content:
                machineParams['nbrHdd'] = content['nbrHdd']
            if 'sizeHdd' in content:
                machineParams['sizehdd'] = content['sizeHdd']
            if 'versionsOs' in content:
                machineParams['versionsOs'] = content['versionsOs']
            patchMachineApi()
        elif request.method == 'DELETE':
            deleteMachineApi()

    @app.route('/machines', methods = ['GET'])
    def manageGetAllMachines():
        MachineUtils.listMachines()
    
    @app.route('/machine', methods = ['POST'])
    def manageAddMachine():
        content = request.json
        if MachineUtils.checkHostnameExists(content['hostname']) :
            print('Ce hostname est déjà utilisé vous allez être redirigé sur le panneau de contrôle du parc machine')
            return 
        for key in ['hostname','ip','nbrCpu','ramSize','nbrHdd','sizeHdd','versionsOs']:
            if key not in content:
                print('Le bpdy de votre requete n\'est pas complet, veuillez renseigner tous les champs.')
                return
        machineParams = {}        
        machineParams['hostname'] = content['hostname']    
        machineParams['ip'] = content['ip']        
        machineParams['nbrCpu'] = content['nbrCpu']        
        machineParams['ramSize'] = content['ramSize']        
        machineParams['nbrHdd'] = content['nbrHdd']        
        machineParams['sizehdd'] = content['sizeHdd']        
        machineParams['versionsOs'] = content['versionsOs']
        machine = Machine(machineParams)
        MachineUtils.addMachine(machine)

    app.run(host='0.0.0.0')