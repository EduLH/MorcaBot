import re
from utils.services.money import normalize_brl_amount

SEPARATORS = r"\s*(?:-|/|\*|,)\s*"


def parse_message(text: str):
    if not text:
        return None

    # Normaliza separadores estranhos se necessário, mas o regex cuida da divisão
    parts = re.split(SEPARATORS, text.strip())

    # Permite parsing flexível (ex: nome - categoria - valor)
    if len(parts) < 3:
        return None
    
    # Se houver mais partes, assumimos que as primeiras são do nome/categoria
    # mas a especificação pede nome, categoria, valor. Vamos pegar os 3 primeiros
    # ou os 3 últimos? O padrão é: Nome - Categoria - Valor
    # Se o nome tiver hífen? "Pão-de-queijo - Lanche - 5,00" -> 4 partes.
    # O ideal seria splitar apenas 2 vezes.
    
    parts = re.split(SEPARATORS, text.strip(), maxsplit=2)
    
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
