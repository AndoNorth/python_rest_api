import requests

BASE= "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld/ando")
print(response.json())

response = requests.get(BASE + "helloworld/bob")
print(response.json())