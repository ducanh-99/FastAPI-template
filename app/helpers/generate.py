import random
import string
from datetime import datetime, timedelta


def generate_file(file_name: str):
    return datetime.now().strftime("%d%m%Y%H%M%S") + "_" + file_name


def generate_random_string(length: int = 5):
    letters = string.ascii_letters
    return datetime.now().strftime("%d%m%Y%H%M%S") + ''.join(random.choice(letters) for _ in range(length))


def generate_otp(length=6):
    """
    Generate a random OTP code of the specified length.
    """
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp


def generate_otp_expiration():
    """
    Generate the expiration datetime for an OTP code.
    """
    expiration = datetime.now() + timedelta(minutes=5)  # Adjust the expiration duration as needed
    return expiration
