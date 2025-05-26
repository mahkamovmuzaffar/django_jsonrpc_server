def card_mask(card_number: str, mask_char: str = 'x', start: int = 6, end: int = -4) -> str:
    """
    Mask a card number with the given character, preserving specified start and end digits.

    Example: card_mask("8600123456781234") -> "860012xxxxxx1234"
    """
    digits = card_number.replace(' ', '')
    if len(digits) < abs(start) + abs(end):
        return card_number  # or raise ValueError

    return (
            digits[:start] +
            (mask_char * (len(digits) - start + end)) +
            digits[end:]
    )


def phone_mask(phone_number: str) -> str:
    """Returns masked phone number like +9989x xxx xx xx"""
    pass

def phone_country(phone_number: str, country_codes=None) :
     """Validate if the phone number is a valid Uzbekistan number"""
     if country_codes is None:
         country_codes = [860]

# def short_fullname(full_name: str) -> str:
#     """Returns format like 'Makhkamov M.' """

# def make_hash(data: str) -> str:
# def encrypt(data: str, key: str) -> str:
# def decrypt(encrypted: str, key: str) -> str:
