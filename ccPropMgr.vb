'ccPropMgr - module containing user interface used when macro feature definition is being edited
'@author:    Leszek Dubicki
'studentID:  x14125439
'email:  leszek.dubicki@ student.ncirl.ie
'@date: 08/12/2015
Option Explicit

' Handler for PropertyManager page controls
Implements PropertyManagerPage2Handler9

'couple text labels:
Dim pm_Label As PropertyManagerPageLabel
Dim pm_Label2 As PropertyManagerPageLabel
Dim pm_Label3 As PropertyManagerPageLabel
Dim pm_Label4 As PropertyManagerPageLabel
Dim pm_Label5 As PropertyManagerPageLabel
Dim pm_Label6 As PropertyManagerPageLabel
Dim pm_Label7 As PropertyManagerPageLabel
Dim pm_horLineLabel As PropertyManagerPageLabel
Const horLineLabel As Long = 31

' Control objects required for the PropertyManager page
Dim pm_Page As PropertyManagerPage2
Dim pm_servGroup As PropertyManagerPageGroup
Dim pm_servUrl As PropertyManagerPageTextbox

'Selection of when to call the API:
Dim pm_servOptionList As PropertyManagerPageCombobox
'
'button to retrieve all information (in case "on demand" option is selected):
Dim pm_getDataButton As PropertyManagerPageButton
Const getDataButtonID As Long = 101

'selection boxes aren't necessary yet
'Dim pm_Selection As PropertyManagerPageSelectionbox
'Dim pm_Selection2 As PropertyManagerPageSelectionbox


'the projects group:
Dim pm_projectsGroup As PropertyManagerPageGroup
'Dim pm_projectsList As PropertyManagerPageListbox

'method to retrieve projects
Dim pm_proSelRadioList As PropertyManagerPageOption
Dim pm_proSelRadioCustI As PropertyManagerPageOption
Dim pm_proSelRadioFolder As PropertyManagerPageOption
'id-s of above controls
Const proSelRadioIDList As Long = 20
Const proSelRadioIDCustI As Long = 21
Const proSelRadioIDFolder As Long = 22
'buton to retrieve list of projects from a server:
Dim pm_getProjectsButton As PropertyManagerPageButton
'list of projects to pick from:
Dim pm_projectsList As PropertyManagerPageCombobox
'get (try) project for Custom Info or folder project selection:
Dim pm_tryProjectButton As PropertyManagerPageButton
Const tryProjectButtonID As Long = 30
'Text box to type the custom info
Dim pm_proSelCustITxt As PropertyManagerPageTextbox
'combobox is for pick the number from the end or the beginning of the path
Dim pm_proSelDirectionList As PropertyManagerPageCombobox
Const proSelDirectionListID As Long = 26
'and control to select which in order will it be
Dim pm_proSelFolderLevel As PropertyManagerPageSlider
Const proSelFolderLevelID As Long = 27
Dim pm_proSelFolderLabel As PropertyManagerPageLabel
Const proSelFolderLabelID As Long = 28
Dim pm_projectInfoLabel As PropertyManagerPageLabel
Const projectInfoLabelID As Long = 29

Dim pm_Number As PropertyManagerPageNumberbox

Dim pm_RetRadio0 As PropertyManagerPageOption
Dim pm_RetRadio1 As PropertyManagerPageOption

Dim pm_Slider As PropertyManagerPageSlider
Dim pm_Tab As PropertyManagerPageTab
Dim pm_Button As PropertyManagerPageButton
Dim pm_BMPButton As PropertyManagerPageBitmapButton
Dim pm_Bitmap As PropertyManagerPageBitmap
Dim pm_ActiveX As PropertyManagerPageActiveX

Dim ClickedCancel As Boolean
Dim retVal As Long
Dim proNumber As String
'Dim macroFeatureData As SldWorks.macroFeatureData

