import requests


class Test:
    def test_check(self):
        response = requests.post(" https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        x_secret_homework_header = response.headers['x-secret-homework-header']
        header_value = 'Some secret value'
        assert x_secret_homework_header == header_value, f"Wrong header value"
