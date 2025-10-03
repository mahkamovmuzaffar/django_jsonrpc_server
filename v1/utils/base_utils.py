import hashlib
import hmac
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib


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


def make_hash(data: str, secret: str = "") -> str:
    """
    Generates a SHA256 hash of the given data. If a secret is provided,
    it uses HMAC for added security (e.g. for verifying header signatures).

    Example:
        make_hash("8600123412341234")  -> SHA256 hash
        make_hash("8600123412341234", secret="mysecret") -> HMAC-SHA256

    Args:
        data (str): The input string to hash (e.g., card number).
        secret (str, optional): Optional secret key for HMAC. Default is "".

    Returns:
        str: Hexadecimal string of the hash.
    """
    if secret:
        return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
    else:
        return hashlib.sha256(data.encode()).hexdigest()


def _generate_fernet_key(secret: str) -> bytes:
    """
    Derives a Fernet-compatible key from a plain secret.
    """
    sha256 = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(sha256)


def encrypt(data: str, key: str) -> str:
    """
    Encrypts a string using a key. Returns the encrypted token.

    Args:
        data (str): Plain text to encrypt.
        key (str): Shared secret for encryption.

    Returns:
        str: Encrypted string (Fernet token).
    """
    fernet = Fernet(_generate_fernet_key(key))
    return fernet.encrypt(data.encode()).decode()


def decrypt(encrypted: str, key: str) -> str:
    """
    Decrypts a Fernet token using the same key used for encryption.

    Args:
        encrypted (str): Encrypted token.
        key (str): Shared secret used during encryption.

    Returns:
        str: Decrypted plain text.

    Raises:
        ValueError: If the token is invalid or decryption fails.
    """
    fernet = Fernet(_generate_fernet_key(key))
    try:
        return fernet.decrypt(encrypted.encode()).decode()
    except InvalidToken:
        raise ValueError("Invalid encryption key or token.")


def amount_formatter(amount, currency: str = '', symbol: bool = False, decimals: int = 2, separator: str = ',', decimal_point: str = '.') -> str:
    """
    Formats an amount with thousands separator, decimal places, and currency symbol/code.

    Args:
        amount (float|int|str): The amount to format.
        currency (str): Currency code (e.g., 'USD', 'UZS').
        symbol (bool): If True, append currency code/symbol.
        decimals (int): Number of decimal places.
        separator (str): Thousands separator.
        decimal_point (str): Decimal point character.

    Returns:
        str: Formatted amount string.
    """
    try:
        amt = float(amount)
    except (ValueError, TypeError):
        return str(amount)

    # Format with thousands separator and decimals
    int_part, _, frac_part = f"{amt:.{decimals}f}".partition('.')
    int_part = f"{int(int_part):,}".replace(',', separator)
    formatted = int_part
    if decimals > 0:
        formatted += decimal_point + frac_part
    if symbol and currency:
        formatted += f" {currency.upper()}"
    elif currency:
        formatted += f" {currency.upper()}"
    return formatted
