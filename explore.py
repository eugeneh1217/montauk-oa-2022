import requests

URL = "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/"

resp = requests.get(URL)

print(resp.status_code)

# print(list(resp.json().keys()))

print(len(resp.json()["blobs"]))
