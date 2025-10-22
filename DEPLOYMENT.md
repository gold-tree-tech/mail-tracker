# Windows Deployment Guide

## Quick Setup

1. Install dependencies:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the server:
```cmd
start_server.bat
```

## Running as Windows Service

1. Download NSSM from https://nssm.cc/download
2. Run `install_service.bat`
3. Start service: `nssm start MailTracker`

Manage service:
- Stop: `nssm stop MailTracker`
- Restart: `nssm restart MailTracker`
- Remove: `nssm remove MailTracker confirm`

## Firewall

Allow external access:
```cmd
netsh advfirewall firewall add rule name="Mail Tracker" dir=in action=allow protocol=TCP localport=5000
```

## Troubleshooting

- **Port in use**: `netstat -ano | findstr :5000`
- **Logs**: Check `logs\service.log` and `logs\service_error.log`