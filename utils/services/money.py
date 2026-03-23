from decimal import Decimal, InvalidOperation


def normalize_brl_amount(raw: str) -> Decimal:
    """
    Converte:
    1.000,50 -> 1000.50
    59 -> 59.00
    """
    raw = raw.strip()

    raw = raw.replace(".", "")
    raw = raw.replace(",", ".")

    try:
        value = Decimal(raw)
    except InvalidOperation:
        raise ValueError("Invalid amount")

    return value.quantize(Decimal("0.01"))

def format_brl(amount: Decimal) -> str:
    return f"R$ {amount:.2f}".replace(".", ",")