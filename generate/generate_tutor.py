import random
import requests

from app.helpers.enums import ClassEnum
from app.schemas.sche_subject import SubjectEnum
from tests.const import PREFIX, DEFAULT_SUBJECT


def generate_phone_number():
    area_code = random.randint(100, 999)
    prefix = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return f"{area_code}{prefix}{line_number}"


def random_grade():
    random_color = random.choice(list(ClassEnum))
    return random_color.value


def random_subject():
    random_s = random.choice(list(SubjectEnum))
    return random_s.value


# Example usage
DOMAIN = "http://127.0.0.1:5000"


def new_tutor():
    phone = generate_phone_number()
    user = requests.post(f"{DOMAIN + PREFIX}/auth/register", json={
        "fullName": "string",
        "phone": phone,
        "email": "user@example.com",
        "password": "string",
        "confirmPassword": "string",
        "role": "tutor"
    })
    user_id = user.json().get("data").get("id")
    otp_res = requests.get(f"{DOMAIN + PREFIX}/auth/otp?phone={phone}").json()
    otp_code = otp_res.get("data").get("otp_code")
    token = requests.post(f"{DOMAIN + PREFIX}/auth/verify-otp", json={
        "phoneNumber": phone,
        "otpCode": otp_code
    }).json().get("data").get("accessToken")
    tutor = requests.post(f"{DOMAIN + PREFIX}/users/update/tutor", json={
        "literacy": "college_student",
        "school": "string",
        "subjects": [
            {
                "subject": random_subject(),
                "grade": random_grade(),
                "price": random.randint(100, 999) * 1000
            }
        ],
    }, headers={"Authorization": f"Bearer {token}"}).json()


if __name__ == "__main__":
    for i in range(5):
        new_tutor()
