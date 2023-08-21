from datetime import datetime, date
from typing import List

from sqlalchemy import inspect

from app.core.config import settings
from app.migrations.models import BareBaseModel


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def convert_list_dict_to_dict(array: List[dict], key: str):
    new_dict = {}
    for item in array:
        name = item[key]
        new_dict[name] = item
    return new_dict


def convert_models_to_dict(array: List[BareBaseModel]):
    new_array = []
    for item in array:
        new_array.append(item.__dict__)
    return new_array


def convert_add_prefix_dictionary(my_dict: dict, k: str):
    res = {k + str(key): val for key, val in my_dict.items()}

    return res


def convert_datetime_to_json_decode(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def convert_date_to_json_decode(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def render_download_image(s: str):
    if s is None:
        return None
    return settings.DOMAIN + "api/download/minio/" + s
