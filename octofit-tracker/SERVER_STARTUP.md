# OctoFit Tracker - Server Startup Instructions

## Start Backend (Django)

1. Open a terminal
2. Run the following commands:

```bash
cd /workspaces/flai-workshop-github-copilot-800/octofit-tracker/backend/octofit_tracker
source ../venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

The backend will be available at:
- Local: http://localhost:8000
- Codespace: https://${CODESPACE_NAME}-8000.app.github.dev

## Start Frontend (React)

1. Open another terminal
2. Run the following commands:

```bash
cd /workspaces/flai-workshop-github-copilot-800/octofit-tracker/frontend
npm start
```

The frontend will be available at:
- Local: http://localhost:3000
- Codespace: https://${CODESPACE_NAME}-3000.app.github.dev

## Verify MongoDB is Running

```bash
ps aux | grep mongod | grep -v grep
```

If MongoDB is not running, start it with:

```bash
mongod --dbpath /data/db --fork --logpath /tmp/mongod.log
```

## Common Issues

### "Failed to fetch" error in frontend
- **Cause**: Backend Django server is not running
- **Solution**: Start the Django backend server (see above)

### CORS errors
- **Cause**: CORS not configured properly
- **Solution**: Already configured in settings.py with `CORS_ALLOW_ALL_ORIGINS = True`

### Connection refused
- **Cause**: Port not forwarded or service not running
- **Solution**: Make sure ports 8000 (backend) and 3000 (frontend) are forwarded and public

## Quick Start (Both Servers)

Open two terminals and run:

**Terminal 1 (Backend):**
```bash
cd /workspaces/flai-workshop-github-copilot-800/octofit-tracker/backend/octofit_tracker && source ../venv/bin/activate && python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```bash
cd /workspaces/flai-workshop-github-copilot-800/octofit-tracker/frontend && npm start
```
