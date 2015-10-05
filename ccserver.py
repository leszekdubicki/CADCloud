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
def show_project(project_id):
    return "UNDER CONSTRUCTION"

#projects adding:
@app.route('/cad/api/v0.1/projects/add', methods = ['GET','POST'])
def add_project():
    if request.headers['Content-Type'] == 'application/json':
        #get json object with project data:
        VAR = request.json
        return jsonify(VAR)
    else:
        if request.method == "GET":
            #return project creation form:
            form = ProjectAddForm()
            form.validate_on_submit()
            return render_template('new_project.html',form = form, active = 'projects', get_active = get_active)

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

#get form for creation of a variable
@app.route('/cad/api/v0.1/set_variable/<int:project_id>', methods = ['GET'])
def set_var_form(project_id):
    #type of variable must be worked out from the request:
    if request.headers['Content-Type'] == 'application/json':
        #get json object:
        VAR = request.content
    else:
        P = Project.query.get(project_id)
        p = P.__dict__
        return render_template('set_var_form.html', title="CADCloud", project = p, active = 'home', get_active = get_active)

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
