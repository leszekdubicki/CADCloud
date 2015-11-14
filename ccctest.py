import ccclient
#get an instance of a client:
URL = "http://83.212.82.152:5000"
c = ccclient.CCloud(URL)

print "get all projects:\n"
print c.get_projects_list()
print "\n\n\n"
print "get project by name:"
PROJECT_NUM = '1234564'
PROJECT = c.get_project_by_number(PROJECT_NUM)['project']
print PROJECT
if not PROJECT == None:
    PROJECT_ID = PROJECT['id']
print "get variables within project " + PROJECT['project_number']
VARS = c.get_variables(PROJECT_ID)
print VARS