'________________________________________________
'VARIABLES___VARIABLES___VARIABLES
'five groups of variables definitions - names and where to save the vars
'(either CI or global variable in equations)
'VARIABLE GROUP 1
Dim pm_varGroup1 As PropertyManagerPageGroup
Const varGroup1ID As Long = 110
'textbox with variable name:
Dim pm_varNameBox1 As PropertyManagerPageTextbox
Const varNameBox1ID As Long = 111
'combobox to select which way the communication will be - from SW to CC or the other way:
Dim pm_varDirectionSelection1 As PropertyManagerPageCombobox
Const varDirectionSelection1ID As Long = 115
'combobox to select where to put the variable:
Dim pm_varRecSelection1 As PropertyManagerPageCombobox
Const varRecSelection1ID As Long = 112
'name of either custom property or variable name to put the variable
Dim pm_varValue1 As PropertyManagerPageLabel
Const varValue1ID As Long = 113
'button to try the variable from the server:
Dim pm_varSetButton1 As PropertyManagerPageButton
Const varSetButton1ID As Long = 114


'VARIABLE GROUPS ARRAYS:
Dim pm_varGroup() As PropertyManagerPageGroup
Dim varGroupID() As Long
'textbox with variable name:
Dim pm_varNameBox() As PropertyManagerPageTextbox
Dim varNameBoxID() As Long
'combobox to select which way the communication will be - from SW to CC or the other way:
Dim pm_varDirectionSelection() As PropertyManagerPageCombobox
Dim varDirectionSelectionID() As Long
'combobox to select where to put the variable:
Dim pm_varRecSelection() As PropertyManagerPageCombobox
Dim varRecSelectionID() As Long
'name of either custom property or variable name to put the variable
Dim pm_varValue() As PropertyManagerPageLabel
Dim varValueID() As Long
'button to try the variable from the server:
Dim pm_varSetButton() As PropertyManagerPageButton
Dim varSetButtonID() As Long




'IDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIDIIDIDIDID
' Each control in the page needs a unique ID
Const servGroupID As Long = 1
Const LabelID As Long = 2
Const TextID As Long = 3
Const ComboID As Long = 4

'id-s of projects group items:
Const projectsGroupID As Long = 17
Const projectsListID As Long = 5
Const getProjectsButtonID As Long = 19
Const servOptionListID As Long = 18
Const proSelTxtIDCustI As Long = 25

Const Selection2ID As Long = 6
Const NumberID As Long = 7
Const RadioID As Long = 8
Const SliderID As Long = 9
Const TabID As Long = 10
Const ButtonID As Long = 11
Const BMPButtonID As Long = 12
Const BitmapID As Long = 13
Const ActiveXID As Long = 14
Const RadioID2 As Long = 15
Const LabelID2 As Long = 16
Const LabelID3 As Long = 100
Const LabelID4 As Long = 101
Const LabelID5 As Long = 102
Const LabelID6 As Long = 103


'Additional variables
Dim boolStatus As Boolean
Dim longstatus As Long
Dim projectsList() As Variant



Sub Show()

    pm_Page.Show2 0

End Sub

'set everything on folder settings changed
Sub whenFolderSettingsChanged()
    'save the Level from current slider position
    dataObject.proSelPathDirection = pm_proSelDirectionList.CurrentSelection
    dataObject.proSelPathLevel = pm_proSelFolderLevel.Position
    pm_Label5.caption = Str(dataObject.proSelPathLevel) & ", " & "Directory name is:"
    Dim folder As String
    'folder = getFolderByIndex(dirName, dataObject.proSelPathLevel, dataObject.proSelPathDirection)
    folder = getProjectNumber
    projectNumber = folder
    'display it on the label
    pm_proSelFolderLabel.caption = folder
    'get the project:
    'dataObject
    'getProject projectNumber
    'dataObject.getProject projectNumber
    'SetProjectInfo
End Sub

