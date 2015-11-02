#CADCloud application for sharing enginering info between CAD apps
#Leszek Dubicki
#student number: x14125439

from ccapp import *

#active dictionary to determine which tab is active - for use in templates
def get_active(this, active):
    #function to return either class="active" or string 
    if this == active:
        return "class=active"
    else:
        return ""

#Start Page:
@app.route('/')
def start_page():
    if request.headers['Content-Type'] == 'application/json':
        return jsonify(request.headers)
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
        P2 = Project.query.get(p.id)
        Pros[p.id] = P2.__dict__
        if '_sa_instance_state' in Pros[p.id]:
            Pros[p.id].__delitem__('_sa_instance_state')
    if request.headers['Content-Type'] == 'application/json':
        return jsonify(Pros)
    else:
        #What to show in the table, Combinations of key name - Header text 
        headers = [['name', 'Project Name'],['project_number','Project Number'], ['description','Project descriprion']]
        return render_template('projects.html',projects = Pros, headers = headers, active = 'projects', get_active = get_active)
        
    
@app.route('/cad/api/v0.1/projects/<int:project_id>')
def get_project(project_id):
    project = Project.query.get(project_id)
    if request.headers['Content-Type'] == 'application/json':
        #get json object with project data:
        VAR = request.json
        return jsonify(VAR)
    else:
        return render_template('show_project.html',project = project, active = '', get_active = get_active)

#projects adding:
@app.route('/cad/api/v0.1/projects/add', methods = ['GET','POST'])
def add_project():
    if request.headers['Content-Type'] == 'application/json' and request.method.lower() == 'post':
        #get json object with project data:
        VAR = request.json['project']
        if True:#there must be validators here
            p = Project(VAR['name'], VAR['project_number'], VAR['description'])
            db.session.add(p)
            db.session.commit()
        return jsonify(VAR)
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

#creation of a variable
@app.route('/cad/api/v0.1/variables/add/<int:project_id>', methods = ['GET','POST'])
def add_variable(project_id):
    #type of variable must be worked out from the request:
    if request.headers['Content-Type'] == 'application/json':
        P = Project.query.get(project_id)
        #get json object:
        VAR = request.json['variable']
        if 'type' in VAR and VAR['type'] == 'string':
                if 'name' in VAR and 'value' in VAR:
                    if not 'comment' in VAR:
                        VAR['comment'] == ''
                    v = String(VAR['name'],VAR['value'], project_id, VAR['comment'])
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
        db.session.add(v)
        db.session.commit()
        return jsonify({'variable':VAR})
    else:
        P = Project.query.get(project_id)
        p = P.__dict__
        form = VariableAddForm()
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
    if request.headers['Content-Type'] == 'application/json':
        P = Project.query.get(project_id)
        VAR = request.json['variable']
        if variable_type == 'string':
            v = String.query.get(variable_id)
        elif variable_type == 'number':
            v = Number.query.get(variable_id)
        elif variable_type == 'boolean':
            v = Boolean.query.get(variable_id)
        #get json object:
        if not VAR['name'] == v.name:
            v.name = VAR['name']
        if not VAR['value'] == v.value:
            v.value = VAR['value']
        if not VAR['comment'] == v.comment:
            v.comment = VAR['comment']
        db.session.commit()
        return jsonify({'variable':VAR})
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

#get all variables for given project number
@app.route('/cad/api/v0.1/variables/<int:project_id>')
def get_variables(project_id):
    #get all variables within given project:
    N = Number.query.filter_by(project_id = project_id)
    S = String.query.filter_by(project_id = project_id)
    B = Boolean.query.filter_by(project_id = project_id)
    numerics = []
    for n in N:
        numerics.append(n.__dict__)
        if '_sa_instance_state' in numerics[-1]:
            numerics[-1].__delitem__('_sa_instance_state')
    strings = []
    for s in S:
        strings.append(s.__dict__)
        if '_sa_instance_state' in strings[-1]:
            strings[-1].__delitem__('_sa_instance_state')
    booleans = []
    for b in B:
        booleans.append(b.__dict__)
        if '_sa_instance_state' in booleans[-1]:
            booleans[-1].__delitem__('_sa_instance_state')
    if request.headers['Content-Type'] == 'application/json':
        return jsonify({'numbers':numerics, 'strings':strings, 'booleans':booleans})
    else:
        #return "You've requested variables for project " + str(project_id) + "\n" + str({'numerics':numerics})
        return jsonify({'numbers':numerics, 'strings':strings, 'booleans':booleans})

#get a variable within a project by name
@app.route('/cad/api/v0.1/get_variable/<int:project_id>/<string:var_name>', methods = ['GET'])
def get_var(project_id, var_name):
    V = Number.query.filter_by(project_id = project_id, name = var_name)
    if V.count() == 0:
        V = String.query.filter_by(project_id = project_id, name = var_name)
    if V.count() == 0:
        V = Boolean.query.filter_by(project_id = project_id, name = var_name)
    if not V.count() == 0:
        variable = V.first().__dict__
    if '_sa_instance_state' in variable:
        variable.__delitem__('_sa_instance_state')
    return jsonify({var_name:variable})

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
