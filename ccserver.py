#ccserver.py - web application file containing definitions of all entry points for CADCloud application for sharing enginering info between CAD apps
#@author:    Leszek Dubicki
#studentID:  x14125439
#email:  leszek.dubicki@student.ncirl.ie
#@date: 08/12/2015

from ccapp import *

#active dictionary to determine which tab is active - for use in templates
def get_active(this, active):
    #function to return either class="active" or string 
    if this == active:
        return "class=active"
    else:
        return ""


#fucntion for going back anywhere:
def redirect_url(default='start_page'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

#errorhandler...
#from http://flask.pocoo.org/docs/0.10/patterns/apierrors/
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#Start Page:
@app.route('/')
def start_page():
    if request.headers['Content-Type'] == 'application/json':
        #basically do nothing - just let know that it's up:
        return jsonify({'cadcloud':'up'})
    else:
        return render_template('index.html', title="CADCloud", active = 'home', get_active = get_active)

#projects listing:
@app.route('/cad/api/v0.1/projects')
def get_projects():
    #get all projects (that this user has access rights to):
    #P = Project.query.filter_by(project_id = project_id)
    #For now all projects:
    P = Project.query.all()
    Pros = {}
    for p in P:
        #P2 = Project.query.get(p.id)
        Pros[p.id] = dict_model(p) 
        #Pros[p.id] = P2.__dict__
        #if '_sa_instance_state' in Pros[p.id]:
        #    Pros[p.id].__delitem__('_sa_instance_state')
        
    if request.headers['Content-Type'] == 'application/json':
        return jsonify({'projects':Pros})
    else:
        #What to show in the table, Combinations of key name - Header text 
        headers = [['name', 'Project Name'],['project_number','Project Number'], ['description','Project descriprion']]
        return render_template('projects.html',projects = Pros, headers = headers, active = 'projects', get_active = get_active)
        

@app.route('/cad/api/v0.1/projects_list')
def get_projects_list():
    #only list of projects id-s and their numbers
    #to keep network traffic low
    if request.headers['Content-Type'] == 'application/json':
        P = Project.query.all()#should be limited to only these two fields.
        Pros = {}
        for p in P:
            #P2 = Project.query.get(p.id)
            #dictionary to find project via by project number
            Pros[p.project_number] =  p.id
        print Pros
        return jsonify({'projects':Pros})
    else:
        #redirect to regular projects list page
        return redirect(url_for('get_projects'))
    

@app.route('/cad/api/v0.1/projects/<int:project_id>')
def get_project(project_id):
    #retrieves only the project with a given id and returns it's html or json representatoin
    project = Project.query.get(project_id)
    if request.headers['Content-Type'] == 'application/json':
        #get json object with project data:
        P2 = Project.query.get(project_id)
        pro =dict_model(P2) 
        return jsonify({'project':pro})
    else:
        return render_template('show_project.html',project = project, active = '', get_active = get_active)

#same but get project by number. There shouldn't be two projects with the same number, newertheless app will return the first project with given number
@app.route('/cad/api/v0.1/projects_by_num/<string:project_number>')
def get_project_by_number(project_number):
    #get first project (there should not be more than one:
    project = Project.query.filter_by(project_number = project_number).first()
    #redirect to standard get project by id route:
    return redirect(url_for('get_project', project_id = project.id))


#projects adding:
@app.route('/cad/api/v0.1/projects/add', methods = ['GET','POST'])
def add_project():
    if request.headers['Content-Type'] == 'application/json' and request.method.lower() == 'post':
        #get json object with project data:
        VAR = request.json['project']
        if ('name' in VAR)  and ('project_number' in VAR):#there must be validators here
            #check if project with given no exists:
            projects = Project.query.filter_by(project_number = VAR['project_number'])
            if projects.count() > 0:
                #project exists, return error
                return jsonify({'project':None, 'status':'exists'}), status.HTTP_406_NOT_ACCEPTABLE
            if not "description" in VAR:
                VAR["description"] = ""
            p = Project(VAR['name'], VAR['project_number'], VAR['description'])
            db.session.add(p)
            db.session.commit()
            #get full model (with id)
            p = Project.query.filter_by(project_number = VAR['project_number']).first()
            VAR = dict_model(p)
            return jsonify({'project':VAR, 'status':'success'}), status.HTTP_201_CREATED
        else:
            return jsonify({'project':None, 'status':'failure'}), status.HTTP_400_BAD_REQUEST
    else:
        #return project creation form:
        form = ProjectAddForm()
        if form.validate_on_submit():
            #add projet to database:
            p = Project(request.form['name'], request.form['project_number'], request.form['description'])
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('get_project', project_id = p.id))
        return render_template('new_project.html',form = form, active = '', get_active = get_active, method = 'POST')

