import re
from datetime import datetime

from app.helpers.regex import VALIDATE_EMAIl_REGEX, VALIDATE_PHONE_NUMBER_1_15_REGEX


def is_valid_phone_number(phone_number: str):
    pattern = re.compile(VALIDATE_PHONE_NUMBER_1_15_REGEX)
    return pattern.match(phone_number)


def is_valid_email(email: str):
    pattern = re.compile(VALIDATE_EMAIl_REGEX)
    return pattern.fullmatch(email)


def is_valid_date_format_dd_mm_yyyy(date_string: str):
    try:
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except:
        return False
