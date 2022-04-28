import requests

methods = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]
endpoint = "https://playground.learnqa.ru/ajax/api/compare_query_type"

for method_value in methods:
    print()
    response = requests.get(endpoint, params=method_value)
    print(
        f"Method GET with params = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.get(endpoint, data=method_value)
    print(
        f"Method GET with data = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.post(endpoint, data=method_value)
    print(
        f"Method POST with data = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.post(endpoint, params=method_value)
    print(
        f"Method POST with params = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.put(endpoint, data=method_value)
    print(
        f"Method PUT with data = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.put(endpoint, params=method_value)
    print(
        f"Method PUT with params = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.delete(endpoint, data=method_value)
    print(
        f"Method DELETE with data = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")

    response = requests.delete(endpoint, params=method_value)
    print(
        f"Method DELETE with params = {method_value} "
        f"has following result {response} "
        f"with status code {response.status_code}.")
