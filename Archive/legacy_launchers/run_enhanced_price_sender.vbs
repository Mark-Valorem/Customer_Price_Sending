Option Explicit

' VBS Script to launch the Enhanced Price Sheet Email Draft Creator with Templates
' This script provides an easy double-click way to run the enhanced Python automation

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

' Check if the enhanced script exists
If Not objFSO.FileExists(workingDir & "\create_drafts_enhanced.py") Then
    MsgBox "create_drafts_enhanced.py not found in the current directory." & vbCrLf & _
           "Please ensure the script is in the same folder as this VBS file.", _
           vbCritical, "Script Not Found"
    WScript.Quit 1
End If

' Check if templates file exists
If Not objFSO.FileExists(workingDir & "\email_templates.json") Then
    MsgBox "email_templates.json not found." & vbCrLf & _
           "The enhanced version requires the email templates configuration file." & vbCrLf & _
           "Run manage_templates.py first to create templates.", _
           vbExclamation, "Templates Not Found"
    WScript.Quit 1
End If

' No popup - go straight to execution

' Run the enhanced Python script in a visible command window
pythonCommand = "cmd /c ""python create_drafts_enhanced.py & echo. & echo Press any key to close this window... & pause > nul"""

' Execute the command and wait for it to complete
result = objShell.Run(pythonCommand, 1, True)

' Show completion message
If result = 0 Then
    MsgBox "Enhanced draft creation completed successfully!" & vbCrLf & vbCrLf & _
           "Check your Outlook Drafts folder to review the customized emails before sending." & vbCrLf & vbCrLf & _
           "Tip: Use manage_templates.py to create or edit email templates for future use.", _
           vbInformation, "Success"
Else
    MsgBox "There was an error running the enhanced script." & vbCrLf & _
           "Please check the console output for details." & vbCrLf & vbCrLf & _
           "Common issues:" & vbCrLf & _
           "• Missing python-dateutil package (run: pip install python-dateutil)" & vbCrLf & _
           "• Invalid template format in email_templates.json", _
           vbExclamation, "Error"
End If

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing