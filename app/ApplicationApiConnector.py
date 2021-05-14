from flask import flask, request
import ApplicationUtils

def launchApiConnector():

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

    app.run(host='0.0.0.0')