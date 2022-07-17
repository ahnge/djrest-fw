import requests

endpoint = "http://localhost:8000/api/products/1/"

get_res = requests.get(endpoint, json={"title": 'hello world'})

# print(get_res.headers)
# print(get_res.text)
print(get_res.status_code)
print(get_res.json())

