import requests


class Test:
    def test_check(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.post("https://playground.learnqa.ru/api/homework_cookie", data=data)
        cook = response.cookies.get("auth_sid")
        print(cook)
        assert cook == 'name', f"Вместо куки {cook}"
