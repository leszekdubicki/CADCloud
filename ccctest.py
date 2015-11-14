import ccclient
#get an instance of a client:
URL = "http://83.212.82.152:5000"
c = ccclient.CCloud(URL)

PROJECT_ID = 1
print "get all projects:"
print c.get_projects()
print "get project by id:"
PROJECT = c.get_project(PROJECT_ID)
print PROJECT
print "get variables within project " + PROJECT['project']['project_number']
VARS = c.get_variables(PROJECT_ID)
print VARS
