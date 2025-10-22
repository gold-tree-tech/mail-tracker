# Production Deployment Guide

This guide covers deploying the mail-tracker application to production on Windows using Waitress as the WSGI server.

## Prerequisites

- Python 3.8+
- pip
- Windows 10/11 or Windows Server

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd mail-tracker
```

2. Create a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

## Running in Production

### Quick Start (Manual)

Simply run the batch file:
```cmd
start_server.bat
```

Or run directly:
```cmd
venv\Scripts\activate
python run_server.py
```

### Running as a Windows Service (Recommended)

To run the application as a Windows service that starts automatically:

#### Method 1: Using NSSM (Non-Sucking Service Manager)

1. Download NSSM from https://nssm.cc/download and extract to your project folder

2. Run the installation script:
```cmd
install_service.bat
```

3. Start the service:
```cmd
nssm start MailTracker
```

4. Manage the service:
```cmd
nssm stop MailTracker        # Stop service
nssm restart MailTracker     # Restart service
nssm status MailTracker      # Check status
nssm remove MailTracker confirm  # Remove service
```

#### Method 2: Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "At startup"
4. Action: Start a program
5. Program: `D:\Dev\GoldTreeTech\mail-tracker\venv\Scripts\python.exe`
6. Arguments: `run_server.py`
7. Start in: `D:\Dev\GoldTreeTech\mail-tracker`

## Configuration

### Environment Variables

You can customize the server using environment variables in `run_server.py`:

- **HOST**: Server address (default: `0.0.0.0`)
- **PORT**: Server port (default: `5000`)
- **THREADS**: Number of threads (default: `4`)

Example:
```cmd
set HOST=127.0.0.1
set PORT=8080
set THREADS=8
python run_server.py
```

### IIS Reverse Proxy (Recommended for Windows Server)

If using IIS on Windows Server:

1. Install URL Rewrite and Application Request Routing (ARR) modules
2. Create a new site or use Default Web Site
3. Add this to web.config:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="ReverseProxyInboundRule1" stopProcessing="true">
                    <match url="(.*)" />
                    <action type="Rewrite" url="http://localhost:5000/{R:1}" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```

## Firewall Configuration

If you need to access the server from external networks:

```cmd
netsh advfirewall firewall add rule name="Mail Tracker" dir=in action=allow protocol=TCP localport=5000
```

## Security Considerations

1. **Never expose Flask's development server to the internet**
2. Use a reverse proxy (IIS/nginx) in front of Waitress
3. Enable HTTPS/SSL in production
4. Set appropriate file permissions on `opens.db`
5. Consider using environment variables for sensitive configuration
6. Implement rate limiting to prevent abuse
7. Use Windows Firewall to restrict access
8. Run the service with a limited user account (configure in NSSM)

## Monitoring

Monitor the application using:
- Service logs in `logs\service.log` and `logs\service_error.log`
- Windows Event Viewer for service events
- Task Manager for resource usage
- Consider integrating with monitoring tools (Datadog, New Relic, etc.)

## Updating

To update the application:
```cmd
nssm stop MailTracker
git pull
venv\Scripts\activate
pip install -r requirements.txt --upgrade
nssm start MailTracker
```

## Troubleshooting

- **Service won't start**: Check logs in `logs\service_error.log`
- **Permission issues**: Verify the service user has write access to the database folder
- **Database errors**: Ensure `opens.db` exists and is writable
- **Port conflicts**: Check if port 5000 is in use: `netstat -ano | findstr :5000`
- **Python not found**: Verify the Python path in `install_service.bat` is correct
- **Module not found**: Ensure virtual environment is activated and requirements are installed