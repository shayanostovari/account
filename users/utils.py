import requests
from account.local_settings import SMS_API, MY_NUMBER


def send_otp(phone, otp):
    API_KEY = SMS_API
    URL = "https://api.sms.ir/v1/send"

    data = {
        "MobileNumbers": [phone],
        "Messages": [f"Your OTP is: {otp}"],
        "LineNumber": MY_NUMBER,
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }

    response = requests.post(URL, json=data, headers=headers)
    return response.status_code == 200
