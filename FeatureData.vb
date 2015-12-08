'FeatureData - module containing definition of class that performs operations on macro feature data, Solidworks document and CC server instance.
'it's for synchronizing operations on the feature and on the server.

'@author:    Leszek Dubicki
'studentID:  x14125439
'email:  leszek.dubicki@ student.ncirl.ie
'@date: 08/12/2015
'terminology of the methods suffixes is as follows:
'get / set - means operations on the server
'save/restore - means operations on the macro feature data
'write/read - means operations on Solidworks document.


'Private variables:
'macro feature data object:
Private pFeatData As SldWorks.macroFeatureData

'fields for storing project variables :
'Public varValues(1 To 5) As Variant
'Public varNames(1 To 5) As String

'configuration variables
Private pUrl As String
'data retrieve method from server:
'0 - "On Rebuild"
'1 - "On Edit Definition"
Private pRetrieveMethod As Long
'project selection method:
Private pProSelMethod As Long
'custom info containing project number:
Private pProSelCustomInfo As String
'direction of counting folders in path:
Private pProSelPathDirection  As Long
'how many folders from beginning or end of path count ot get project number:
Private pProSelPathLevel As Long
'CADCloud object (initially public, it will be private in the future):
Private pCC As Object

'project variables:
Private pProjectNumber As String
Private pProjectId As Long
Private pProjectDescription As String
Private pProjectName As String
Private pProjectFound As Boolean
'variable telling if the definition was just edited
'(for use when swmRebuild method is called just after hitting okay in feature definition UI page)
Private pWasJustEdited As Boolean
'amount of variables stored in ccserver (generally fixed to 5, can be altered in the future)
Dim varQty As Integer
'class private variables
Dim errors As Long
Dim retVal As Long
Dim boolStatus As Boolean

Private Sub Class_Initialize()
    'assign initial values to some variables:
    'initial url - empty string
    pUrl = ""
    'amount of variables stored in ccserver (generally fixed to 5, can be altered in the future)
    varQty = 5
    
End Sub

'Definitions of setters and getters:
Public Property Get url() As String
    url = pUrl
End Property
Public Property Let url(u As String)
    If u = "" Then
        u = "None" 'workaround - seems like empty string is passed as numm and causing problems
    End If
    pUrl = u
    pCC.setUrl (u)
End Property

Public Property Get retrieveMethod() As Long
    retrieveMethod = pRetrieveMethod
End Property
Public Property Let retrieveMethod(r As Long)
    pRetrieveMethod = r
End Property

Public Property Get proSelMethod() As Long
    proSelMethod = pProSelMethod
End Property
Public Property Let proSelMethod(r As Long)
    pProSelMethod = r
End Property

Public Property Get proSelCustomInfo() As String
    proSelCustomInfo = pProSelCustomInfo
End Property
Public Property Let proSelCustomInfo(c As String)
    pProSelCustomInfo = c
End Property

Public Property Get proSelPathDirection() As Long
    proSelPathDirection = pProSelPathDirection
End Property
Public Property Let proSelPathDirection(d As Long)
    pProSelPathDirection = d
End Property

Public Property Get proSelPathLevel() As Long
    proSelPathLevel = pProSelPathLevel
End Property
Public Property Let proSelPathLevel(d As Long)
    pProSelPathLevel = d
End Property

Public Property Get CC() As Object
    Set CC = pCC
End Property
Public Property Let CC(c As Object)
    Set pCC = c
    If Not pUrl = "" Then
        'set the url of the server:
        pCC.setUrl (pUrl)
    End If
End Property

Public Property Get featData() As Object
    Set featData = pFeatData
End Property
Public Property Let featData(c As Object)
    Set pFeatData = c
End Property

'project getters and setters
Public Property Get projectNumber() As String
    projectNumber = pProjectNumber
End Property
Public Property Let projectNumber(c As String)
    pProjectNumber = c
End Property

Public Property Get projectId() As Integer
    projectId = pProjectId
End Property
Public Property Let projectId(c As Integer)
    pProjectId = c
End Property

