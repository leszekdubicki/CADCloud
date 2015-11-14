#client app to connect to ccloud server app
import requests

class CCloud:
    #class to perform operations on single CADCloud web app (given by base URL)
    def __init__(self, url):
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def get_projects(self):
        #gets list of projects
        uri = '/cad/api/v0.1/projects'
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
            #I'd rather not store all the projects not to consume too much memory
    def get_variables(self, project_id):
        #gets list of variables of one project given by id
        uri = '/cad/api/v0.1/variables/' + str(project_id)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        
    def get_project_by_number(self, project_number):
        #project_number should be a string already but it's converted to str just in case:
        uri = '/cad/api/v0.1/projects_by_num/' + str(project_number)
        r = requests.get(self._url + uri, headers = self._headers)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
    def get_project(self, project_id):
        #gets project by id
        uri = '/cad/api/v0.1/projects/' + str(project_id)
        r = requests.get(self._url + uri, headers = self._headers)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()

class CCStore(CCloud):
    #class storing some values for the projects and list of projects
    def set_projects_list(self):
        #gets list of all projects under given url and stores it in the object
        idsList = []
        numsList = []
