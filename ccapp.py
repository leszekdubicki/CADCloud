#ccapp.py - base file for CADCloud application for sharing enginering info between CAD apps
#@author:    Leszek Dubicki
#studentID:  x14125439
#email:  leszek.dubicki@student.ncirl.ie
#@date: 08/12/2015



import os
from flask import Flask, jsonify, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import TextField, TextAreaField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators, SelectField
from wtforms.validators import Required
from urlparse import urlparse, urljoin

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../ccdata.sqlite')
print basedir

app = Flask(__name__)

Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path
app.secret_key = "lexosecretkey"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#function for creating dictionary from a model.
def dict_model(model):
    M = {}
    keysToRem = []
    for key in model.__dict__:
        try:
            j = jsonify({key: model.__dict__[key]})
        except:
            keysToRem.append(key)
    for key in model.__dict__:
        #add a key:
        if not key in keysToRem: 
            M[key] = model.__dict__[key]
    return M

#errorhandler...
#from http://flask.pocoo.org/docs/0.10/patterns/apierrors/
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

#Models Definition:
class Project(db.Model):
    #class for projects record
    #__tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    project_number = db.Column(db.String(32), index = True)
    numbers = db.relationship('Number', backref='project', lazy='dynamic')
    strings = db.relationship('String', backref='project', lazy='dynamic')
    booleans = db.relationship('Boolean', backref='project', lazy='dynamic')
    description =  db.Column(db.String(512))
    def __init__(self, name, number, description = ""):
        self.name = name
        self.project_number = number
        self.description = description
    def __repr__(self):
        return "<Project %r>" % self.project_number
    def json(self, var_name = 'project'):
        #returns json representation of the model:
        variable = self.__dict__
        if '_sa_instance_state' in variable:
            variable.__delitem__('_sa_instance_state')
        return jsonify({var_name:variable})

def findProject(projectNumber):
    #funcrion to find out if project with given name exists. returns this project.
    #N = Number.query.filter_by(project_id = project_id)
    projects = Project.query.filter_by(project_number = projectNumber)
    if projects.count() == 0:
        return None
    elif projects.count() > 1:
        return False #not perfect, just to distinguish from none
    else:
        return projects.first()
   
class Number(db.Model):
    #__tablename__ = "numbers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    value = db.Column(db.Float)
    unit = db.Column(db.String(32))
    def __init__(self, name, value, project_id, comment = "", link = "", unit = None):
        self.value = value
        self.name = name
        self.project_id = project_id
        self.comment = comment
        self.link = link
        self.unit = unit

class String(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128))
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    type = 'string'
    def __init__(self, name, value, project_id, comment = "", link = ""):
        self.value = value
        self.name = name
        self.project_id = project_id
        self.comment = comment
        self.link = link

class Boolean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Boolean)
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    def __init__(self, name, value, project_id, comment = "", link = ""):
        self.value = value
        self.name = name
        self.project_id = project_id
        self.comment = comment
        self.link = link


def findVariable(projectId, varName):
    #funcrion to find out if variable with given name exists. returns this variable or False.
    #N = Number.query.filter_by(project_id = project_id)
    strVariables = String.query.filter_by(project_id = projectId, name = varName)
    numVariables = Number.query.filter_by(project_id = projectId, name = varName)
    boolVariables = Boolean.query.filter_by(project_id = projectId, name = varName)
    print boolVariables.count()
    print numVariables.count()
    print strVariables.count()
    notUnique = numVariables.count() != 0 or strVariables.count() != 0 or boolVariables.count() != 0
    print notUnique
    if not notUnique:
        return None
    else:
        variables = []
        if numVariables.count() > 0:
            for v in numVariables:
                variables.append(v)
        if strVariables.count() > 0:
            for v in strVariables:
                variables.append(v)
        if boolVariables.count() > 0:
            for v in boolVariables:
                variables.append(v)
        print variables
        if variables.__len__() > 1:
            return False #not perfect, just to distinguish from none
        elif variables.__len__() == 1:
            return variables[0]
#
##forms definitions:
class ProjectEditForm(Form):
    name = TextField('Project Name', description='Enter Name of the project here',validators=[Required()])
    description = TextAreaField(u'Project Description', [validators.optional(), validators.length(max=200)])
    submit_button = SubmitField('Update Project')


class ProjectAddForm(ProjectEditForm):
    project_number = TextField('Project Number', description='Number of the project', validators=[Required()])
    submit_button = SubmitField('Create Project')
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        #look for a project with given number (must be unique)
        pro = findProject(self.project_number.data)
        if pro == None:
            return True
        else:
            self.project_number.errors.append('Project with given number already exists!')
            


class VariableEditForm(Form):
    name = TextField('Variable Name', description='Name of the variable',validators=[Required()])
    value = TextField('Variable Value', description='Value',validators=[Required()])
    comment = TextAreaField(u'Comment', [validators.optional(), validators.length(max=200)])
    submit_button = SubmitField('Update Variable')
    vType = None
    def setProjectId(self, projectId):
        self.projectId = projectId
    def setType(self, varType):
        self.varType = varType
    def getType(self):
        if self.vType == None:
            return self.varType
        else:
            return self.vType.data
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not self.vType == None:
            typ = self.vType.data.lower()
        else:
            typ = None
        if typ == 'number':
            #just check if value can be converted:
            try:
                float(self.value.data)
            except:
                self.value.errors.append('Must be a number if variable type is number')
                return False
        elif typ == 'boolean':
            #just check if value can be converted:
            if self.value.data not in ['1', '0', 'True', 'False', 'true', 'false']:
                self.value.errors.append('Must be logic value if variable type is boolean')
                return False
        #return true if there are no errors
        return True

class VariableAddForm(VariableEditForm):
    #http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    vType = SelectField('Variable Type', description='Type of the variable',validators=[Required()], choices = [('string','String'),('numeric','Numeric'),('boolean','Boolean')])
    #vType = TextField('Project Number', description='Number of the project', validators=[Required()])
    submit_button = SubmitField('Create Variable')
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        #check if variable with the same name already exists:
        var = findVariable(self.projectId, self.name.data)
        if not var == None:
            self.name.errors.append('Variable with this name already exists within this project!')
            return False
        if not self.vType == None:
            typ = self.vType.data.lower()
        else:
            typ = None
        if typ == 'number':
            #just check if value can be converted:
            try:
                float(self.value.data)
            except:
                self.value.errors.append('Must be a number if variable type is number')
                return False
        elif typ == 'boolean':
            #just check if value can be converted:
            if self.value.data not in ['1', '0', 'True', 'False', 'true', 'false']:
                self.value.errors.append('Must be logic value if variable type is boolean')
                return False
        #return true if there are no errors
        return True

#function to go back:
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target 


#delete confirmation form:

class ConfirmDeleteForm(Form):
    submit_button = SubmitField('Delete')
    cancel_button = SubmitField('Cancel')
    next = HiddenField()
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''
    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))
    
if __name__ == '__main__':
    manager.run()
