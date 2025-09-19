' Valorem Chemicals - Enhanced Dashboard Launcher v2.0
' This script provides options to launch either the original or enhanced dashboard

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Check which dashboards are available
strOriginalDashboard = objFSO.BuildPath(strScriptPath, "dashboard.py")
strEnhancedDashboard = objFSO.BuildPath(strScriptPath, "dashboard_v2.py")

Dim strMessage, intChoice
strMessage = "VALOREM CHEMICALS - Dashboard Selection" & vbCrLf & vbCrLf
strMessage = strMessage & "Choose which dashboard to launch:" & vbCrLf & vbCrLf

If objFSO.FileExists(strEnhancedDashboard) Then
    strMessage = strMessage & "YES - Enhanced Dashboard v2.0 (RECOMMENDED)" & vbCrLf
    strMessage = strMessage & "     • Customer database management" & vbCrLf
    strMessage = strMessage & "     • Multi-layer verification system" & vbCrLf
    strMessage = strMessage & "     • Real-time security checks" & vbCrLf
    strMessage = strMessage & "     • Complete audit logging" & vbCrLf & vbCrLf
End If

If objFSO.FileExists(strOriginalDashboard) Then
    strMessage = strMessage & "NO - Original Dashboard (Legacy)" & vbCrLf
    strMessage = strMessage & "     • Basic email generation" & vbCrLf
    strMessage = strMessage & "     • Excel-based workflow" & vbCrLf & vbCrLf
End If

strMessage = strMessage & "CANCEL - Exit without launching"

' Show the selection dialog
intChoice = MsgBox(strMessage, vbYesNoCancel + vbQuestion + vbDefaultButton1, "Dashboard Selection")

Dim strPythonScript, strDashboardName

Select Case intChoice
    Case vbYes ' Enhanced Dashboard v2.0
        If objFSO.FileExists(strEnhancedDashboard) Then
            strPythonScript = strEnhancedDashboard
            strDashboardName = "Enhanced Dashboard v2.0"
        Else
            MsgBox "Enhanced Dashboard v2.0 not found!" & vbCrLf & vbCrLf & "File: " & strEnhancedDashboard, 16, "File Not Found"
            WScript.Quit
        End If

    Case vbNo ' Original Dashboard
        If objFSO.FileExists(strOriginalDashboard) Then
            strPythonScript = strOriginalDashboard
            strDashboardName = "Original Dashboard"
        Else
            MsgBox "Original Dashboard not found!" & vbCrLf & vbCrLf & "File: " & strOriginalDashboard, 16, "File Not Found"
            WScript.Quit
        End If

    Case vbCancel
        WScript.Quit

End Select

' Launch the selected dashboard
If strPythonScript <> "" Then
    ' Try to run with pythonw command (no console window)
    strCommand = "pythonw """ & strPythonScript & """"

    ' Run the Python script
    On Error Resume Next
    objShell.Run strCommand, 0, False
    If Err.Number <> 0 Then
        ' If pythonw fails, try python command with visible window
        strCommand = "python """ & strPythonScript & """"
        objShell.Run strCommand, 1, False
        If Err.Number <> 0 Then
            ' If python command fails, try py command
            strCommand = "py """ & strPythonScript & """"
            objShell.Run strCommand, 1, False
            If Err.Number <> 0 Then
                MsgBox "Error launching " & strDashboardName & "." & vbCrLf & vbCrLf & "Please ensure Python is installed and accessible." & vbCrLf & vbCrLf & "Command tried: " & strCommand, 16, "Launch Error"
            End If
        End If
    End If
    On Error GoTo 0
End If