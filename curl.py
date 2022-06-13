import requests

url = 'http://127.0.0.1:5000/start/application/1'
myobj = {'somekey': 'somevalue'}

x = requests.get(url)

print(x.text)