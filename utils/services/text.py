from difflib import get_close_matches


def get_closest_match(input_value: str, options: list[str], cutoff=0.6):
    matches = get_close_matches(
        input_value.lower(),
        [o.lower() for o in options],
        n=1,
        cutoff=cutoff,
    )
    return matches[0] if matches else None