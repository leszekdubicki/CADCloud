'feature_module - module containing methods executed when macro feature is either edited or rebuilt
'@author:    Leszek Dubicki
'studentID:  x14125439
'email:  leszek.dubicki@ student.ncirl.ie
'@date: 08/12/2015
'Written in SolidWorks 2014
'Based on example from CADSharp LLC www.cadsharp.com
'Written in SolidWorks 2014

'Creates a macro feature

Public swApp As SldWorks.SldWorks
Public Part As SldWorks.ModelDoc2
Public path As String
Public dirName As String
Dim options As Long
Dim errors As Long
Dim retVal As Long
Public featData As SldWorks.macroFeatureData
Public feat As SldWorks.Feature
Public Doc As SldWorks.ModelDoc2
Public CC As Object
'project variables:
Public projectNumber As String
Public projectId As Integer
Public projectDescription As String
Public projectName As String
Public projectFound As Boolean

'main data storage class:
Public dataObject As FeatureData


'variables for variables (variable:
Dim varValues(1 To 5) As Variant
Dim varNames(1 To 5) As String

'configuration variables
Public url As String
Public proSelCustomInfo As String
Public proSelPathDirection  As Long
Public proSelPathLevel As Long


'functions used across all project:
Public Sub saveConfigData()
    'save all config data (server and retrieval etc)
    featData.SetStringByName "url", url
End Sub
Public Sub saveVarData()
    'save all variables to the macro feature (NOT to the server)
    Dim i As Integer
    Dim typeCode As Long
    For i = LBound(varValues) To UBound(varValues)
        If TypeName(i) = "String" Then
            typeCode = 0
        ElseIf (TypeName(i) = "Integer") Or (TypeName(i) = "Double") Then
            typeCode = 1
        ElseIf TypeName(i) = "Boolean" Then
            typeCode = 2
        End If
        Dim varFieldName As String
        Dim varValue As String
        varFieldName = "variable_" & Str(i)
        featData.SetStringByName varFieldName, varValues(i)
    Next i
End Sub

Public Sub saveAllData()
    'subroutine to save all data to the macro feature data feature
    'save config data:
    saveConfigData
    'save project data from global vars:
    
    'save variables data from global vars:
    
End Sub


Public Sub restoreAllData()
    restoreConfigData
End Sub

Public Sub getProject(ByVal number As String)
    'this sub gets the project number from the server and sets all variables for it
    '(like description, id and others)
    Dim projectData As Variant
    projectData = CC.getprojectbynumber(number)
    'projectData = CC.getprojectbynumber("123457")
    'get values from returned array and assign them to global variables
    If UBound(projectData) > 1 Then
        projectId = projectData(0)
        projectNumber = projectData(1)
        projectName = projectData(2)
        projectDescription = projectData(3)
        projectFound = True
    End If
End Sub

Function getProjectNumber() As String
    'function gets the project number based on options set in GUI
    Dim customInfoName As String
    Dim pn As String
    'set current project selection method from the UI page:
    'getProSelMethod
    Select Case dataObject.proSelMethod
    Case 1
        'get custom info
        customInfoName = dataObject.proSelCustomInfo
        pn = getCustomInfo(customInfoName)
    Case 2
        'calculate project no based on folder:
        pn = getFolderByIndex(dirName, dataObject.proSelPathLevel, dataObject.proSelPathDirection)
    Case 0
        'project should be selected manually
        pn = dataObject.projectNumber
    End Select
    dataObject.projectNumber = pn
    dataObject.saveProjectData
    getProjectNumber = pn
End Function

