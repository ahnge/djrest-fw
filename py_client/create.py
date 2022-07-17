import requests

endpoint = "http://localhost:8000/api/products/"

data = {"title": "This field is filled"}
get_res = requests.post(endpoint, json=data)

# print(get_res.headers)
# print(get_res.text)
print(get_res.status_code)
print(get_res.json())