'change enable status of controls when project selection option changed:
Sub whenProjectSelectionOptChanged()
    'disable all related controls:
    pm_projectsList.Enabled = False
    pm_getProjectsButton.Enabled = False
    pm_proSelCustITxt.Enabled = False
    pm_proSelFolderLabel.Enabled = False
    
    pm_proSelFolderLevel.Enabled = False
    pm_proSelDirectionList.Enabled = False
    'enable only the proper ones
    Select Case dataObject.proSelMethod
    Case 1
        'send changes to dataObject:
        dataObject.proSelMethod = 1
        pm_proSelCustITxt.Enabled = True
        pm_proSelCustITxt.Text = dataObject.proSelCustomInfo
    Case 2
        'send changes to dataObject:
        dataObject.proSelMethod = 2
        pm_proSelDirectionList.Enabled = True
        pm_proSelFolderLevel.Enabled = True
        pm_proSelFolderLabel.Enabled = True
        'MsgBox Left(swApp.ActiveDoc.GetPathName, InStrRev(swApp.ActiveDoc.GetPathName, "\")) ' & vbNewLine & Str(getPathLength(swApp.ActiveDoc.GetPathName))
        'MsgBox swApp.ActiveDoc.GetPathName & vbNewLine & Str(getPathLength(swApp.ActiveDoc.GetPathName))
        Dim l As Integer
        l = getPathLength(dirName)
        boolStatus = pm_proSelFolderLevel.SetRange(1, l)
        'set folder > project num settings controls
        whenFolderSettingsChanged
        
    Case 0
        'send changes to dataObject:
        dataObject.proSelMethod = 0
        pm_getProjectsButton.Enabled = True
        pm_projectsList.Enabled = True
    End Select
End Sub
Function getProjectNumber() As String
    'function gets the project number based on options set in GUI
    Dim customInfoName As String
    Dim pn As String
    'set current project selection method from the UI page:
    getProSelMethod
    Select Case dataObject.proSelMethod
    Case 1
        'get custom info
        customInfoName = pm_proSelCustITxt.Text
        pn = getCustomInfo(customInfoName)
    Case 2
        'calculate project no based on folder:
        pn = getFolderByIndex(dirName, dataObject.proSelPathLevel, dataObject.proSelPathDirection)
    Case 0
        'project should be selected manually
        pn = ""
    End Select
    dataObject.projectNumber = pn
    getProjectNumber = pn
End Function
Sub SetProjectInfo()
    'sets all information about the project into proper controls:
    pm_projectInfoLabel.caption = "Project Id: " & Str(dataObject.projectId) & vbNewLine & _
        "Project Number: " & dataObject.projectNumber & vbNewLine & _
        "Project Name: " & dataObject.projectName & vbNewLine & _
        "Project Desc: " & dataObject.projectDescription & vbNewLine
End Sub

Sub getProSelMethod()
    'Save project selection list
        If pm_proSelRadioList.Checked Then
            'dataObject.featData.SetIntegerByName "project_number_selection_method", 0
            dataObject.proSelMethod = 0
        ElseIf pm_proSelRadioCustI.Checked Then
            'dataObject.featData.SetIntegerByName "project_number_selection_method", 1
            dataObject.proSelMethod = 1
            dataObject.proSelCustomInfo = pm_proSelCustITxt.Text
        ElseIf pm_proSelRadioFolder.Checked Then
            'dataObject.featData.SetIntegerByName "project_number_selection_method", 2
            dataObject.proSelMethod = 2
        End If
End Sub
        

' The following runs when a new instance of the class is created