Public Property Get projectDescription() As String
    projectDescription = pProjectDescription
End Property
Public Property Let projectDescription(c As String)
    pProjectDescription = c
End Property

Public Property Get projectName() As String
    projectName = pProjectName
End Property
Public Property Let projectName(c As String)
    pProjectName = c
End Property

Public Property Get projectFound() As Boolean
    projectFound = pProjectFound
End Property
'read-only property therefore no Let method

'subroutines to restore all data from macro feature:
Public Sub restoreConfigData()
    'get data saved in macro feature and writh them into global variables:
    pFeatData.GetStringByName "url", pUrl
    pFeatData.GetStringByName "project_number_custom_info", pProSelCustomInfo
    pFeatData.GetIntegerByName "retrieve_method", pRetrieveMethod
    pFeatData.GetIntegerByName "project_number_selection_method", pProSelMethod
    pFeatData.GetIntegerByName "project_number_folder_direction", pProSelPathDirection
    pFeatData.GetIntegerByName "project_number_folder_level", pProSelPathLevel
    pFeatData.GetStringByName "project_number_custom_info", pProSelCustomInfo
End Sub

'Sub to save all data to macro feature (usually called on closing UI object or at the end of rebuild procedure)
Public Sub saveConfigData()
    pFeatData.SetStringByName "url", pUrl
    pFeatData.SetStringByName "project_number_custom_info", pProSelCustomInfo
    pFeatData.SetIntegerByName "retrieve_method", pRetrieveMethod
    pFeatData.SetIntegerByName "project_number_selection_method", pProSelMethod
    pFeatData.SetIntegerByName "project_number_folder_direction", pProSelPathDirection
    pFeatData.SetIntegerByName "project_number_folder_level", pProSelPathLevel
    pFeatData.SetStringByName "project_number_custom_info", pProSelCustomInfo
End Sub

Public Sub saveProjectData()
    pFeatData.SetIntegerByName "project_id", pProjectId
    pFeatData.SetStringByName "project_name", pProjectName
    pFeatData.SetStringByName "project_description", pProjectDescription
    pFeatData.SetStringByName "project_number", pProjectNumber
End Sub

'restore project data from macro feature data, NOT the server
Public Sub restoreProjectData()
    pFeatData.GetIntegerByName "project_id", pProjectId
    pFeatData.GetStringByName "project_name", pProjectName
    pFeatData.GetStringByName "project_description", pProjectDescription
    pFeatData.GetStringByName "project_number", pProjectNumber
End Sub
'method to save all data to macro feature (NOT Server!)
Public Sub saveData()
    saveConfigData
    saveProjectData
End Sub

Public Sub setUrl(givenUrl As String)
    'set url and CC's url:
    url = givenUrl
    pCC.setUrl url
End Sub

Public Sub getProject(Optional pNumber As String = "")
    'gets project from CC server and stores it in an object
    If pNumber = "" Then
        pNumber = Me.projectNumber
    End If
    'this sub gets the project number from the server and sets all variables for it
    '(like description, id and others)
    Dim projectData As Variant
    projectData = pCC.getprojectbynumber(pNumber)
    'projectData = CC.getprojectbynumber("123457")
    'get values from returned array and assign them to global variables
    'MsgBox TypeName(projectData)
    'If Not IsEmpty(projectData) Then
    If UBound(projectData) > 2 Then
        Me.projectId = projectData(0)
        Me.projectNumber = projectData(1)
        Me.projectName = projectData(2)
        If IsNull(projectData(3)) Then
            projectData(3) = ""
        End If
        Me.projectDescription = projectData(3)
        pProjectFound = True
    Else
        Me.projectId = -1
        Me.projectNumber = ""
        Me.projectName = ""
        Me.projectDescription = ""
        pProjectFound = False
    End If
End Sub

