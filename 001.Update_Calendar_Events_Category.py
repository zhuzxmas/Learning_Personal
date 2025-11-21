import json, requests, datetime, os
import configparser
from pandas import DataFrame
from datetime import datetime
import funcLG


login_return = funcLG.func_login() # to login into MS365 and get the return value info.
result = login_return['result']
proxies = login_return['proxies']

refresh_token = result['refresh_token']
access_token = result['access_token']

# Initialize ConfigParser
config = configparser.ConfigParser()

# Read existing config file if it exists (to avoid overwriting other sections)
config_file = 'config.cfg'
if os.path.exists(config_file):
    config.read(config_file)

# Ensure the [azure] section exists
if not config.has_section('azure'):
    config.add_section('azure')

# Set the refresh_token option under [azure]
config.set('azure', 'refresh_token', refresh_token)

# Write back to the config file
with open(config_file, 'w', encoding='utf-8') as configfile:
    config.write(configfile)

print(f"Saved refresh_token to {config_file} under [azure] section.")

# Prepare headers
http_headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# GET /me/calendars
# https://learn.microsoft.com/en-us/graph/api/user-list-calendars?view=graph-rest-1.0&tabs=http

endpoint = "https://graph.microsoft.com/v1.0/me/calendars"
try:
    data = requests.get(endpoint, headers=http_headers, stream=False).json()
except:
    data = requests.get(endpoint, headers=http_headers, stream=False, proxies=proxies).json()
calendar_lists = data['value']
for item in calendar_lists:
    if item['name'] == 'Celine-Nathan':
        calendar_Celine_Nathan_ID = item['id']


# GET /me/calendars/{id}/events
# https://learn.microsoft.com/en-us/graph/api/user-list-events?view=graph-rest-1.0&tabs=http

endpoint = "https://graph.microsoft.com/v1.0/me/calendars/{calendar_Celine_Nathan_ID}/events"
endpoint = "https://graph.microsoft.com/v1.0/me/calendar/events"

http_headers_to_List_Calendar_Events = {
    'Authorization': f'Bearer {access_token}',
    'Prefer': 'outlook.timezone="China Standard Time"',
    "Content-Type": "application/json"
}

# OData filter: subject contains "疫苗"
# Note: Use single quotes inside the filter string
params = {
    "$filter": "contains(subject,'疫苗')",
    "$select": "subject,start,end,id"  # optional: reduce payload
}

try:
    data = requests.get(endpoint, headers=http_headers_to_List_Calendar_Events, params=params, stream=False).json()
except:
    data = requests.get(endpoint, headers=http_headers_to_List_Calendar_Events, params=params, stream=False, proxies=proxies).json()

### here, it fails for family group shared calendar for personal account, not sure why...

# PATCH /me/calendar/events/{id}
# https://learn.microsoft.com/en-us/graph/api/event-update?view=graph-rest-1.0&tabs=http
