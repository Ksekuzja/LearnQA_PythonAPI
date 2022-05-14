import pytest
import json
import requests


class Test:
    url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'
    user_agent_list = {
        "UserAgent1": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",

        "UserAgent2": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",

        "UserAgent3": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",

        "UserAgent4": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",

        "UserAgent5": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }

    Expected_values_list = {
        "Expected_values1": {"platform": "Mobile", "browser": "No", "device": "Android"},
        "Expected_values2": {"platform": "Mobile", "browser": "Chrome", "device": "iOS"},
        "Expected_values3": {"platform": "Googlebot", "browser": "Unknown", "device": "Unknown"},
        "Expected_values4": {"platform": "Web", "browser": "Chrome", "device": "No"},
        "Expected_values5": {"platform": "Mobile", "browser": "No", "device": "iPhone"}
    }
    expected_results = [
        (user_agent_list["UserAgent1"],
         Expected_values_list["Expected_values1"]["platform"],
         Expected_values_list["Expected_values1"]["browser"],
         Expected_values_list["Expected_values1"]["device"]),
        (user_agent_list["UserAgent2"],
         Expected_values_list["Expected_values2"]["platform"],
         Expected_values_list["Expected_values2"]["browser"],
         Expected_values_list["Expected_values2"]["device"]),
        (user_agent_list["UserAgent3"],
         Expected_values_list["Expected_values3"]["platform"],
         Expected_values_list["Expected_values3"]["browser"],
         Expected_values_list["Expected_values3"]["device"]),
        (user_agent_list["UserAgent4"],
         Expected_values_list["Expected_values4"]["platform"],
         Expected_values_list["Expected_values4"]["browser"],
         Expected_values_list["Expected_values4"]["device"]),
        (user_agent_list["UserAgent5"],
         Expected_values_list["Expected_values5"]["platform"],
         Expected_values_list["Expected_values5"]["browser"],
         Expected_values_list["Expected_values5"]["device"])
    ]

    @pytest.mark.parametrize('user_agent,platform,browser,device', expected_results)
    def test_check(self, user_agent, platform, browser, device):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                headers={"User-Agent": user_agent}
                                )
        actual_platform = response.json()["platform"]
        actual_browser = response.json()["browser"]
        actual_device = response.json()["device"]

        assert platform == actual_platform, f"Параметр 'platform' неправильный: {actual_platform}. Правильный: {platform}"
        assert browser == actual_browser, f"Параметр 'browser' неправильный: {actual_browser}. Правильный: {browser}"
        assert device == actual_device, f"Параметр 'browser' неправильный: {actual_device}. Правильный: {device}"
