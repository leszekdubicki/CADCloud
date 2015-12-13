import os, os.path
import sys
import random

#add path of CCloud into path:
path = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
#os.chdir(path)
if path not in sys.path:
     sys.path.insert(0, path)
#import ccloud module:
import ccclient
projects = ['TEST124', 'TEST125' , 'TEST126', 'TEST127', 'TEST128', 'TEST129', 'TEST130']

#actually, why not take all projects from the server:
CC = ccclient.CCloud()
CC.setUrl("http://leszekdubicki.pythonanywhere.com")
projects = CC.get_projects()
print projects

#add the following variables to the projects:
variables = []

#variables.append({"name":"banana_engraving", "value":"la Banana", "type":"string"})
variables.append({"name":"custom_engraving_on", "value":0, "type":"number"})
variables.append({"name":"custom_engraving", "value":"engraving_", "type":"string"})
variables.append({"name":"A", "value":1.2, "type":"number"})
variables.append({"name":"B", "value":220, "type":"number"})
variables.append({"name":"C", "value":420, "type":"number"})
variables.append({"name":"track_width", "value":5.4, "type":"number"})
variables.append({"name":"track_depth", "value":8.4, "type":"number"})
variables.append({"name":"tracks_pitch", "value":28., "type":"number"})
variables.append({"name":"no_of_tracks", "value":5, "type":"number"})

for P in projects['projects']:
    print ""
    print "crating variables for project " + projects['projects'][P]["project_number"]
    for v in variables:
        if v['name'] == "custom_engraving_on":
            v['value'] = random.choice([0,1])
        elif v['name'] == "custom_engraving":
            v['value'] = v['value'] + str(random.randint(0,100))
        elif v['name'] == "A":
            v['value'] = random.uniform(.6,3.2)
        elif v['name'] == "B":
            v['value'] = random.uniform(200.,240.)
        elif v['name'] == "C":
            v['value'] = random.uniform(400.,440.)
        elif v['name'] == "track_width":
            v['value'] = random.uniform(2.2,6.)
        elif v['name'] == "track_depth":
            v['value'] = random.uniform(7.,12.)
        elif v['name'] == "tracks_pitch":
            v['value'] = random.uniform(15.,20.)
        elif v['name'] == "no_of_tracks":
            v['value'] = random.randint(5,10)
        print CC.add_variable(P, v)
        print v
