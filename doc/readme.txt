Server files include ccapp.py and ccserver.py,
Before running server the following Python packages must be installed:
pip install Flask
pip install Flask-Migrate
pip install Flask-WTF
pip install flask-bootstrap
pip install flask-api


Executing command "python ccserver.py" should start the server listening on  all network interfaces. The server part requires templates and static folder to be placed in the same location as python files

Client components include ccclient.py, cccomclient.py
the client com component require pywin32 module (python for windows extensions - pip install pywin32)
To test python client files can be imported in python console (for example in ipython) and one of the modules must be imported, for example:

import ccclient
c = ccclient.CCloud()
c.setUrl("http://83.212.82.152:5000")
c.get_variable(1, "testnum") #- should return variable testnum for project with id 1

To start com server command "python cccomclient.py" must be executed, than server will be available in windows as "Python.CadCloud"

To test SolidWorks VBA code just run file "macro_feature-ccloud.swp" in Solidworks (tools > macro > run). Feature will be inserted into active document and can then be configured and used.

To test VBA code (for example in Excel) the following declaration must be made

    Dim CC As Object
    Set CC = CreateObject("Python.CadCloud")

'And then call one of the methods, eg.
    pCC.setUrl ("http://leszekdubicki.pythonanywhere.com")
    Dim pNumber As String
    pNumber = Excel.Range("E3")
    Dim projectData As Variant
    projectData = CC.getprojectbynumber(pNumber)
    If UBound(projectData) > 2 Then
        Excel.Range("D4").Value = "Project Id:"
        Excel.Range("E4").Value = projectData(0)
        Excel.Range("D5").Value = "Project Name"
        Excel.Range("E5").Value = projectData(2)
        If IsNull(projectData(3)) Then
            projectData(3) = ""
        End If
        Excel.Range("D6").Value = "Project Description"
        Excel.Range("E6").Value = projectData(3)
    Else
        Excel.Range("D4").Value = "NO Project"
        Excel.Range("E4").Value = ""
        Excel.Range("D5").Value = ""
        Excel.Range("E5").Value = ""
        Excel.Range("D6").Value = ""
        Excel.Range("E6").Value = ""
    End If