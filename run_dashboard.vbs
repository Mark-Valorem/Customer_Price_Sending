' Valorem Chemicals - Dashboard Launcher v3.0
' This script launches the dashboard directly without terminal

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Path to the dashboard
strDashboard = objFSO.BuildPath(strScriptPath, "dashboard.py")

' Check if dashboard exists
If Not objFSO.FileExists(strDashboard) Then
    MsgBox "Dashboard not found!" & vbCrLf & vbCrLf & "File: " & strDashboard, 16, "File Not Found"
    WScript.Quit
End If

' Launch the dashboard using pythonw (no console window)
strCommand = "pythonw """ & strDashboard & """"

' Run the Python script
On Error Resume Next
objShell.Run strCommand, 0, False

If Err.Number <> 0 Then
    ' If pythonw fails, show error message
    MsgBox "Error launching Dashboard v3.0" & vbCrLf & vbCrLf & _
           "Please ensure Python is installed and accessible." & vbCrLf & vbCrLf & _
           "If the problem persists, try running the dashboard directly:" & vbCrLf & _
           "python dashboard.py", _
           16, "Launch Error"
    WScript.Quit
End If
On Error GoTo 0