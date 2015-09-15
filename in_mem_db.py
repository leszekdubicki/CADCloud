#in memory simple initial database used in initial version of ccserver.py
import ccapp
projects = [
    {'id': 1,
    'name': 'Project 1',
    'number': '12345'
    },
    {'id': 2,
    'name': 'Project 2',
    'number': '12346'
    }]

#numeric values to be shared
numerics = [
    {'id': 1,
        'value': 1254,
        'name': 'h1',
        'link': 'D1@Sketch2@part1.sldprt',
        'unit': 'mm',
        'project_id': 1
    },
    {'id': 2,
        'value': 125456.3,
        'name': 'b1',
        'link': 'D2@Sketch2@part1.sldprt',
        'unit': 'mm',
        'project_id': 1
    }]

#string values to be shared
strings = [
    {'id': 1,
        'value': '1254',
        'name': 'str1',
        'link': 'D1@Sketch2@part1.sldprt',
        'project_id': 2
    },
    {'id': 2,
        'value': 'hehehe',
        'name': 'Engraving',
        'link': 'D2@Sketch2@part1.sldprt',
        'project_id': 1
    }]

#boolean values to be shared
booleans = [
    {'id': 1,
        'value': True,
        'name': 'Custom_Engraving',
        'link': 'Sketch2@part1.sldprt',
        'project_id': 2
    },
    {'id': 2,
        'value': False,
        'name': 'Stopper_Unit',
        'link': 'Stopper.sldasm',
        'project_id': 1
    }]

#ccapp.db.create_all()
"""
for P in projects:
    PM = ccapp.Project(P['name'], P['number'])
    print PM
    ccapp.db.session.add(PM)
    ccapp.db.session.commit()

"""
def test_data():
    for P in projects:
        if ccapp.Project.query.filter_by(project_number = P['number']).count() == 0:
            #add project:
            PM = ccapp.Project(P['name'], P['number'])
            ccapp.db.session.add(PM)
    for N in numerics:
        if ccapp.Number.query.filter_by(name = N['name']).count() == 0:
            #add project:
            NN = ccapp.Number()
            NN.value = N['value']
            NN.name = N['name']
            NN.link= N['link']
            NN.unit= N['unit']
            ccapp.db.session.add(NN)
    for N in strings:
        if ccapp.String.query.filter_by(name = N['name']).count() == 0:
            #add str:
            NN = ccapp.String()
            NN.value = N['value']
            NN.name = N['name']
            NN.link= N['link']
            ccapp.db.session.add(NN)
    for N in booleans:
        if ccapp.Boolean.query.filter_by(name = N['name']).count() == 0:
            #add str:
            NN = ccapp.Boolean()
            NN.value = N['value']
            NN.name = N['name']
            NN.link= N['link']
            ccapp.db.session.add(NN)
    ccapp.db.session.commit()
#P = ccapp.Project.query.all()
#print P
test_data()