Private Sub Class_Initialize()

    Dim PageTitle As String
    Dim caption As String
    Dim tip As String
    Dim options As Long
    Dim longerrors As Long
    Dim controlType As Long
    Dim alignment As Long
    
    ' Set the variables for the page
    PageTitle = "CADCloud Get"
   
    options = swPropertyManager_OkayButton _
        + swPropertyManager_CancelButton _
        + swPropertyManagerOptions_LockedPage _
        + swPropertyManagerOptions_PushpinButton
    
    ' Create the PropertyManager page
    Set pm_Page = swApp.CreatePropertyManagerPage(PageTitle, _
        options, Me, longerrors)
   
    ' Make sure that the page was created properly
    If longerrors = swPropertyManagerPage_Okay Then
        ' Add controls to the page
        ' Add a tab
        Set pm_Tab = pm_Page.AddTab(TabID, "CCloud", "", 0)
        ' Add a group box to the tab
        caption = "CadCloud"
        options = swGroupBoxOptions_Visible + _
            swGroupBoxOptions_Expanded
        Set pm_servGroup = pm_Tab.AddGroupBox(servGroupID, caption, options)
        
        options = swControlOptions_Visible + _
              swControlOptions_Enabled
        ' Add a text box for url:
        Set pm_Label2 = pm_servGroup.AddControl2(LabelID2, swControlType_Label, "Server url:", swControlAlign_LeftEdge, options, "")
        Set pm_servUrl = pm_servGroup.AddControl2(TextID, swControlType_Textbox, "", swControlAlign_LeftEdge, options, "")
        'check if feature has an url already saved:
        pm_servUrl.Text = dataObject.url
        '____________________________
        ' Add a combo list box for data retrieve method (offline or online)
        Set pm_Label = pm_servGroup.AddControl2(LabelID, swControlType_Label, "Retrieve data:", swControlAlign_LeftEdge, options, "")
        'Set pm_RetRadio0 = pm_Group.AddControl2(RadioID, swControlType_Option, "On rebuild", swControlAlign_LeftEdge, options, "On rebuild")
        'Set pm_RetRadio1 = pm_Group.AddControl2(RadioID2, swControlType_Option, "On demand", swControlAlign_LeftEdge, options, "On demand")
        Set pm_servOptionList = pm_servGroup.AddControl2(servOptionListID, _
              swControlType_Combobox, caption, alignment, options, tip)
        If Not pm_servOptionList Is Nothing Then
            pm_servOptionList.Height = 20
            Dim listItems(3) As String
            listItems(0) = "On Rebuild"
            listItems(1) = "On Edit Definition"
            pm_servOptionList.AddItems (listItems)
            'get currently saved macro feature data
            Select Case dataObject.retrieveMethod
            Case 0
                pm_servOptionList.CurrentSelection = 0
            Case 1
                pm_servOptionList.CurrentSelection = 1
            End Select
        End If
        'button to retrieve data:
        Set pm_getDataButton = pm_servGroup.AddControl2(getDataButtonID, swControlType_Button, "Get Data", swControlAlign_LeftEdge, options, "Get all data from server")
        'project info:
        dataObject.restoreProjectData
        Set pm_projectInfoLabel = pm_servGroup.AddControl2(projectInfoLabelID, swControlType_Label, "Project Number:", swControlAlign_LeftEdge, options, "")
        SetProjectInfo
        '_____________________________
        '_____________________________
        'Project selection group:
        'opts for creating the group:
        options = swGroupBoxOptions_Visible ' + _
            'swGroupBoxOptions_Expanded
        caption = "Project Selection"
        Set pm_projectsGroup = pm_Tab.AddGroupBox(projectsGroupID, caption, options)
        'opts for controls:
        options = swControlOptions_Visible + _
              swControlOptions_Enabled
        alignment = swControlAlign_LeftEdge
        'descriptive label
        Set pm_Label3 = pm_projectsGroup.AddControl2(LabelID3, swControlType_Label, "Project selection method", swControlAlign_LeftEdge, options, "")
        'alignment = swControlAlign_Indent
        '__________________________________________
        'radio butons telling what method will be used to select project number
        Set pm_proSelRadioList = pm_projectsGroup.AddControl2(proSelRadioIDList, swControlType_Option, "Select project fom list", swControlAlign_LeftEdge, swControlOptions_Visible + swControlOptions_Enabled, "")
        '__________________________________________
        'button to retrieve projects from a box:
        Set pm_getProjectsButton = pm_projectsGroup.AddControl2(getProjectsButtonID, swControlType_Button, "Get Projects", swControlAlign_LeftEdge, options, "Click")
        'controlType = swControlType_Listbox
        caption = ""
        tip = "Select a project from list"
        Set pm_projectsList = pm_projectsGroup.AddControl2(projectsListID, _
              swControlType_Combobox, caption, alignment, options, tip)
        '
        '_______________________________________________________
        'other selections:
        Set pm_horLineLabel = pm_projectsGroup.AddControl2(horLineLabel, swControlType_Label, "__________________________________", swControlAlign_LeftEdge, options, "")
        Set pm_tryProjectButton = pm_projectsGroup.AddControl2(tryProjectButtonID, swControlType_Button, "Try Project", swControlAlign_LeftEdge, options, "Click to retrieve project from the number below")
        
        'part for selection through custom info:
        Set pm_proSelRadioCustI = pm_projectsGroup.AddControl2(proSelRadioIDCustI, swControlType_Option, _
            "Get project using Custom Properity", swControlAlign_LeftEdge, swControlOptions_Visible + swControlOptions_Enabled, "")
        Set pm_Label4 = pm_projectsGroup.AddControl2(LabelID4, swControlType_Label, "Type in the custom info below", swControlAlign_LeftEdge, options, "")
        Set pm_proSelCustITxt = pm_projectsGroup.AddControl2(proSelTxtIDCustI, swControlType_Textbox, "", swControlAlign_LeftEdge, options, "")
        
        '_______________________________________________________
        'part for selection using folder:
        'add radio button:
        Set pm_proSelRadioFolder = pm_projectsGroup.AddControl2(proSelRadioIDFolder, swControlType_Option, "Get project using this file path", swControlAlign_LeftEdge, swControlOptions_Visible + swControlOptions_Enabled, "")
        'list to pick the direction - from end or from the beginning of the path
        Set pm_proSelDirectionList = pm_projectsGroup.AddControl2(proSelDirectionListID, _
              swControlType_Combobox, "Which end to count from", alignment, options, tip)
        Dim directionOpts(1) As String
        directionOpts(0) = "From the beginning of path"
        directionOpts(1) = "From the end of path"
        pm_proSelDirectionList.AddItems (directionOpts)
        pm_proSelDirectionList.CurrentSelection = dataObject.proSelPathDirection
        Set pm_Label5 = pm_projectsGroup.AddControl2(LabelID5, swControlType_Label, "Current Project Number:", swControlAlign_LeftEdge, options, "")
        Set pm_proSelFolderLabel = pm_projectsGroup.AddControl2(proSelFolderLabelID, swControlType_Label, "", swControlAlign_LeftEdge, options, "")
        
        'slider for selecting folder level
        Set pm_proSelFolderLevel = pm_projectsGroup.AddControl2(proSelFolderLevelID, swControlType_Slider, "Select Level", swControlAlign_LeftEdge, options, "Slide to change")
        'set the range:
        boolStatus = pm_proSelFolderLevel.SetRange(1, getPathLength(dirName))
        'set the position
        pm_proSelFolderLevel.Position = dataObject.proSelPathLevel
        'Add label to display the folder / project name:
        
        'select the proper radio  button:
        Select Case dataObject.proSelMethod
        Case 0
            pm_proSelRadioList.Checked = True
        Case 1
            pm_proSelRadioCustI.Checked = True
        Case 2
            pm_proSelRadioFolder.Checked = True
        End Select
        'set everything according to what was selected:
        whenProjectSelectionOptChanged
        SetProjectInfo
        '__________________________________________
        'VARIABLES GROUPS:
        Dim varData As Variant
        Dim varValue As String
        Dim varNum As Integer
        Dim ctrlOpts As Long
        
        'controls creation opts:
        options = swGroupBoxOptions_Visible + _
            swGroupBoxOptions_Expanded
        ctrlOpts = swControlOptions_Visible + _
              swControlOptions_Enabled
        alignment = swControlAlign_LeftEdge
        'items for data direction combobox
        Dim varOpts(0 To 1) As String
        varOpts(0) = "CC > SW"
        varOpts(1) = "SW > CC"
        Dim varOpts2(0 To 1) As String
        varOpts2(0) = "Custom Property"
        varOpts2(1) = "Global Variable"
        
        Dim id As Long
        id = 110
        Dim index As Long
        index = 0
        
        
        For index = 1 To 5
            'assign id's to id arrays:
            ReDim Preserve varGroupID(1 To index)
            ReDim Preserve varNameBoxID(1 To index)
            ReDim Preserve varDirectionSelectionID(1 To index)
            ReDim Preserve varRecSelectionID(1 To index)
            ReDim Preserve varValueID(1 To index)
            ReDim Preserve varSetButtonID(1 To index)
            'redimension controls also:
            ReDim Preserve pm_varGroup(1 To index)
            ReDim Preserve pm_varNameBox(1 To index)
            ReDim Preserve pm_varDirectionSelection(1 To index)
            ReDim Preserve pm_varRecSelection(1 To index)
            ReDim Preserve pm_varValue(1 To index)
            ReDim Preserve pm_varSetButton(1 To index)
            
            varGroupID(index) = id
            varNameBoxID(index) = id + 1
            varDirectionSelectionID(index) = id + 2
            varRecSelectionID(index) = id + 3
            varValueID(index) = id + 4
            varSetButtonID(index) = id + 5
            'increase id by 10
            id = id + 10
            'create variable controls:
            varNum = index
            varData = dataObject.restoreVariableConfig(varNum)
            caption = "VARIABLE " & Str(varNum)
            If varData(1) = "" Then
                options = swGroupBoxOptions_Visible
            Else
                    options = swGroupBoxOptions_Visible + _
                swGroupBoxOptions_Expanded
            End If
            'variable group control:
            Set pm_varGroup(index) = pm_Tab.AddGroupBox(varGroupID(index), caption, options)
            'variable name:
            Set pm_varNameBox(index) = pm_varGroup(index).AddControl2(varNameBoxID(index), swControlType_Textbox, varData(1), alignment, ctrlOpts, "")
            'direction of communication:
            Set pm_varDirectionSelection(index) = pm_varGroup(index).AddControl2(varDirectionSelectionID(index), _
                  swControlType_Combobox, "Direciton of Data", alignment, ctrlOpts, "select which way communication is going - CC > SW or SW > CC")
        
            pm_varDirectionSelection(index).AddItems (varOpts)
            pm_varDirectionSelection(index).CurrentSelection = varData(5)
            Set pm_varRecSelection(index) = pm_varGroup(index).AddControl2(varRecSelectionID(index), _
                  swControlType_Combobox, "Where to put", alignment, ctrlOpts, "select where to put the variable - custom info or equations")
            
            pm_varRecSelection(index).AddItems (varOpts2)
            pm_varRecSelection(index).CurrentSelection = varData(3)
            'add label to display current valuee of the var:
            varValue = dataObject.readVariable(varNum, Part)
            If varValue = "" Then varValue = "<no value>"
            Set pm_varValue(index) = pm_varGroup(index).AddControl2(varValueID(index), swControlType_Label, varValue, swControlAlign_LeftEdge, ctrlOpts, "Value of the first variable")
            'button:
            Set pm_varSetButton(index) = pm_varGroup(index).AddControl2(varSetButtonID(index), swControlType_Button, "Get Variable", swControlAlign_LeftEdge, ctrlOpts, "Click to get variable from server")
        Next index
       
    Else
        'display error message:
        MsgBox "An error occurred while attempting to create the PropertyManager Page", vbCritical
    End If



