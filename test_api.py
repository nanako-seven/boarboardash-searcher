import base64

import requests

with open('in.png', 'rb') as f:
    data = f.read()

url = 'http://localhost:8000/search-images'
arg = {
    'data': base64.b64encode(data).decode(),
    'max_num_hits': 2,
}
r = requests.post(url, json=arg)
print(r.status_code)