'operations on variables:
Public Function restoreVariableConfig(number As Integer) As Variant()
    'gets variable from feature data, NOT the server:
    '
    'assemble field name to retrieve:
    Dim varValueFieldName As String
    Dim varNameFieldName As String
    Dim varTypeFieldName As String
    Dim varStorageMethodFieldName As String
    Dim varSWNameFieldName As String
    Dim varDirectionFieldName As String
    Dim varEquationIndexFieldName As String
    
    varValueFieldName = "variable_" & Str(number)
    varNameFieldName = "variable_name_" & Str(number)
    varTypeFieldName = "variable_type_" & Str(number)
    varStorageMethodFieldName = "storage_method_" & Str(number)
    varSWNameFieldName = "sw_name_" & Str(number)
    varDirectionFieldName = "variable_direction_" & Str(number)
    varEquationIndexFieldName = "variable_equation_index_" & Str(number)
    
    'determine type of the variable
    Dim varValue As String
    Dim varName As String
    Dim varType As Long
    Dim varStorageMethod As Long
    Dim varSWName As String
    Dim varDirection As Long
    Dim varEquationIndex As Long
    
    pFeatData.GetStringByName varValueFieldName, varValue
    pFeatData.GetStringByName varNameFieldName, varName
    pFeatData.GetIntegerByName varTypeFieldName, varType '0 - string, 1 - number, 2 - boolean (which means 0 or 1)
    pFeatData.GetIntegerByName varStorageMethodFieldName, varStorageMethod
    pFeatData.GetStringByName varSWNameFieldName, varSWName
    pFeatData.GetIntegerByName varDirectionFieldName, varDirection
    pFeatData.GetIntegerByName varEquationIndexFieldName, varEquationIndex
    Dim result() As Variant
    ReDim Preserve result(0 To 6)
    result(0) = varValue
    result(1) = varName
    result(2) = varType
    result(3) = varStorageMethod
    result(4) = varSWName
    result(5) = varDirection
    result(6) = varEquationIndex
    restoreVariableConfig = result
End Function

Public Sub saveVariableConfig(number As Integer, data() As Variant)
    'saves variable options to feature data, NOT the server:
    '
    'assemble field name to retrieve:
    Dim varValueFieldName As String
    Dim varNameFieldName As String
    Dim varTypeFieldName As String
    Dim varStorageMethodFieldName As String
    Dim varSWNameFieldName As String
    Dim varDirectionFieldName As String
    Dim varEquationIndexFieldName As String
    
    varValueFieldName = "variable_" & Str(number)
    varNameFieldName = "variable_name_" & Str(number)
    varTypeFieldName = "variable_type_" & Str(number)
    varStorageMethodFieldName = "storage_method_" & Str(number)
    varSWNameFieldName = "sw_name_" & Str(number)
    varDirectionFieldName = "variable_direction_" & Str(number)
    varEquationIndexFieldName = "variable_equation_index_" & Str(number)

    pFeatData.SetStringByName varValueFieldName, data(0)
    pFeatData.SetStringByName varNameFieldName, data(1)
    pFeatData.SetIntegerByName varTypeFieldName, data(2)
    pFeatData.SetIntegerByName varStorageMethodFieldName, data(3)
    pFeatData.SetStringByName varSWNameFieldName, data(4)
    pFeatData.SetIntegerByName varDirectionFieldName, data(5)
    pFeatData.SetIntegerByName varEquationIndexFieldName, data(6)
End Sub


