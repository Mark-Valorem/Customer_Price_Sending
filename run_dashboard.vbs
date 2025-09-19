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

' First try pythonw for silent launch
strCommand = "pythonw.exe """ & strDashboard & """"
On Error Resume Next
objShell.Run strCommand, 0, False

' Check if pythonw failed
If Err.Number <> 0 Then
    Err.Clear

    ' Fallback to python.exe with visible window
    strCommand = "python.exe """ & strDashboard & """"
    objShell.Run strCommand, 1, False

    If Err.Number <> 0 Then
        Err.Clear

        ' Try with full path to Python
        strCommand = "C:\Python313\python.exe """ & strDashboard & """"
        objShell.Run strCommand, 1, False

        If Err.Number <> 0 Then
            ' Show error message if all attempts fail
            MsgBox "Error launching Dashboard v3.0" & vbCrLf & vbCrLf & _
                   "Could not launch the dashboard using:" & vbCrLf & _
                   "- pythonw.exe" & vbCrLf & _
                   "- python.exe" & vbCrLf & _
                   "- C:\Python313\python.exe" & vbCrLf & vbCrLf & _
                   "Please ensure Python is installed correctly." & vbCrLf & vbCrLf & _
                   "Manual launch instructions:" & vbCrLf & _
                   "1. Open Command Prompt" & vbCrLf & _
                   "2. cd """ & strScriptPath & """" & vbCrLf & _
                   "3. python dashboard.py", _
                   16, "Launch Error"
        End If
    End If
End If
On Error GoTo 0