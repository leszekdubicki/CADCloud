#client app to connect to ccloud server app
import requests

class CCloud:
    #class to perform operations on single CADCloud web app (given by base URL)
    def __init__(self):
        self._url = None
        self._headers = {'content-type': 'application/json'}
    def set_url(self, url):
        self._url = url
    def setUrl(self, url):
        #copy of set_url method
        self.set_url(url)
    def get_projects(self):
        #gets list of projects
        uri = '/cad/api/v0.1/projects'
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': None}
            #I'd rather not store all the projects not to consume too much memory (see below)
    def getProjectNumbers(self):
        #only a list of project numbers (without id's or anything)
        projects = self.get_projects_list()
        pList = []
        for p in projects['projects']:
            pList.append(p)
        return pList
    def get_projects_list(self):
        #gets list of projects in format {'number':'id'}
        uri = '/cad/api/v0.1/projects_list'
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': None}
    def get_variables(self, project_id):
        #gets list of variables of one project given by id
        uri = '/cad/api/v0.1/variables/' + str(project_id)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'numbers':None, 'strings':None, 'booleans':None}
        
    def get_variable(self, project_id, variable_name):
        #gets one variable
        uri = '/cad/api/v0.1/get_variable/' + str(project_id) + '/' + str(variable_name)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code,variable_name:None}
    def get_project_by_number(self, project_number):
        #project_number should be a string already but it's converted to str just in case:
        uri = '/cad/api/v0.1/projects_by_num/' + str(project_number)
        r = requests.get(self._url + uri, headers = self._headers)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code,'project':None}
    def get_project(self, project_id):
        #gets project by id
        uri = '/cad/api/v0.1/projects/' + str(project_id)
        r = requests.get(self._url + uri, headers = self._headers)
        r = requests.get(self._url + uri, headers = self._headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code,'project':None}

class CCStore(CCloud):
    #class storing some values for the projects and list of projects
    def set_projects_list(self):
        #gets list of all projects under given url and stores it in the object
        idsList = []
        numsList = []