'function to save one variable (by it's number) to SW custom info or global variable (or other way in the future, eg. to dimension)
Public Function writeVariable(number As Integer, model As SldWorks.ModelDoc2) As Boolean
    'get the variable:
    Dim var() As Variant
    Dim result As Boolean
    var = Me.restoreVariableConfig(number)
    'swCustomInfoText = 30
    'swCustomInfoDate = 64
    'swCustomInfoNumber = 3
    'swCustomInfoYesOrNo = 11
    'retVal = Part.AddCustomInfo("", "Station", 30, Station)
    Select Case var(3)
    Case 0
        'save as custom info /property
        boolStatus = model.DeleteCustomInfo(var(1))
        Select Case var(2)
        Case 0
            'save as text:
            result = model.AddCustomInfo3("", var(1), swCustomInfoText, var(0))
        Case 1
            'save as number:
            result = model.AddCustomInfo3("", var(1), swCustomInfoNumber, var(0))
        Case 2
            'means it's boolean, but still save as number (0 or 1):
            If TypeName(var(0)) = "Boolean" Then
                If var(0) = True Then
                    var(0) = 1
                ElseIf var(0) = False Then
                    var(0) = 0
                End If
            End If
            result = model.AddCustomInfo3("", var(1), swCustomInfoNumber, var(0))
        End Select
    Case 1
        'save as global variable (must be of type numeric):
        If Not var(2) = 1 Then
            MsgBox "Only variables of type number can be saved to equations"
        Else
            Dim swEquationMgr As SldWorks.EquationMgr
            Dim longEquation    As Long
            Set swEquationMgr = model.GetEquationMgr
            If Not swEquationMgr Is Nothing Then
                'from example: http://help.solidworks.com/2014/english/api/sldworksapi/Add_Equations_Example_VB.htm
                'longEquation = swEquationMgr.Add3(0, """A"" = 2", True, swAllConfiguration, Empty)
                
                If var(6) = -1 Then
                    'no index assigned yet, create a new one:
                    Dim index As Integer
                    
                    longEquation = swEquationMgr.Add3(-1, """" & var(1) & """ = " & Str(var(0)), True, swAllConfiguration, Empty)
                    'save assigned index to feature data:
                    var(6) = longEquation
                    Me.saveVariableConfig number, var
                    result = True
                Else
                    'update equation under given index:
                    'longEquation = swEquationMgr.Add3(var(6), """" & var(1) & """ = " & Str(var(0)), True, swAllConfiguration, Empty)
                    longEquation = swEquationMgr.SetEquationAndConfigurationOption(var(6), """" & var(1) & """ = " & Str(var(0)), swAllConfiguration, Empty)
                    result = True
                End If
            End If
        End If
    End Select
    writeVariable = result
End Function

'function to read one variable (by it's number) from SW custom info or global variable (or other way in the future, eg. to dimension)
Public Function readVariable(number As Integer, model As SldWorks.ModelDoc2) As String
    'get the variable from what was saved in the model:
    Dim var() As Variant
    var = Me.restoreVariableConfig(number)
    Select Case var(3)
    Case 0
        Dim value As String
        value = model.GetCustomInfoValue("", var(1))
        Select Case var(2)
        Case 0
            'save as text:
            var(0) = value
        Case 1
            'save as number:
            var(0) = value
        Case 2
            'means it's boolean, but still save as number (0 or 1):
            var(0) = value
        End Select
        readVariable = value
    Case 1
        'read from equations:
        Dim swEquationMgr As SldWorks.EquationMgr
        Dim longEquation    As Long
        Dim equationValue As Double
        Set swEquationMgr = model.GetEquationMgr
        equationValue = swEquationMgr.value(var(6))
        readVariable = Str(equationValue)
    End Select
End Function

'function to get variable from CC server and write it to given model object
Public Function getVariable(number As Integer, model As SldWorks.ModelDoc2) As Boolean
    Dim variable As Variant
    Dim varData() As Variant
    Dim vType As Integer
    Dim result As Boolean
    varData = Me.restoreVariableConfig(number)
    If Not varData(1) = "" Then 'protection fron unset variables:
        variable = pCC.get_variable(pProjectId, varData(1))
        'ccserver will return array with the following data:
        '[variable_id, variable_name, variable_value, variable_type, variable_comment]
        'and it must be converted into the following to save it into macro:
        '[value, name, type, ......] - it's already in varData array...
        If UBound(variable) > 1 Then
            'overwrite vardata:
            varData(0) = variable(2)
            varData(1) = variable(1)
            varData(2) = variable(3)
            result = True
        Else
            'overwrite vardata but only value:
            varData(0) = ""
            varData(2) = 0
            result = False
        End If
        'save to the feature data:
        Me.saveVariableConfig number, varData
        'write variable data to sw:
        Me.writeVariable number, model
        'rerutn status:
        getVariable = result
    Else
        getVariable = False
    End If
End Function

'setvariable function - to send the variable to the server:

