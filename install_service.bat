@echo off
nssm install MailTracker "%CD%\venv\Scripts\python.exe" "%CD%\run_server.py"
nssm set MailTracker AppDirectory "%CD%"
nssm set MailTracker DisplayName "Mail Tracker"
nssm set MailTracker Start SERVICE_AUTO_START
nssm set MailTracker AppStdout "%CD%\logs\service.log"
nssm set MailTracker AppStderr "%CD%\logs\service_error.log"
echo Done! Run: nssm start MailTracker
pause