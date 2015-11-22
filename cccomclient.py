#import ccclient, os.path, pythoncom
import pythoncom, os.path
import ccclient
from ccclient import CCStore

fName = '.ccguidfile.txt'
#print "hehe"

class CCComClient(CCStore):
    #_reg_clsid_ = "{E51C6BDA-7811-45B3-B962-AADDBDF0E2C3}"
    #_reg_clsid_ = guid()
    _reg_clsid_ = ""
    _reg_desc_ = "Python Cad Cloud Client COM Server"
    _reg_progid_ = "Python.CadCloud"
    _public_methods_ = ["getProjectNumbers", "setUrl", "getUrl"]
    _public_attrs_ = []
    _readonly_attrs_ = []
    def __init__(self):
        CCStore.__init__(self)

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
