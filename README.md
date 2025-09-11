# Cloud Status Aggregator
Live multi-cloud health dashboard monitoring AWS, GCP, and Azure in one view.
Patent-inspired: Predictive Failure Identification and Proactive Failover in Multi-Cloud Computing Environment by Venkata Srinivas Kantamneni USPTO 19/325718.

## Live App
Production URL: https://cloud-status-aggregator.onrender.com
Note: Hosted on Render free tier. App may take 30 to 60 seconds to wake up on first visit after inactivity.

## What This App Does
- Fetches real-time status from AWS, GCP, and Azure public status APIs
- Displays each provider health as UP or DEGRADED or DOWN or UNKNOWN
- Color coded badges: Green is UP, Yellow is DEGRADED, Red is DOWN, Grey is UNKNOWN
- Auto-refreshes every 60 seconds
- JSON API endpoint at /api/status for programmatic access

## App Endpoints
| Route | Method | Description |
| / | GET | Main dashboard showing all 3 provider statuses |
| /api/status | GET | Returns JSON with all provider statuses |

## How to Use the Dashboard
1. Open https://cloud-status-aggregator.onrender.com in browser
2. See three cards: AWS, GCP, Azure each with current status badge
3. Page auto-refreshes every 60 seconds
4. Green badge means all systems operational
5. Yellow badge means some services degraded
6. Red badge means major outage detected
7. Grey badge means status feed unreachable

## How to Use the JSON API
Call this URL in browser or via curl:
https://cloud-status-aggregator.onrender.com/api/status
Returns JSON with provider name, status, and last_updated for each provider plus a checked_at timestamp.

## Run Locally Without Docker
Requirements: Python 3.11 and pip installed.
Step 1: git clone https://github.com/kantamnenisri/cloud-status-aggregator.git
Step 2: cd cloud-status-aggregator
Step 3: python -m venv venv
Step 4 on Windows: .\venv\Scripts\Activate
Step 5: pip install -r requirements.txt
Step 6: python app.py
Step 7: Open http://localhost:5000 in browser

## Deploy to Render
1. Push this repo to GitHub
2. Go to https://dashboard.render.com
3. Click New then Blueprint
4. Connect GitHub and select this repo
5. Render reads render.yaml and builds Docker image automatically on Render servers
6. Click Apply
7. App goes live at https://cloud-status-aggregator.onrender.com
Every git push to main branch triggers auto-redeploy.

## Project Structure
app.py is the Flask backend.
templates/index.html is the Bootstrap 5 dashboard.
requirements.txt lists Python dependencies.
Dockerfile is the container definition used by Render.
render.yaml is the Render deployment config.
.dockerignore keeps Docker image lean.
.gitignore keeps repo clean.
README.md is this file.

## Tech Stack
Backend: Python 3.11 Flask
Frontend: Bootstrap 5 Vanilla JavaScript
Container: Docker built on Render servers
Hosting: Render free tier
Data Sources: AWS GCP Azure public status APIs

## Data Sources
AWS: https://status.aws.amazon.com/data.json
GCP: https://status.cloud.google.com/incidents.json
Azure: https://azure.status.microsoft/api/status/feed

## Author
Venkata Srinivas Kantamneni
USPTO Patent Application 19/325718

## License
MIT License


## 💡 Inspiration
This project is a reference implementation exploring concepts related to 
multi-cloud reliability engineering. The author holds USPTO patent 
applications in this domain (US 19/325,718 and US 19/344,864).

## Health Check
- Added /ping endpoint for automated health monitoring.