End Sub

Private Sub PropertyManagerPage2Handler9_OnClose(ByVal Reason As Long)

    If Reason = swPropertyManagerPageClose_Cancel Then

        ' Cancel button clicked
        ClickedCancel = True

    ElseIf Reason = swPropertyManagerPageClose_Okay Then

        ' OK button clicked
        'save the url to the macro parameter:
        url = pm_servUrl.Text
        dataObject.url = url
        '
        'set retrieve method
        If pm_servOptionList.CurrentSelection = 0 Then
            dataObject.retrieveMethod = 0
            
        
        ElseIf pm_servOptionList.CurrentSelection = 1 Then
            dataObject.retrieveMethod = 1
        End If
        '
        getProSelMethod
        End If
        dataObject.saveProjectData
        '_____________________________________________________________
        'save variables data:
        Dim var(0 To 6) As Variant
        Dim varCurrent() As Variant
        Dim i As Integer
        For i = 1 To 5
            varCurrent = dataObject.restoreVariableConfig(i)
            var(0) = varCurrent(0) 'variable value (initial, will be red from SW or CC anyway)
            var(1) = pm_varNameBox(i).Text 'get variable name:
            var(2) = 0 'initially String
            var(3) = pm_varRecSelection(i).CurrentSelection
            var(4) = "" 'for now empty - meand SWName is the same as Name
            var(5) = pm_varDirectionSelection(i).CurrentSelection
            var(6) = varCurrent(6) 'index of equation
            dataObject.saveVariableConfig i, var
        Next i
        'save all modified feature data:
        dataObject.saveData
        'save data from featuredata to feature object:
        feat.ModifyDefinition dataObject.featData, Doc, Nothing
        ClickedCancel = False
   
    Set CC = Nothing
