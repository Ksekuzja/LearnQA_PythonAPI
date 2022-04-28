import requests

payload = {"method": "GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)

print(response.text)
