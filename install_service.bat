@echo off
REM Install Mail Tracker as a Windows Service using NSSM
REM Download NSSM from: https://nssm.cc/download

SET SERVICE_NAME=MailTracker
SET PYTHON_PATH=%CD%\venv\Scripts\python.exe
SET SCRIPT_PATH=%CD%\run_server.py
SET NSSM=nssm.exe

echo Installing %SERVICE_NAME% as a Windows Service...

REM Install the service
%NSSM% install %SERVICE_NAME% "%PYTHON_PATH%" "%SCRIPT_PATH%"

REM Set service parameters
%NSSM% set %SERVICE_NAME% AppDirectory "%CD%"
%NSSM% set %SERVICE_NAME% DisplayName "Mail Tracker Service"
%NSSM% set %SERVICE_NAME% Description "Email tracking pixel server"
%NSSM% set %SERVICE_NAME% Start SERVICE_AUTO_START

REM Set environment variables (optional)
REM %NSSM% set %SERVICE_NAME% AppEnvironmentExtra PORT=5000 THREADS=4

REM Set log files
%NSSM% set %SERVICE_NAME% AppStdout "%CD%\logs\service.log"
%NSSM% set %SERVICE_NAME% AppStderr "%CD%\logs\service_error.log"

echo Service installed successfully!
echo To start: nssm start %SERVICE_NAME%
echo To stop: nssm stop %SERVICE_NAME%
echo To remove: nssm remove %SERVICE_NAME% confirm
pause