from flask import Flask, render_template, jsonify
import requests
import feedparser
from datetime import datetime, timezone
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def get_aws_status():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(
            'https://status.aws.amazon.com/rss/ec2-us-east-1.rss',
            headers=headers,
            timeout=15,
            verify=False
        )
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            active_issues = []
            for entry in feed.entries:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                if any(word in title + summary for word in ['issue', 'error', 'outage', 'degraded', 'investigating', 'impact', 'disruption', 'failure']):
                    active_issues.append(entry)
            if len(active_issues) == 0:
                return {
                    'name': 'AWS',
                    'status': 'UP',
                    'last_updated': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    'name': 'AWS',
                    'status': 'DEGRADED',
                    'last_updated': active_issues[0].get('published', 'N/A')
                }
        else:
            return {'name': 'AWS', 'status': 'UNKNOWN', 'last_updated': 'N/A'}
    except Exception as e:
        return {'name': 'AWS', 'status': 'UNKNOWN', 'last_updated': str(e)}

def get_gcp_status():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        }
        response = requests.get(
            'https://status.cloud.google.com/incidents.json',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            incidents = response.json()
            active = [i for i in incidents if i.get('end') is None]
            if len(active) == 0:
                return {'name': 'GCP', 'status': 'UP', 'last_updated': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
            else:
                severity = active[0].get('severity', '').lower()
                status = 'DOWN' if 'high' in severity else 'DEGRADED'
                return {'name': 'GCP', 'status': status, 'last_updated': active[0].get('begin', 'N/A')}
        else:
            return {'name': 'GCP', 'status': 'UNKNOWN', 'last_updated': 'N/A'}
    except Exception as e:
        return {'name': 'GCP', 'status': 'UNKNOWN', 'last_updated': 'N/A'}

def get_azure_status():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml'
        }
        response = requests.get(
            'https://azure.status.microsoft/en-us/status/feed/',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            active_issues = []
            for entry in feed.entries:
                title = entry.get('title', '').lower()
                if any(word in title for word in ['issue', 'outage', 'degraded', 'investigating', 'impact', 'disruption']):
                    active_issues.append(entry)
            if len(active_issues) == 0:
                return {'name': 'Azure', 'status': 'UP', 'last_updated': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
            else:
                return {'name': 'Azure', 'status': 'DEGRADED', 'last_updated': active_issues[0].get('published', 'N/A')}
        else:
            return {'name': 'Azure', 'status': 'UNKNOWN', 'last_updated': 'N/A'}
    except Exception as e:
        return {'name': 'Azure', 'status': 'UNKNOWN', 'last_updated': 'N/A'}

@app.route('/')
def index():
    providers = [get_aws_status(), get_gcp_status(), get_azure_status()]
    checked_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', providers=providers, checked_at=checked_at)

@app.route('/api/status')
def api_status():
    providers = [get_aws_status(), get_gcp_status(), get_azure_status()]
    return jsonify({
        'providers': providers,
        'checked_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/ping')
def ping():
    return 'OK'

@app.route('/api/debug')
def api_debug():
    import traceback
    results = {}
    for name, fn in [('aws', get_aws_status), ('gcp', get_gcp_status), ('azure', get_azure_status)]:
        try:
            results[name] = fn()
        except Exception as e:
            results[name] = {'error': str(e), 'trace': traceback.format_exc()}
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
