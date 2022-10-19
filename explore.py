import requests

URL = "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/"

# resp = requests.get(URL)

# print(resp.status_code)

# print(list(resp.json().keys()))

# print(resp.json()["blobs"][0])
resp = requests.get("https://uhc-tic-mrf.azureedge.net/public-mrf/2022-10-01/2022-10-01_-Big-Valley-Construction-LLC_index.json")
data = resp.json()
ein = data["reporting_structure"][0]["reporting_plans"][0]["plan_id"]
print(ein)