Public Function getPathLength(path As String) As Integer
    'example path : "D:\lex\nci\CADCloud\test\TEST123\Design\Solidworks"
    'length is every directory without D:, so in this case 7
    'it's required for folder selection slider in ccPropMgr
    Dim p As String
    Dim i As Integer
    p = path
    'removal of the file extension (if the file is there it always ends with .sldprt or .sldasm or .slddrw):
    Dim ext(1 To 3) As String
    ext(1) = ".sldprt"
    ext(2) = ".slddrw"
    ext(3) = ".sldasm"
    For i = 1 To UBound(ext)
        If (Len(p) > 7) And (InStrRev(LCase(p), ext(i)) = Len(p) - Len(ext(i)) + 1) Then
            p = Left(p, Len(p) - Len(ext(i)))
        End If
    Next i
    'removal of the last "\" character if any:
    If (InStrRev(p, "\") = Len(p)) Then
        p = Left(p, Len(p) - 1)
    End If
    'let's make it recursive
    If Len(p) <= 2 Then
        getPathLength = 0
    Else
        p = Left(p, InStrRev(p, "\") - 1)
        getPathLength = 1 + getPathLength(p)
    End If
End Function

Public Function getFolderByIndex(path As String, index As Long, direction As Long) As String
    'gets index-th folder from the beginning or from the end of the path
    'get length of the path (number of folders):
    n = getPathLength(path)
    'build array of all folders:
    Dim folders() As String
    Dim p As String
    p = path
    Dim i As Integer
    Dim sp As Integer
    'remove drive leter:
    sp = InStr(p, ":\")
    If sp > 0 Then
        p = Right(p, Len(p) - sp - 1)
    End If
    For i = 1 To n
        'resize the array:
        ReDim Preserve folders(1 To i)
        'get the position of first "\"
        sp = InStr(p, "\")
        'put the folder int the array:
        If (sp = 0) Then
            folders(i) = p
        Else
            folders(i) = Left(p, sp - 1)
        End If
        p = Right(p, Len(p) - sp)
    Next i
    'set i to be equal to index:
    i = CInt(index)
    If direction = 0 Then
        getFolderByIndex = folders(i)
    Else
        getFolderByIndex = folders(UBound(folders) + 1 - i)
    End If
End Function

Public Function getCustomInfo(infoName As String) As Variant
    'function gets custom info of certain name from the active configuration
    Dim swModel As SldWorks.ModelDoc2
    Dim config As SldWorks.Configuration
    Dim cusPropMgr As SldWorks.CustomPropertyManager
    Dim lRetVal As Boolean
    Dim vPropNames As Variant
    Dim vPropTypes As Variant
    Dim vPropValues As Variant
    Dim ValOut As String
    Dim ResolvedValOut As String
    Dim wasResolved As Boolean
    Dim resolved As Variant
    Dim nNbrProps As Long
    Dim custPropType As Long
    Set swModel = swApp.ActiveDoc
    Set config = swModel.GetActiveConfiguration
    Set cusPropMgr = config.CustomPropertyManager
    'lRetVal = cusPropMgr.Get4(infoName, False, ValOut, ResolvedValOut, wasResolved)
    lRetVal = cusPropMgr.Get4(infoName, False, ValOut, ResolvedValOut)
    If ValOut = "" Then
        'get global custom info
        Set cusPropMgr = swModel.Extension.CustomPropertyManager("")
        lRetVal = cusPropMgr.Get4(infoName, False, ValOut, ResolvedValOut)
    End If
    getCustomInfo = ValOut
End Function

Function swmRebuild(varApp As Variant, varDoc As Variant, varFeat As Variant) As Variant
    Set swApp = varApp
    Set swApp = Application.SldWorks
    Set Part = swApp.ActiveDoc
    Dim boolStatus As Boolean
    Dim i As Integer
    Dim pn As String
    path = swApp.ActiveDoc.GetPathName
    dirName = Left(path, InStrRev(path, "\"))
    Set featData = varFeat.GetDefinition
    Set dataObject = New FeatureData
    'copy reference of feature data to dataObject:
    dataObject.featData = featData
    'get data from macro feature:
    dataObject.restoreConfigData
    dataObject.restoreProjectData
    If dataObject.retrieveMethod = 0 Then
        'refresh data from the server.
        Set CC = CreateObject("Python.CadCloud")
        'CC.setUrl (dataObject.url)
        'set CC field in dataObject also:
        dataObject.CC = CC
        'getProject dataObject.projectNumber
        pn = getProjectNumber
        dataObject.getProject
        For i = 1 To 5
            boolStatus = dataObject.getVariable(i, Part)
        Next i
    End If
End Function

Function swmEditDefinition(varApp As Variant, varDoc As Variant, varFeat As Variant) As Variant
    Dim App As SldWorks.SldWorks
    'Dim Doc As SldWorks.ModelDoc2
    'Dim feat As SldWorks.Feature
    'feadData moved to the header to be global variable
    Dim pm As ccPropMgr
    Set swApp = Application.SldWorks
    Set App = varApp
    Set Doc = varDoc
    Set feat = varFeat
    Set Part = swApp.ActiveDoc
    path = swApp.ActiveDoc.GetPathName
    dirName = Left(path, InStrRev(path, "\"))
    
    Set featData = varFeat.GetDefinition
    Set dataObject = New FeatureData
    'copy reference of feature data to dataObject:
    dataObject.featData = featData
    'get data from macro feature:
    dataObject.restoreConfigData
    'create CadCloud object:
    Set CC = CreateObject("Python.CadCloud")
    'CC.setUrl (dataObject.url)
    'set CC field in dataObject also:
    dataObject.CC = CC
    
    '
    Dim n As Object
    Dim T As Object
    Dim V As Object
    Dim Name As String
    Dim Num As Long
    Dim pName As String
    
    'CC.setUrl ("")
    'FeatData.GetParameters N, T, V
    'FeatData.GetStringByName "Hello", Name
    'FeatData.GetIntegerByName "Something", Num
    Dim List As Variant
    'List = CC.getProjectNumbers
    'MsgBox FeatData.GetParameterCount
    'MsgBox N(0)
    Set pm = New ccPropMgr
    'pm.setFeatData (featData)
    pm.Show
    
    Dim url2 As String
    'featData.GetStringByName "url", url2
    'MsgBox "hehe: " & url2
    'varFeat.ModifyDefinition featData, varDoc, Nothing
    
    EditDefinition = True
End Function


