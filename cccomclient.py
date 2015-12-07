#import ccclient, os.path, pythoncom
import pythoncom, os.path
import ccclient
from ccclient import CCStore

fName = '.ccguidfile.txt'

class CCComClient(CCStore):
    #_reg_clsid_ = "{E51C6BDA-7811-45B3-B962-AADDBDF0E2C3}"
    #_reg_clsid_ = guid()
    _reg_clsid_ = ""
    _reg_desc_ = "Python Cad Cloud Client COM Server"
    _reg_progid_ = "Python.CadCloud"
    _public_methods_ = ["getProjectNumbers", "setUrl", "getUrl", "getprojectbynumber", "getvariable", "get_variable"]
    _public_attrs_ = []
    _readonly_attrs_ = []
    def __init__(self):
        CCStore.__init__(self)
    #def get_project_by_number(self, project_number):
    def getprojectbynumber(self, project_number):
        #retrieve project, but instead of dictionary return list (which will be accesible as variant array in VBA)
        project = CCStore.get_project_by_number(self, project_number)
        #project = {}
        #test dictionary similar to the one that should be returned:
        #project = {'project':{'id':9, 'project_number':'cykkk', 'name':'pykkk', 'description':'hehehehe'}}
        projectList = []
        if 'status_code' in project and project['status_code'] >= 300:
            projectList.append('project_not_found')
        elif ('project' in project) and (not project['project'] == None):
            #building a list of project data:
            p = project['project']
            projectList.append(p['id'])
            projectList.append(p['project_number'])
            projectList.append(p['name'])
            projectList.append(p['description'])
            #change all None values to empty strings since vba has problem with them:
            for i in range(0, len(projectList)-1):
                if projectList[i] == None:
                    projectList[i] = ""
        else:
            projectList.append('project_not_found')
        return projectList
    def get_variable(self, project_id, variable_name):
        #retrieve variable, but instead of dictionary return list (which will be accesible as variant array in VBA)
        var = CCStore.get_variable(self, project_id, variable_name)
        #test dictionary similar to the one that should be returned:
        #project = {'project':{'id':9, 'project_number':'cykkk', 'name':'pykkk', 'description':'hehehehe'}}
        variableList = []
        if (variable_name in var) and (not var[variable_name] == None) and ('available' in var[variable_name]) and (var[variable_name]['available'] == 'yes'):
            #building a list of variable data:
            v = var[variable_name]
            variableList.append(v['id'])
            variableList.append(v['name'])
            variableList.append(v['value'])
            if v['type'] == 'string':
                variableList.append(0)
            elif v['type'] == 'number':
                variableList.append(1)
            elif v['type'] == 'boolean':
                variableList.append(2)
            variableList.append(v['comment'])
            return variableList
        else:
            #return empty list/array
            return []

def guid():
    if os.path.isfile(fName):
        F = file(fName, 'r')
        gid = F.readlines()[0].strip()
        F.close()
    else:
        gid = pythoncom.CreateGuid()
        F = file(fName, 'w')
        F.writelines([str(gid)])
        F.close()
    return gid

if __name__=='__main__':
    #create COM server id:
    _reg_clsid_ = guid()
    CCComClient._reg_clsid_ = _reg_clsid_
    import win32com.server.register
    #get guid for this machine:
    win32com.server.register.UseCommandLine(CCComClient)
