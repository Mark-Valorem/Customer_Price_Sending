Option Explicit

' VBS Script to launch the Price Sheet Email Draft Creator
' This script provides an easy double-click way to run the Python automation

Dim objShell, objFSO
Dim scriptPath, workingDir, pythonCommand
Dim result

' Create objects
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS script is located
scriptPath = WScript.ScriptFullName
workingDir = objFSO.GetParentFolderName(scriptPath)

' Change to the working directory
objShell.CurrentDirectory = workingDir

' Check if Python is available
On Error Resume Next
result = objShell.Run("python --version", 0, True)
If Err.Number <> 0 Then
    MsgBox "Python is not installed or not in PATH." & vbCrLf & _
           "Please install Python 3.7+ and try again.", vbCritical, "Python Not Found"
    WScript.Quit 1
End If
On Error GoTo 0

' Check if the main script exists
If Not objFSO.FileExists(workingDir & "\create_drafts.py") Then
    MsgBox "create_drafts.py not found in the current directory." & vbCrLf & _
           "Please ensure the script is in the same folder as this VBS file.", _
           vbCritical, "Script Not Found"
    WScript.Quit 1
End If

' No popup - go straight to execution

' Run the Python script in a visible command window
pythonCommand = "cmd /c ""python create_drafts.py & echo. & echo Press any key to close this window... & pause > nul"""

' Execute the command and wait for it to complete
result = objShell.Run(pythonCommand, 1, True)

' Show completion message
If result = 0 Then
    MsgBox "Draft creation completed successfully!" & vbCrLf & vbCrLf & _
           "Check your Outlook Drafts folder to review the emails before sending.", _
           vbInformation, "Success"
Else
    MsgBox "There was an error running the script." & vbCrLf & _
           "Please check the console output for details.", _
           vbExclamation, "Error"
End If

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing