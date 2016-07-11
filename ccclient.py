#ccclient.py - client app to connect to ccloud server app
#@author:    Leszek Dubicki
#studentID:  x14125439
#email:  leszek.dubicki@ student.ncirl.ie
#@date: 08/12/2015
import requests
import json

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
    def getUrl(self):
        return self._url
    def checkUrl(self):
        #checks if there is something under given url, if not then return False
        if self._url == None or self._url == "None":
            return False
        else:
            #give it a chance:
            try:
                r = requests.get(self._url, headers = self._headers)
                if (r.status_code == 200) and ('cadcloud' in r.json()) and (r.json()['cadcloud'] == 'up'):
                    return True
                else:
                    return False
            except:
                return False

    def get_projects(self):
        #gets list of projects
        uri = '/cad/api/v0.1/projects'
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            #return custom status code
            return {'status_code':1404, 'projects': []}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': []}
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
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            #return custom status code
            return {'status_code':1404, 'projects': []}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'projects': []}
    def get_variables(self, project_id):
        #gets list of variables of one project given by id
        uri = '/cad/api/v0.1/variables/' + str(project_id)
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            #return custom status code
            return {'status_code':1404, 'numbers':[], 'strings':[], 'booleans':[]}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, 'numbers':[], 'strings':[], 'booleans':[]}

    def get_variable(self, project_id, variable_name):
        #gets one variable
        uri = '/cad/api/v0.1/get_variable/' + str(project_id) + '/' + str(variable_name)
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            return {'status_code':1404, variable_name:""}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code, variable_name:""}

    def set_variable(self, project_id, variable_data):
        #sends variable data to the server
        #print variable_data
        if (not 'name' in variable_data):
            return {'status_code':1405, 'variable':None}
        else:
            variable_name = variable_data['name']
        uri = '/cad/api/v0.1/variables/edit/' + str(project_id) + '/' + str(variable_name)
        if self.checkUrl() == True:
            r = requests.put(self._url + uri, headers = self._headers, data=json.dumps({'variable':variable_data}))
        else:
            return {'status_code':1404, 'variable':None}
        if (r.status_code >= 200) and (r.status_code < 300):
            print r.content
            result = r.json()
            result['status_code'] = r.status_code
            return result
        else:
            print r.content
            return {'status_code':r.status_code,'variable':None}
    def set_variable_by_id(self, project_id, variable_data):
        #sends variable data to the server
        if (not 'id' in variable_data) or (not 'type' in variable_data):
            return {'status_code':1405, 'variable':None}
        else:
            variable_id = variable_data['id']
            variable_type = variable_data['type']
        uri = '/cad/api/v0.1/variables/edit/' + str(project_id) + '/' + str(variable_type) + '/' + str(variable_id)  #'<int:project_id>/<string:variable_type>/<int:variable_id>'
        if self.checkUrl() == True:
            r = requests.put(self._url + uri, headers = self._headers, data=json.dumps({'variable':variable_data}))
        else:
            return {'status_code':1404, 'variable':None}
        if (r.status_code >= 200) and (r.status_code < 300):
            print r.content
            result = r.json()
            result['status_code'] = r.status_code
            return result
        else:
            print r.content
            return {'status_code':r.status_code,'variable':None}
        
    def add_variable(self, project_id, variable_data):
        #adds new variable data to the server
        uri = '/cad/api/v0.1/variables/add/' + str(project_id)
        if self.checkUrl() == True:
            r = requests.post(self._url + uri, headers = self._headers, data=json.dumps({'variable':variable_data}))
        else:
            return {'status_code':1404, 'variable':None}
        if (r.status_code >= 200) and (r.status_code < 300):
            print r.content
            return r.json()
        else:
            print r.content
            return {'status_code':r.status_code,'variable':None}

    def get_project_by_number(self, project_number):
        #project_number should be a string already but it's converted to str just in case:
        uri = '/cad/api/v0.1/projects_by_num/' + str(project_number)
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            return {'status_code':1404, 'project':None}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code,'project':None}
    def add_project(self, project_data):
        #creates new project on the server:
        uri = '/cad/api/v0.1/projects/add'
        if self.checkUrl() == True:
            r = requests.post(self._url + uri, headers = self._headers, data=json.dumps({'project':project_data}))
        else:
            return {'status_code':1404, 'project':None}
        if (r.status_code >= 200) and (r.status_code < 300):
            print r.content
            return r.json()
        else:
            print r.content
            return {'status_code':r.status_code,'project':None}

    def get_project(self, project_id):
        #gets project by id
        uri = '/cad/api/v0.1/projects/' + str(project_id)
        if self.checkUrl() == True:
            r = requests.get(self._url + uri, headers = self._headers)
        else:
            return {'status_code':1404, 'project':None}
        if r.status_code == 200:
            return r.json()
        else:
            return {'status_code':r.status_code,'project':None}

class CProject:
    #class storing info about the project on client side
    def __init__(self, dictionary):
        #dictionary is what json returned
        if 'project' in dictionary:
            for key in dictionary['project']:
                setattr(self, key, dictionary['project']['key'])
class CCStore(CCloud):
    #class storing some values for the projects and list of projects
    def set_projects_list(self):
        #gets list of all projects under given url and stores it in the object
        idsList = []
        numsList = []
