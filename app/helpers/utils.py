from typing import List


def str_contain_any_substring_in_list(s: str, lst: List[str]) -> bool:
    for tmp in lst:
        if tmp in s:
            return True
    return False
