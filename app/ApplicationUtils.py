import requests

def listApplications():

    url = "http://192.168.0.101:8086/service/rest/v1/components?repository=apprepo"

    payload={}
    files=[]
    headers = {'Authorization': 'Basic YWRtaW46UzBuQE4zeDk1MS8='}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    return response.text
  
def addApplication(directory,filepath,filenametodisplay):
    
    url = "http://192.168.0.101:8086/service/rest/v1/components?repository=apprepo"

    payload={'raw.directory': directory,
    'raw.asset1.filename': filenametodisplay}
    files= {'raw.asset1' : (open(filepath,'rb'))}
    headers = {'Authorization': 'Basic YWRtaW46UzBuQE4zeDk1MS8='}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    print(filepath)
