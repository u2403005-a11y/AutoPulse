import requests

payload = {'brand':'Tesla','model':'Model 3','year':2019,'km_driven':30000}
try:
    r = requests.post('http://127.0.0.1:5000/api/predict', json=payload, timeout=10)
    print('status', r.status_code)
    print(r.json())
except Exception as e:
    print('error', e)
