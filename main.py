<<<<<<< HEAD
from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/get_301")
print(response.status_code)
=======
import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
>>>>>>> origin/main
