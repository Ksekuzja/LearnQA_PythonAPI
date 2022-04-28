import requests

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")

print(response.status_code)