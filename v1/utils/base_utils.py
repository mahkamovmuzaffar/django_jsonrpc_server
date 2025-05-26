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


def phone_mask(phone_number: str, mask_char: str = 'x', start: int = 6, end: int = -4,
               blank_spaces: bool = True) -> str:
    """
    Mask a phone number by replacing middle digits with a given character.

    Example:
        phone_mask("+99891 234 56 78") -> "+9989x xxx xx xx"

    Args:
        phone_number (str): The input phone number as a string (with or without spaces).
        mask_char (str, optional): Character to use for masking. Default is 'x'.
        start (int, optional): Number of visible characters from the start. Default is 6.
        end (int, optional): Number of visible characters from the end. Default is -4.
        blank_spaces (bool, optional): Whether to return the result in standard phone format with spaces. Default is True.

    Returns:
        str: Masked phone number.
    """
    digits = ''.join(filter(str.isdigit, phone_number))

    if len(digits) < abs(start) + abs(end):
        return phone_number

    masked = digits[:start] + (mask_char * (len(digits) - start + end)) + digits[end:]

    if blank_spaces and len(masked) == 12:
        # Format as +998 XX XXX XX XX
        return f"{masked[:4]}{masked[4:6]} {masked[6:9]} {masked[9:11]} {masked[11:]}"
    else:
        return masked


def phone_country(phone_number: str, country_codes=None):
    """Validate if the phone number is a valid Uzbekistan number"""
    if country_codes is None:
        country_codes = [860]

def short_fullname(full_name: str) -> str:
    """
    Converts a full name into short format like 'Makhkamov M.'.

    Example:
        short_fullname("Muzaffar Makhkamov") -> "Makhkamov M."
        short_fullname("Makhkamov Muzaffar") -> "Makhkamov M."

    Args:
        full_name (str): Full name in any order (first last or last first).

    Returns:
        str: Name in short format.
    """
    parts = full_name.strip().split()
    if len(parts) >= 2:
        last, first = parts[-1], parts[0]
        return f"{last} {first[0]}."
    elif len(parts) == 1:
        return parts[0]
    return ""

# def make_hash(data: str) -> str:
# def encrypt(data: str, key: str) -> str:
# def decrypt(encrypted: str, key: str) -> str:
