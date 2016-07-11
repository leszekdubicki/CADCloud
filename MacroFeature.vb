'macro_feature - module inserting macro feature into active solidworks document
'@author:    Leszek Dubicki
'studentID:  x14125439
'email:  leszek.dubicki@ student.ncirl.ie
'@date: 08/12/2015
'Written in SolidWorks 2014
'Creates macro feature that read from CADCloud server (through COM component which is also part of this project)

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swFeatMgr As SldWorks.FeatureManager
Dim swFeat As Feature
    
Sub main()
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc
    
    Dim BaseName As String
    Dim ProgId As String
    Dim vMacroMethods As Variant
    'parameters:
    Dim paramNames, paramTypes, paramValues
    
    Dim paramNameArray(0 To 79) As String
    Dim paramTypeArray(0 To 79) As Long
    Dim paramValueArray(0 To 79) As String
    'first parameter -url of cadCloud server:
    paramNameArray(0) = "url"
    paramTypeArray(0) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(0) = ""
    'second parameter -project number:
    paramNameArray(1) = "project_number"
    paramTypeArray(1) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(1) = ""
    'third parameter - how to retrieve values - on rebuild (0) or during edit-definition (1):
    paramNameArray(2) = "retrieve_method"
    paramTypeArray(2) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(2) = 0 'default value is on rebuild
    'fourth - project id retrieved from cc server:
    paramNameArray(3) = "project_id"
    paramTypeArray(3) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(3) = -1 '-1 means none
    'Project name:
    paramNameArray(4) = "project_name"
    paramTypeArray(4) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(4) = "" 'empty on startup
    'Project description:
    paramNameArray(5) = "project_description"
    paramTypeArray(5) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(5) = "" '-1 means none
    'security method:
    '0 - no security (must be allowed on the server or already set in python com server / cc client instance)
    '1 - user and password stored directly in macro feature
    '2 - user and password stored in custom info fields
    paramNameArray(6) = "security_option"
    paramTypeArray(6) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(6) = 0 'default - no security, should be set upon macro feature creation.
    'username for the server:
    paramNameArray(7) = "login"
    paramTypeArray(7) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(7) = "" 'empty by default
    'username for the server:
    paramNameArray(8) = "password"
    paramTypeArray(8) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(8) = "" 'empty by default
    'how to retrieve project number :
    paramNameArray(9) = "project_number_selection_method"
    paramTypeArray(9) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(9) = 0 'can be 0 - select from list, 1 - get from custom info, or 2 - get based on folder
    'if method to retrieve project number is folder (2)
    '   than the direction of folder level pickup
    '   and index of folder to get must be stored as well :
    paramNameArray(10) = "project_number_folder_direction" 'can be 0(left to right) or 1 (right to left)
    paramTypeArray(10) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(10) = 0
    paramNameArray(11) = "project_number_folder_level" 'count from 0 to length of path
    paramTypeArray(11) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
    paramValueArray(11) = 0
    'if method to retrieve project number is custom info (1)
    '   Than we need to store which custom info to be used:
    paramNameArray(12) = "project_number_custom_info"
    paramTypeArray(12) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
    paramValueArray(12) = "" 'empty by default
    'next series of spare parameters up to index 29 for the future use:
    Dim i As Integer
    For i = 13 To 29
        paramNameArray(i) = "prop_" & Str(i)
        paramTypeArray(i) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
        paramValueArray(i) = ""
    Next i
    '
    '
    'next a series of 5 groups each corresponding to one variable of cc server
    'each group having 4 parameters to store:
    'each variable from CadCloud server has the following fields associated to it:
    'variable fields stored on cc server:
    '- variable name and value (always string)
    '- variable type (ie to what convert it to from string)
    '- where to store the value: name: "storageMethod_i" (where i is a number)
    ', type: integer, values: 0 - custom_info, 1 - global variable
    '- name of the variable inside SW (as it will be visible in custom property or in equations)
    'for start it will be the same as varname
    '- spare fields for the future
    Dim j As Integer
    j = 0
    Dim k As Integer
    k = 0
    For i = 30 To 79 Step 10
        j = j + 1
        paramNameArray(i) = "variable_" & Str(j)
        paramTypeArray(i) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString 'all will be of type string,
        'they will be converted into the appropriate type later
        paramValueArray(i) = ""
        paramNameArray(i + 1) = "variable_name_" & Str(j)
        paramTypeArray(i + 1) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
        paramValueArray(i + 1) = "" 'initialy empty
        paramNameArray(i + 2) = "variable_type_" & Str(j)
        paramTypeArray(i + 2) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
        paramValueArray(i + 2) = -1 '0 - string, 1 - number, 2 - boolean (which means 0 or 1)
        paramNameArray(i + 3) = "storage_method_" & Str(j)
        paramTypeArray(i + 3) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
        paramValueArray(i + 3) = 0 '0 - custom_info, 1 - global variable
        paramNameArray(i + 4) = "sw_name_" & Str(j)
        paramTypeArray(i + 4) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
        paramValueArray(i + 4) = "" 'if empty that means the same as cc name
        paramNameArray(i + 5) = "variable_direction_" & Str(j)
        paramTypeArray(i + 5) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
        paramValueArray(i + 5) = 0 '0 - CC > SW, 1 - SW > CC
        paramNameArray(i + 6) = "variable_equation_index_" & Str(j)
        paramTypeArray(i + 6) = swMacroFeatureParamType_e.swMacroFeatureParamTypeInteger
        paramValueArray(i + 6) = -1 'initially no equation
        'plus four spare parameters for future use:
        For k = 7 To 9
            paramNameArray(i + k) = "variable_" & Str(j) & "_property_" & Str(k)
            paramTypeArray(i + k) = swMacroFeatureParamType_e.swMacroFeatureParamTypeString
            paramValueArray(i + k) = ""
        Next k
    Next i
    '
    
    paramNames = paramNameArray
    paramTypes = paramTypeArray
    paramValues = paramValueArray
    
    
    Dim IconFiles As Object
    Dim options As Integer

    Dim MacroMethods(8) As String
    MacroMethods(0) = swApp.GetCurrentMacroPathName
    MacroMethods(1) = "Feature_Module"
    MacroMethods(2) = "swmRebuild"
    MacroMethods(3) = swApp.GetCurrentMacroPathName
    MacroMethods(4) = "Feature_Module"
    MacroMethods(5) = "swmEditDefinition"
    MacroMethods(6) = ""
    MacroMethods(7) = ""
    MacroMethods(8) = ""
    
    BaseName = "CADCloud"
    ProgId = ""
    vMacroMethods = MacroMethods
    'original declaration:
    'Set ParamNames = Nothing
    'Set ParamTypes = Nothing
    'Set ParamValues = Nothing
    
    'Feature Dimensions:
    Dim DimTypes, DimValues
    
    Dim DimTypesArray(0 To 0) As Long
    Dim DimValuesArray(0 To 0) As Double
    DimTypesArray(0) = swDimensionType_e.swLinearDimension
    DimValuesArray(0) = 0 'remember - it's in meters
    DimTypes = DimTypesArray
    DimValues = DimValuesArray
    
    'Set DimTypes = Nothing
    'Set DimValues = Nothing
    Set EditBodies = Nothing
    Set IconFiles = Nothing
    'options = swMacroFeatureOptions_e.swMacroFeatureEmbedMacroFile
    options = swMacroFeatureOptions_e.swMacroFeatureByDefault

    Set swFeatMgr = swModel.FeatureManager
    Set swFeat = swFeatMgr.InsertMacroFeature3(BaseName, ProgId, vMacroMethods, _
        paramNames, paramTypes, paramValues, DimTypes, DimValues, EditBodies, _
        IconFiles, options)
End Sub

