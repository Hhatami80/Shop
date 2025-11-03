# lets you search for pattern in text. Patterns like does the text have digits or symbols
import re


def is_strong_password(password: str) -> (bool, str):
    """
    Conditions:
        - Must Contain uppercase, lowercase, digit and symbol
        - Must have at least 8 characters
    """
    if len(password) < 8:
        return False, "پسوورد باید حداقل شامل 8 حرف باشد"
    # [A-Z] looks for uppercase
    if not re.search(r'[A-Z]', password):
        return False, "پسوورد باید شامل حداقل یک حرف بزرگ باشد"
    # [a-z] looks for lowercase
    if not re.search(r'[a-z]', password):
        return False, "پسوورد باید شامل حداقل یک حرف کوچک باشد"
    # looks for digits (0-9)
    if not re.search(r'\d', password):
        return False, "پسوورد باید حداقل شامل یک عدد باشد"

    # ^ at the beginning of a set = "NOT".
    # \w = any "word character" (letters, digits, underscore).
    # \s = whitespace (spaces, tabs, newlines).
    # So [^ \w\s] = any character that is NOT a letter, digit, underscore, or space.

    if not re.search(r'[^\w\s]', password):
        return False, "پسوورد باید حداقل شامل یک نماد مخصوص باشد"

    return True, "پسوورد قوی است"