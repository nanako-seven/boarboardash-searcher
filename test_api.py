import base64

import requests


# url = 'http://localhost:8000/_internal/add-image'
# arg = {
#     'url': 'https://mz.eastday.com/60028752.jpg'
# }
with open('a.jpg', 'rb') as f:
    data = f.read()
url = 'http://localhost:8000/search-images'
arg = {
    'data': base64.b64encode(data).decode(),
    'max_num_hits': 10
}
r = requests.post(url, json=arg)
print(r.json())
print(r.status_code)
