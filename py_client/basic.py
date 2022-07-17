import requests

endpoint = "http://localhost:8000/api/"

get_res = requests.post(endpoint, json={"title": 'hello world'})

# print(get_res.headers)
# print(get_res.text)
print(get_res.status_code)
print(get_res.json())