End Sub


Private Sub PropertyManagerPage2Handler9_AfterActivation()

End Sub


Private Sub PropertyManagerPage2Handler9_AfterClose()

    ' Destroy the class
    Set pm_Page = Nothing

End Sub


Private Function PropertyManagerPage2Handler9_OnActiveXControlCreated(ByVal id As Long, ByVal Status As Boolean) As Long
    Debug.Print "ActiveX control created"
End Function


Private Sub PropertyManagerPage2Handler9_OnButtonPress(ByVal id As Long)
    Dim pn As String
    Dim varArray() As Variant
    If id = getProjectsButtonID Then
        'set the url with the one from the window:
        
        url = pm_servUrl.Text
        dataObject.url = pm_servUrl.Text
        'CC.setUrl dataObject.url
        Dim projects As Variant
        Dim i As Integer
        projects = dataObject.CC.getProjectNumbers
        'Const n As Integer = UBound(projects)
        Dim projectsStrList() As String
        'MsgBox UBound(projects)
        If UBound(projects) >= 0 Then
            For i = 0 To UBound(projects)
                ReDim Preserve projectsStrList(0 To i)
                projectsStrList(i) = projects(i)
            Next i
            pm_projectsList.AddItems projectsStrList
        Else
            MsgBox "No projects found"
        End If
        
    ElseIf id = tryProjectButtonID Then
        'get the project from server (I assume that project no is set)
        'check the url
        If Not pm_servUrl.Text = dataObject.url Then
            dataObject.setUrl (pm_servUrl.Text)
        End If
        pn = getProjectNumber
        dataObject.projectNumber = pn
        'dataObject.saveProjectData
        dataObject.getProject
        SetProjectInfo
    
    ElseIf id = getDataButtonID Then
        'get all data - project and variables
        If Not pm_servUrl.Text = dataObject.url Then
            dataObject.setUrl (pm_servUrl.Text)
        End If
        pn = getProjectNumber
        dataObject.getProject pn
        SetProjectInfo
    Else
        'check variable buttons:
        For i = 1 To 5
        If id = varSetButtonID(i) Then
            'get crrent value of variable name:
            varArray = dataObject.restoreVariableConfig(i)
            'get variable name form textbox:
            If Not varArray(1) = pm_varNameBox(i).Text Then
                varArray(1) = pm_varNameBox(i).Text
            End If
            If Not varArray(3) = pm_varRecSelection(i).CurrentSelection Then
                varArray(3) = pm_varRecSelection(i).CurrentSelection
            End If
            If Not varArray(5) = pm_varDirectionSelection(i).CurrentSelection Then
                varArray(5) = pm_varDirectionSelection(i).CurrentSelection
            End If
            dataObject.saveVariableConfig i, varArray
            boolStatus = dataObject.getVariable(i, Part)
            If boolStatus = True Then
                pm_varValue(i).caption = dataObject.readVariable(i, Part)
            Else
                pm_varValue(i).caption = "<failed to get the value>"
            End If
        End If
        Next i
    End If
