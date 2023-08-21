import json
import os
from enum import Enum
from typing import Dict


class Language(Enum):
    VI = "vi"
    EN = "en"


class MultiLanguage:
    lang_data: Dict

    def __init__(self, lang=Language.EN):
        addon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        lang_dir = os.path.join(addon_path, 'i18n')
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        json_path = os.path.join(lang_dir, f"{lang.value}.json")
        self.lang_data = json.load(open(json_path))

    def get(self, code: str, *args, default_value=None):
        data: str = self.lang_data.get(code, default_value)
        if data:
            data = data.format(*args)
        return data
