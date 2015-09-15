#CADCloud application for sharing enginering info between CAD apps
#Leszek Dubicki
#student number: x14125439

from ccapp import *


@app.route('/')
def startPage():
    return render_template('index.html', title="CADCloud")


#get all variables for given project number
@app.route('/cad/api/v0.1/variables/<int:project_id>')
def get_variables(project_id):
    return jsonify({'numerics':numerics})

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
    manager.run()