#projects editing:
@app.route('/cad/api/v0.1/projects/edit/<int:project_id>', methods = ['GET', 'PUT', 'POST'])
def edit_project(project_id):
    if request.headers['Content-Type'] == 'application/json':
        #get json object with project data:
        P = Project.query.get(project_id)
        VAR = request.json['project']
        keys = ['name', 'project_number', 'description']
        for k in keys:
            if k in VAR  and not VAR[k] == P.name:
                P.name = VAR[k]
        db.session.commit()
        return jsonify(VAR)
    else:
        #get project: 
        P = Project.query.get(project_id)
        #return project creation form:
        form = ProjectEditForm(name = P.name, project_number = P.project_number, description = P.description)
        #if request.method == 'PUT' and form.validate():
        if form.validate_on_submit():
            #add projet to database:
            #db.session.add(p)
            if not request.form['name'] == P.name:
                P.name = request.form['name']
            if not request.form['project_number'] == P.project_number:
                P.project_number = request.form['project_number']
            if not request.form['description'] == P.description:
                P.description = request.form['description']
            db.session.commit()
            return redirect(url_for('get_project', project_id = P.id))
        return render_template('new_project.html',form = form, active = '', get_active = get_active)

#projects deleting:
@app.route('/cad/api/v0.1/projects/delete/<int:project_id>', methods = ['GET', 'POST'])
def delete_project(project_id):
    if request.headers['Content-Type'] == 'application/json':
        #get json object with project data:
        P = Project.query.get(project_id)
        VAR = request.json['project']
        if 'confirm_delete' in VAR:
            VAR['deleted'] = True
            db.session.delete(P)
            db.session.commit()
        return jsonify({'project':VAR})
    else:
        #get project: 
        P = Project.query.get(project_id)
        form = ConfirmDeleteForm()
        if request.method == 'POST':
            if 'cancel_button' in request.form:
                return form.redirect('start_page')
            elif 'submit_button' in request.form:
                #delete the project:
                db.session.delete(P)
                db.session.commit()
                return form.redirect('start_page')
        else:
            return render_template('confirm_delete_project.html',project = P, form = form, active = '', get_active = get_active)

#creation of a variable
@app.route('/cad/api/v0.1/variables/add/<int:project_id>', methods = ['GET','POST'])
def add_variable(project_id):
    #type of variable must be worked out from the request:
    if (request.headers['Content-Type'] == 'application/json') and (request.method.lower() == "post"):
        P = Project.query.get(project_id)
        if P == None:
            #project doesn't exist, return sth about that:
            return jsonify({'variable':None, 'status':'project doesnt exist'}), status.HTTP_406_NOT_ACCEPTABLE
        #
        #get json object:
        if (not 'variable' in request.json):
            return jsonify({'variable':None, 'status':'incomplite data'}), status.HTTP_406_NOT_ACCEPTABLE
        VAR = request.json['variable']
        #check if variable of the name exists within this project:
        if (not 'name' in VAR) or (not 'value' in VAR):
            return jsonify({'variable':None, 'status':'incomplite data'}), status.HTTP_406_NOT_ACCEPTABLE
        elif not findVariable(project_id, VAR['name']) == None:
            #exists, so return error:
            return jsonify({'variable':None, 'status':'variable exists'}), status.HTTP_406_NOT_ACCEPTABLE

        if ('type' in VAR) and (VAR['type'] == 'string'):
                if not 'comment' in VAR:
                    VAR['comment'] = ''
                v = String(VAR['name'],VAR['value'], project_id, VAR['comment'])
                db.session.add(v)
                db.session.commit()
                VAR = dict_model(String.query.filter_by(name=VAR['name'], project_id = project_id).first())
        elif 'type' in VAR and VAR['type'] == 'number':
                if 'name' in VAR and 'value' in VAR:
                    if not 'comment' in VAR:
                        VAR['comment'] == ''
                    if not 'unit' in VAR:
                        VAR['unit'] == ''
                    v = Number(VAR['name'],VAR['value'], project_id, VAR['comment'], unit = VAR['unit'])
        elif 'type' in VAR and VAR['type'] == 'boolean':
                if 'name' in VAR and 'value' in VAR:
                    if not 'comment' in VAR:
                        VAR['comment'] == ''
                    v = Boolean(VAR['name'],VAR['value'], project_id, VAR['comment'])
        return jsonify({'variable':VAR})
    else:
        P = Project.query.get(project_id)
        p = P.__dict__
        form = VariableAddForm()
        form.setProjectId(project_id)
        if form.validate_on_submit():
            #add variable to database:
            if request.form['vType'].lower() == 'string':
                #creating string variable for the project:
                v = String(request.form['name'],request.form['value'], project_id, request.form['comment'])
            elif request.form['vType'].lower() == 'numeric':
                #creating numeric variable for the project:
                v = Number(request.form['name'],request.form['value'], project_id, request.form['comment'])
            elif request.form['vType'].lower() == 'boolean':
                #creating boolean variable for the project:
                if request.form['value'].lower() in ['true', '1']:
                    value = True
                elif request.form['value'].lower() in ['false', '0']:
                    value = False
                #if value == None:
                    #return error
                v = Boolean(request.form['name'],value, project_id, request.form['comment'])
            db.session.add(v)
            db.session.commit()
            return redirect(url_for('get_project', project_id = project_id))
        return render_template('new_variable.html', project = P, form = form, active = '', get_active = get_active)

