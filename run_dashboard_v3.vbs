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

' Try pythonw first (no console window)
strCommand = "pythonw.exe """ & strDashboard & """"
On Error Resume Next
intReturn = objShell.Run(strCommand, 0, True)

' If pythonw failed or exited with error, try python with window
If Err.Number <> 0 Or intReturn <> 0 Then
    Err.Clear
    ' Try python.exe with visible window for debugging
    strCommand = "python.exe """ & strDashboard & """"
    intReturn = objShell.Run(strCommand, 1, False)

    If Err.Number <> 0 Then
        ' If python also fails, show detailed error
        MsgBox "Error launching Dashboard v3.0" & vbCrLf & vbCrLf & _
               "Neither pythonw.exe nor python.exe could launch the dashboard." & vbCrLf & vbCrLf & _
               "Please ensure Python is installed and accessible." & vbCrLf & vbCrLf & _
               "You can try running manually from command prompt:" & vbCrLf & _
               "cd """ & strScriptPath & """" & vbCrLf & _
               "python dashboard.py", _
               16, "Launch Error"
    End If
End If
On Error GoTo 0