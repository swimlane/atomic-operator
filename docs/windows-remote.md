# Running Tests Remotely On Windows

> NOTE: To use this on your remote Windows machines, you need to do the following:

1. Run from an elevated PowerShell prompt

```powershell
winrm quickconfig (type yes)
Enable-PSRemoting (type yes)
# Set start mode to automatic
Set-Service WinRM -StartMode Automatic
# Verify start mode and state - it should be running
Get-WmiObject -Class win32_service | Where-Object {$_.name -like "WinRM"}
```

2. Additionally you may need to specify the allowed host to remote into systems:

```powershell
# Trust hosts
Set-Item 'WSMan:localhost\client\trustedhosts' -value * -Force 
NOTE: don't use the * for the value parameter in production - specify your Swimlane instance IP
# Verify trusted hosts configuration
Get-Item WSMan:\localhost\Client\TrustedHosts
```

3. Additional Troubleshooting

```powershell
#If you receive a timeout error or something like that, check and make sure that your remote Windows host network is set to Private and NOT public. You can change it using the following:

# Get Network Profile
Get-NetConnectionProfile

# if the NetworkCategory is set to Public then run the following to set it to Private

Set-NetConnectionProfile -InterfaceAlias Ethernet0 -NetworkCategory Private
# try it again
```
