import requests

BASE= "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/1", {"likes": 10, "name":"ando's funny video", "views" : 121})
print(response.json())

response = requests.get(BASE + "video/1")
print(response.json())