End Sub


Private Sub PropertyManagerPage2Handler9_OnCheckboxCheck(ByVal id As Long, ByVal Checked As Boolean)
    
End Sub


Private Sub PropertyManagerPage2Handler9_OnComboboxEditChanged(ByVal id As Long, ByVal Text As String)
    
End Sub

'handling combobox selection change event:
Private Sub PropertyManagerPage2Handler9_OnComboboxSelectionChanged(ByVal id As Long, ByVal Item As Long)
    Select Case id
    Case projectsListID
        'this means that project number was picked
        Dim pn As String
        pn = pm_projectsList.ItemText(pm_projectsList.CurrentSelection)
        'get project data based on project no:
        'Dim projectList As Variant
        'projectList = CC.getprojectbynumber(pn)
        dataObject.getProject (pn)
        SetProjectInfo
        'set information of the project displayed:
        'projectList = CC.getProjectNumbers 'this worked
    Case proSelDirectionListID
        whenFolderSettingsChanged
    End Select
    
End Sub
 

Private Sub PropertyManagerPage2Handler9_OnGroupCheck(ByVal id As Long, ByVal Checked As Boolean)

End Sub


Private Sub PropertyManagerPage2Handler9_OnGroupExpand(ByVal id As Long, ByVal Expanded As Boolean)

End Sub

 
Private Function PropertyManagerPage2Handler9_OnHelp() As Boolean

End Function


Private Function PropertyManagerPage2Handler9_OnKeystroke(ByVal Wparam As Long, ByVal Message As Long, ByVal Lparam As Long, ByVal id As Long) As Boolean

End Function


Private Sub PropertyManagerPage2Handler9_OnListboxSelectionChanged(ByVal id As Long, ByVal Item As Long)
   