#editing a variable
@app.route('/cad/api/v0.1/variables/edit/<int:project_id>/<string:variable_type>/<int:variable_id>', methods = ['GET', 'PUT', 'POST'])
def edit_variable(project_id, variable_type, variable_id):
    #type of variable must be worked out from the request:
    variable_type = variable_type.lower()
    if (request.headers['Content-Type'] == 'application/json') and (request.method.lower() == "put"):
        P = Project.query.get(project_id)
        if P == None:
            #project doesn't exist, return sth about that:
            return jsonify({'variable':None, 'status':'project doesnt exist'}), status.HTTP_406_NOT_ACCEPTABLE
        if variable_type == 'string':
            v = String.query.get(variable_id)
        elif variable_type == 'number':
            v = Number.query.get(variable_id)
        elif variable_type == 'boolean':
            v = Boolean.query.get(variable_id)
        if v == None:
            #project doesn't exist, return sth about that:
            return jsonify({'variable':None, 'status':'variable doesnt exist'}), status.HTTP_406_NOT_ACCEPTABLE
        if (not v == None) and (not P == None):
            #get json object:
            VAR = request.json['variable']
            if ('name' in VAR) and (not VAR['name'] == v.name):
                v.name = VAR['name']
            if ('value' in VAR) and (not VAR['value'] == v.value):
                v.value = VAR['value']
            if ('comment' in VAR) and  (not VAR['comment'] == v.comment):
                v.comment = VAR['comment']
            db.session.commit()
            return jsonify({'variable':VAR, 'status':'success'}), status.HTTP_201_CREATED
        else:
            return jsonify({'variable':None}), status.HTTP_406_NOT_ACCEPTABLE
    else:
        #regular html request
        P = Project.query.get(project_id)
        p = P.__dict__
        if variable_type == 'string':
            v = String.query.get(variable_id)
        elif variable_type == 'number':
            v = Number.query.get(variable_id)
        elif variable_type == 'boolean':
            v = Boolean.query.get(variable_id)
        form = VariableEditForm(name = v.name, value = v.value, comment = v.comment, vType = variable_type)
        #below setters help finding out id the name of the variable isn't taken:
        form.setProjectId(project_id)
        #form.setType(variable_type)
        #actually type doesn't matter, there can be only one variable with given name
        if form.validate_on_submit():
            #add variable to database:
            if not request.form['name'] == v.name:
                v.name = request.form['name']
            if not request.form['value'] == v.value:
                v.value = request.form['value']
            if not request.form['comment'] == v.comment:
                v.comment = request.form['comment']
            db.session.commit()
            return redirect(url_for('get_project', project_id = project_id))
        return render_template('new_variable.html', project = P, form = form, active = '', get_active = get_active)

#delete variable:
@app.route('/cad/api/v0.1/variables/delete/<int:project_id>/<string:variable_type>/<int:variable_id>', methods = ['GET', 'POST'])
def delete_variable(project_id, variable_type, variable_id):
    #get database objects:
    P = Project.query.get(project_id)
    if variable_type == 'string':
        v = String.query.get(variable_id)
    elif variable_type == 'number':
        v = Number.query.get(variable_id)
    elif variable_type == 'boolean':
        v = Boolean.query.get(variable_id)
    if (request.headers['Content-Type'] == 'application/json') and (request.method.lower() == 'delete'):
        #get json object with project data:
        if v['name'] in request.json:
            VAR = request.json[v['name']]
        if 'confirm_delete' in VAR:
            db.session.delete(v)
            db.session.commit()
            VAR['deleted'] = True
        return jsonify({v['name']:VAR})
    else:
        #get project: 
        form = ConfirmDeleteForm()
        if request.method == 'POST':
            if 'cancel_button' in request.form:
                return form.redirect('start_page')
            elif 'submit_button' in request.form:
                #delete the project:
                db.session.delete(v)
                db.session.commit()
                return form.redirect('start_page')
        else:
            return render_template('confirm_delete_variable.html', project = P, variable = v, form = form, active = '', get_active = get_active)

