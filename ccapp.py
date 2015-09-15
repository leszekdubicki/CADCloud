#CADCloud application for sharing enginering info between CAD apps
#Leszek Dubicki
#student number: x14125439


import os
from flask import Flask, jsonify, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../ccdata.sqlite')
print basedir

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path

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
    def __init__(self, name, number):
        self.name = name
        self.project_number = number
    def __repr__(self):
        return "<Project %r>" % self.project_number

class Number(db.Model):
    #__tablename__ = "numbers"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    unit = db.Column(db.String(32))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class String(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128))
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class Boolean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Boolean)
    name = db.Column(db.String(32), index = True)
    link = db.Column(db.String(128))
    comment = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

if __name__ == '__main__':
    manager.run()
