import random

import pandas as pd
import requests

from tests.const import PREFIX

NAME = "Họ và tên "
PHONE = "Số điện thoại liên hệ"
EMAIL = "Email"
LITERARY = "Trình độ học vấn"
SCHOOL = "Trường bạn đang dạy/học"
EXPERIENCES = "Kinh nghiệm dạy học"
SUBJECT = "Môn dạy"
CLASS = "Lớp"

DOMAIN = "https://api.vector.edu.vn"


def generate_tutor_from_file():
    file_path = 'data.xlsx'

    # Read the Excel file
    data_frame = pd.read_excel(file_path, sheet_name='Data')
    subjects_name = [i.get("name") for i in requests.get(f"{DOMAIN + PREFIX}/subjects").json().get("data")]
    print(subjects_name)

    for index, row in data_frame.iterrows():
        phone = row[PHONE]
        full_name = row[NAME]
        email = row[EMAIL]
        subjects = row[SUBJECT]
        try:
            my_class = [i.strip() for i in row[CLASS].split(",") if i.strip()]
        except:
            my_class = []
        try:
            subjects = [i.strip() for i in row[SUBJECT].split(",") if i.strip() in subjects_name]
            if "Anh" in row[SUBJECT]:
                subjects.append("Tiếng Anh")
        except:
            subjects = []
        subjects_payload = []
        for s in subjects:
            for c in my_class:
                while True:
                    num = random.randint(10, 90)
                    if num % 5 == 0:
                        subjects_payload.append({
                            "subject": s,
                            "grade": c,
                            "price": num * 10000
                        })
                        break
            break
        if not subjects_payload:
            continue
        # user = requests.post(f"{DOMAIN + PREFIX}/auth/register", json={
        #     "fullName": full_name.strip(),
        #     "phone": row[PHONE],
        #     "email": email.strip(),
        #     "password": "123456",
        #     "confirmPassword": "123456",
        #     "role": "tutor"
        # })
        # if user.status_code != 200:
        #     print(user.json(), phone)
        #     continue
        # otp_res = requests.get(f"{DOMAIN + PREFIX}/auth/otp?phone={phone}").json()
        # otp_code = otp_res.get("data").get("otp_code")
        # token = requests.post(f"{DOMAIN + PREFIX}/auth/verify-otp", json={
        #     "phoneNumber": phone,
        #     "otpCode": otp_code
        # }).json().get("data").get("accessToken")
        token = requests.post(f"{DOMAIN + PREFIX}/auth/login", json={
            "phoneNumber": phone,
            "password": 123456
        })
        if token.status_code != 200:
            continue
        token = token.json().get("data").get("accessToken")
        tutor = requests.post(f"{DOMAIN + PREFIX}/users/update/tutor", json={
            "literacy": "college_student",
            "subjects": [subjects_payload[0]]
        }, headers={"Authorization": f"Bearer {token}"}).json()
        print(tutor)


# Access row data


if __name__ == "__main__":
    generate_tutor_from_file()
