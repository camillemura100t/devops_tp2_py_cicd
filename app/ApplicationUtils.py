import requests

def listApplications():
    curl -u admin:S0n@N3x951/ -X GET 'http://192.168.0.101:8086/service/rest/v1/components?repository=apprepo'

def AddApplication(directory,filepath,filenametodisplay):
    
    url = "http://192.168.0.101:8086/service/rest/v1/components?repository=apprepo"

    payload={'raw.directory': directory,
    'raw.asset1': filepath,
    'raw.asset1.filename': filenametodisplay}
    files=[]
    headers = {'Authorization': 'Basic YWRtaW46UzBuQE4zeDk1MS8='}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)