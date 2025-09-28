import difflib


def check_name_similarity(name1: str, name2: str) -> float:
    """
    Returns a similarity ratio between two names (0.0 to 1.0).
    Uses SequenceMatcher for fuzzy comparison.
    """
    if not name1 or not name2:
        return 0.0
    name1 = name1.strip().lower()
    name2 = name2.strip().lower()
    return difflib.SequenceMatcher(None, name1, name2).ratio()


def check_card_similarity(card1: str, card2: str) -> float:
    """
    Returns a similarity ratio between two card numbers (0.0 to 1.0).
    Ignores spaces and dashes, compares as strings.
    """
    if not card1 or not card2:
        return 0.0
    card1 = card1.replace(' ', '').replace('-', '')
    card2 = card2.replace(' ', '').replace('-', '')
    return difflib.SequenceMatcher(None, card1, card2).ratio()
