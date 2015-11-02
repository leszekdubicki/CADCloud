#CADCloud application for sharing enginering info between CAD apps
#Leszek Dubicki
#student number: x14125439


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

#forms definitions:
class ProjectAddForm(Form):
    name = TextField('Project Name', description='Enter Name of the project here',validators=[Required()])
    project_number = TextField('Project Number', description='Number of the project', validators=[Required()])
    description = TextAreaField(u'Project Description', [validators.optional(), validators.length(max=200)])
    submit_button = SubmitField('Create Project')

class ProjectEditForm(ProjectAddForm):
    submit_button = SubmitField('Update Project')

class VariableEditForm(Form):
    name = TextField('Variable Name', description='Name of the variable',validators=[Required()])
    value = TextField('Variable Value', description='Value',validators=[Required()])
    comment = TextAreaField(u'Comment', [validators.optional(), validators.length(max=200)])
    submit_button = SubmitField('Update Variable')
    vType = None
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.vType == None:
            return True
        else:
            typ = self.vType.data
        if typ == 'number':
            #just check if value can be converted:
            try:
                float(self.value.data)
                return True
            except:
                self.value.errors.append('Must be a number if variable type is number')
                return False
        elif typ == 'boolean':
            #just check if value can be converted:
            if self.value.data not in ['1', '0', 'True', 'False', 'true', 'false']:
                self.value.errors.append('Must be logic value if variable type is boolean')
                return False
            else:
                return True
        else:
            return True

class VariableAddForm(VariableEditForm):
    #http://wtforms.simplecodes.com/docs/0.6.1/fields.html#wtforms.fields.SelectField
    vType = SelectField('Variable Type', description='Type of the variable',validators=[Required()], choices = [('string','String'),('numeric','Numeric'),('boolean','Boolean')])
    #vType = TextField('Project Number', description='Number of the project', validators=[Required()])
    submit_button = SubmitField('Create Variable')

    
if __name__ == '__main__':
    manager.run()
