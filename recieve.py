import requests

PORT = 5000

resp = requests.get(f"http://127.0.0.1:{PORT}/search",
                    json={"COMPANY": "United Healthcare Services, Inc."})

print(resp.status_code)
print(list(resp.json().keys()))

resp = requests.get(f"http://127.0.0.1:{PORT}/search", json={"EIN": 841556137})

print(resp.status_code)
print(list(resp.json().keys()))
