from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    # удалить пользователя по ID 2
    def test_delete_user_with_id(self):
        logindata = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=logindata)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(
            response2,
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    #  Создать пользователя, авторизоваться из-под него,
    #  удалить, затем попробовать получить его данные по ID и убедиться,
    #  что пользователь действительно удален.
    def test_delete_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        logindata = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=logindata)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_response_text(response4, "User not found")

    # попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_beeing_authorized_with_another_one(self):
        user1_register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user1_register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_user_id = self.get_json_value(response1, "id")

        user2_register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user2_register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user2_email = user2_register_data["email"]
        user2_password = user2_register_data["password"]

        login_data = {
            "email": user2_email,
            "password": user2_password
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        user2_auth_sid = self.get_cookie(response3, "auth_sid")
        user2_token = self.get_header(response3, "x-csrf-token")

        response4 = MyRequests.delete(
            f"/user/{user1_user_id}",
            headers={"x-csrf-token": user2_auth_sid},
            cookies={"auth_sid": user2_token}
        )
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_response_text(response4, "Auth token not supplied")