#editing a variable by name:
@app.route('/cad/api/v0.1/variables/edit/<int:project_id>/<string:variable_name>', methods = ['GET', 'PUT', 'POST'])
def edit_variable_by_name(project_id, variable_name):
    v = findVariable(project_id, variable_name)
    if v == None:
        #no variable with given name, must return error of sime kind
        raise InvalidUsage('Variable not found', status_code=410)
    elif not v == False:
        #we have one variable, return json of it:
        if request.headers['Content-Type'] == 'application/json':
            if (not v == None):
                #get json object:
                VAR = request.json['variable']
                if ('name' in VAR) and (not VAR['name'] == v.name):
                    v.name = VAR['name']
                if ('value' in VAR) and (not VAR['value'] == v.value):
                    v.value = VAR['value']
                if ('comment' in VAR) and  (not VAR['comment'] == v.comment):
                    v.comment = VAR['comment']
                db.session.commit()
                return jsonify({'variable':VAR, 'status':'success'}), status.HTTP_201_CREATED

            else:
                return jsonify({'variable':None}), status.HTTP_406_NOT_ACCEPTABLE
        else:
            return redirect(url_for('edit_variable', project_id = project_id, variable_type = v.type, variable_id = v.id))
        #return redirect(url_for('edit_variable', project_id = project_id, variable_type = v.type, variable_id = v.id), code = status.HTTP_304_NOT_MODIFIED)

#get all variables for given project number
@app.route('/cad/api/v0.1/variables/<int:project_id>')
def get_variables(project_id):
    #get all variables within given project:
    N = Number.query.filter_by(project_id = project_id)
    S = String.query.filter_by(project_id = project_id)
    B = Boolean.query.filter_by(project_id = project_id)
    numerics = []
    for n in N:
        numerics.append(dict_model(n))
    strings = []
    for s in S:
        strings.append(dict_model(s))
    booleans = []
    for b in B:
        booleans.append(dict_model(b))
    if request.headers['Content-Type'] == 'application/json':
        return jsonify({'numbers':numerics, 'strings':strings, 'booleans':booleans})
    else:
        #return "You've requested variables for project " + str(project_id) + "\n" + str({'numerics':numerics})
        return jsonify({'numbers':numerics, 'strings':strings, 'booleans':booleans})

#get a variable within a project by name
@app.route('/cad/api/v0.1/get_variable/<int:project_id>/<string:var_name>', methods = ['GET'])
def get_var(project_id, var_name):
    V = Number.query.filter_by(project_id = project_id, name = var_name)
    if not V.count() == 0:
        variable = dict_model(V.first())
        variable['type'] = 'number'
    if V.count() == 0:
        V = String.query.filter_by(project_id = project_id, name = var_name)
        variable = dict_model(V.first())
        variable['type'] = 'string'
    if V.count() == 0:
        V = Boolean.query.filter_by(project_id = project_id, name = var_name)
        variable = dict_model(V.first())
        variable['type'] = 'boolean'
    if not V.count() == 0:
        variable['available'] = 'yes'
        if '_sa_instance_state' in variable:
            variable.__delitem__('_sa_instance_state')
        return jsonify({var_name:variable})
    else:
        return jsonify({var_name:{'available':'no'}})


#______________________________________________________________________________________________________
#all below will be probably removed
#set a variable for a project
@app.route('/cad/api/v0.1/set_variable/<int:project_id>/<string:var_name>', methods = ['POST'])
def set_var(project_id, var_name):
    #type of variable must be worked out from the request:
    if request.headers['Content-Type'] == 'application/json':
        #get json object:
        VAR = request.json
        return jsonify(VAR)
    else:
        return request.form["name"]

#get one number variable
@app.route('/cad/api/v0.1/numerics/<int:var_id>', methods = ['GET'])
def get_numeric(var_id):
    #get numeric with given id:
    N = Number.query.get(var_id)
    return jsonify({'number':number})

@app.route('/cad/api/v0.1/strings/', methods = ['POST'])
def create_string_variable():
    stringVar = {
        'id': strings[-1]['id']+1,
        'name': request.json['name'],
        'project_id': request.json['project_id'],
        'link': request.json['link']}
    strings.append(stringVar)
    return jsonify({'string':stringVar}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
