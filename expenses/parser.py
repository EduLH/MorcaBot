import re
from utils.services.money import normalize_brl_amount

SEPARATORS = r"\s*(?:-|/|\*|,)\s*"


def parse_message(text: str):
    if not text:
        return None

    parts = re.split(SEPARATORS, text)

    if len(parts) != 3:
        return None

    name, category, raw_amount = [p.strip() for p in parts]

    try:
        amount = normalize_brl_amount(raw_amount)
    except ValueError:
        return None

    return {
        "name": name,
        "category": category.lower(),
        "amount": amount,
    }