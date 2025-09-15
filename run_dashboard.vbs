' Valorem Chemicals - Email Draft Dashboard Launcher
' This script launches the monthly email draft dashboard GUI

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Path to the Python script
strPythonScript = objFSO.BuildPath(strScriptPath, "dashboard.py")

' Check if the Python script exists
If objFSO.FileExists(strPythonScript) Then
    ' Try to run with python command
    strCommand = "python """ & strPythonScript & """"

    ' Run the Python script
    On Error Resume Next
    objShell.Run strCommand, 1, False
    If Err.Number <> 0 Then
        ' If python command fails, try py command
        strCommand = "py """ & strPythonScript & """"
        objShell.Run strCommand, 1, False
        If Err.Number <> 0 Then
            MsgBox "Error launching dashboard. Please ensure Python is installed and accessible." & vbCrLf & vbCrLf & "Command tried: " & strCommand, 16, "Launch Error"
        End If
    End If
    On Error GoTo 0
Else
    MsgBox "Dashboard script not found: " & strPythonScript, 16, "File Not Found"
End If