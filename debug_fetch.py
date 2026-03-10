import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("--- Inspecting AWS Response ---")
response = requests.get("https://status.aws.amazon.com/data.json", headers=HEADERS)
data = response.json()
print(f"Number of items in list: {len(data)}")
if len(data) > 0:
    print(f"Keys in first item: {data[0].keys()}")
    print(f"Status of first item: {data[0].get('status')}")

print("\n--- Testing Azure RSS feed ---")
# Often Microsoft uses RSS feeds for status
# Trying a common one
AZURE_RSS = "https://azurestatus.ms/api/v2/feed"
try:
    response = requests.get(AZURE_RSS, headers=HEADERS, timeout=10)
    print(f"Azure RSS Status: {response.status_code}")
except:
    pass

# Or check the official status page source for hints
response = requests.get("https://azure.status.microsoft/en-us/status", headers=HEADERS)
print(f"Azure Main Page Status: {response.status_code}")
