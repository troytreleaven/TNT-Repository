import os, json, requests, msal

def load_env():
    env = {}
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                env[key] = val.strip().strip('"').strip("'")
    return env

def get_token(env):
    app = msal.ConfidentialClientApplication(client_id=env['CLIENT_ID'], client_credential=env['CLIENT_SECRET'], authority=f'https://login.microsoftonline.com/{env["TENANT_ID"]}')
    return app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])['access_token']

env = load_env()
token = get_token(env)
user = env.get('DEFAULT_USER', '')
url = f'https://graph.microsoft.com/v1.0/users/{user}/messages?$top=100&$select=id,from,subject,receivedDateTime,body'
resp = requests.get(url, headers={'Authorization': f'Bearer {token}'})
for msg in resp.json().get('value', []):
    name = msg.get('from', {}).get('emailAddress', {}).get('name', '')
    if 'Rose' in name:
        print('ID:', msg['id'])
        print('From:', name)
        print('Subject:', msg['subject'])
        print('Date:', msg['receivedDateTime'][:10])
        print('Body:', msg.get('body', {}).get('content', '')[:3000])
        print('---')