End Sub

Private Function PropertyManagerPage2Handler9_OnNextPage() As Boolean

End Function


Private Sub PropertyManagerPage2Handler9_OnNumberBoxChanged(ByVal id As Long, ByVal value As Double)
    Debug.Print "Number box changed"
End Sub


Private Sub PropertyManagerPage2Handler9_OnOptionCheck(ByVal id As Long)
    
    Select Case id
    Case proSelRadioIDCustI
        dataObject.proSelMethod = 1
    Case proSelRadioIDFolder
        dataObject.proSelMethod = 2
    Case proSelRadioIDList
        dataObject.proSelMethod = 0
    End Select
    whenProjectSelectionOptChanged
End Sub


Private Sub PropertyManagerPage2Handler9_OnPopupMenuItem(ByVal id As Long)

End Sub


Private Sub PropertyManagerPage2Handler9_OnPopupMenuItemUpdate(ByVal id As Long, retVal As Long)

End Sub


Private Function PropertyManagerPage2Handler9_OnPreview() As Boolean

End Function


Private Function PropertyManagerPage2Handler9_OnPreviousPage() As Boolean

End Function


Private Sub PropertyManagerPage2Handler9_OnRedo()

End Sub


Private Sub PropertyManagerPage2Handler9_OnSelectionboxCalloutCreated(ByVal id As Long)

End Sub


Private Sub PropertyManagerPage2Handler9_OnSelectionboxCalloutDestroyed(ByVal id As Long)

End Sub


Private Sub PropertyManagerPage2Handler9_OnSelectionboxFocusChanged(ByVal id As Long)

    Debug.Print "The focus moved to selection box " & id

End Sub


Private Sub PropertyManagerPage2Handler9_OnSelectionboxListChanged(ByVal id As Long, ByVal Count As Long)
    pm_Page.SetCursor (swPropertyManagerPageCursors_Advance)

    Debug.Print "The list in selection box " & id & " changed"

End Sub


Private Sub PropertyManagerPage2Handler9_OnSliderPositionChanged(ByVal id As Long, ByVal value As Double)
    Select Case id
    Case proSelFolderLevelID
        whenFolderSettingsChanged
    End Select
End Sub


Private Sub PropertyManagerPage2Handler9_OnSliderTrackingCompleted(ByVal id As Long, ByVal value As Double)

End Sub


Private Function PropertyManagerPage2Handler9_OnSubmitSelection(ByVal id As Long, ByVal Selection As Object, ByVal SelType As Long, ItemText As String) As Boolean

    PropertyManagerPage2Handler9_OnSubmitSelection = True

End Function


Private Function PropertyManagerPage2Handler9_OnTabClicked(ByVal id As Long) As Boolean

End Function


Private Sub PropertyManagerPage2Handler9_OnTextboxChanged(ByVal id As Long, ByVal Text As String)
    Select Case id
    Case proSelTxtIDCustI
        dataObject.proSelCustomInfo = pm_proSelCustITxt.Text
    End Select
End Sub


Private Sub PropertyManagerPage2Handler9_OnUndo()

End Sub


Private Sub PropertyManagerPage2Handler9_OnWhatsNew()

End Sub

 

Private Sub PropertyManagerPage2Handler9_OnLostFocus(ByVal id As Long)

    Debug.Print "Control box " & id & " lost focus"

End Sub


Private Sub PropertyManagerPage2Handler9_OnGainedFocus(ByVal id As Long)

   'Dim varArray As Variant

   'varArray = pm_projectsList.GetSelectedItems

   ''pm_projectsList.CurrentSelection = varArray(0)

End Sub


Public Sub PropertyManagerPage2Handler9_OnListBoxRMBUp(ByVal id As Long, ByVal posX As Long, ByVal posY As Long)

End Sub


Public Function PropertyManagerPage2Handler9_OnWindowFromHandleControlCreated(ByVal id As Long, ByVal Status As Boolean) As Long

End Function
 

Public Sub PropertyManagerPage2Handler9_OnNumberboxTrackingCompleted(ByVal id As Long, ByVal value As Double)
'Public Sub PropertyManagerPage2Handler9_OnTextboxChanged(ByVal Id As Long, ByVal Value As String)

End Sub



