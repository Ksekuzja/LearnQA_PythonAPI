import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # изменить данные пользователя, будучи неавторизованным
    def test_edit_user_without_authorization(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        new_name = "New Name"
        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        print(response2.text)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    # изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_with_authorization_another_user(self):
        register_data_user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_user1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user1_id = self.get_json_value(response1, "id")
        user1_email = register_data_user1["email"]
        user1_first_name = register_data_user1["firstName"]
        user1_password = register_data_user1["password"]

        register_data_user2 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_user2)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user2_id = self.get_json_value(response1, "id")
        user2_email = register_data_user1["email"]
        user2_first_name = register_data_user1["firstName"]
        user2_password = register_data_user1["password"]

        login_data = {
            "email": user2_email,
            "password": user2_password
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        user2_auth_sid = self.get_cookie(response3, "auth_sid")
        user2_token = self.get_header(response3, "x-csrf-token")

        new_name = "New Name"
        response4 = MyRequests.put(f"/user/{user1_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response4, 400)
        print(response4.text)
        Assertions.assert_response_text(response4, "Auth token not supplied")

    # изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @.
    def test_edit_user_with_incorrect_email(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": "email.example.com"}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_text(response3, "Invalid email format")

    # изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_user_with_short_name(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "A"}
        )

        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            "Wrong error message when short length of response param 'firstName'")
