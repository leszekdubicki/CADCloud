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
    _public_methods_ = ["getProjectNumbers", "setUrl", "getUrl", "getprojectbynumber"]
    _public_attrs_ = []
    _readonly_attrs_ = []
    def __init__(self):
        CCStore.__init__(self)
    #def get_project_by_number(self, project_number):
    def getprojectbynumber(self, project_number):
        #retrieve project, but instead of dictionary return list (which will be accesible as variant array in VBA)
        project = CCStore.get_project_by_number(self, project_number)
        #test dictionary similar to the one that should be returned:
        #project = {'project':{'id':9, 'project_number':'cykkk', 'name':'pykkk', 'description':'hehehehe'}}
        projectList = []
        if 'project' in project and not project['project'] == None:
            #building a list of project data:
            p = project['project']
            projectList.append(p['id'])
            projectList.append(p['project_number'])
            projectList.append(p['name'])
            projectList.append(p['description'])
            return projectList
        else:
            return None

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
