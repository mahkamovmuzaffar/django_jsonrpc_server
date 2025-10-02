# What is AML?
# AML stands for Anti-Money Laundering. It refers to a set of procedures, laws, and regulations designed to stop
# the practice of generating income through illegal actions. AML systems are used to detect suspicious activities and
# prevent financial crimes.
#
# How AML must work in future transactions:
# - AML checks should be integrated into transaction processing to automatically flag suspicious activities.
# - Transactions should be monitored for unusual patterns, such as large transfers, rapid movement of funds,
# or mismatched user details.
# - Name and card similarity checks (as implemented below) can help identify attempts to disguise identity or use stolen
# credentials.
# - Future AML systems should leverage machine learning and real-time analytics for improved detection and compliance.
# - All flagged transactions should be reviewed and reported according to regulatory requirements.

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


def check_history(transaction, user):
    """
    Check the user's transaction history for suspicious activities.
    TODO: Implement logic to analyze past transactions for patterns such as frequent large transfers, rapid movement of funds, or repeated failed attempts.
    """
    pass


def detect_pattern(transaction):
    """
    Detect unusual patterns in the current transaction.
    TODO: Implement logic to identify anomalies, such as transactions outside normal behavior, or use machine learning for pattern recognition.
    """
    pass


def flag_large_transaction(transaction):
    """
    Flag transactions that exceed a certain threshold amount.
    TODO: Implement logic to compare transaction amount against predefined limits and flag if necessary.
    """
    pass


def verify_user_details(transaction, user):
    """
    Verify that user details match transaction information.
    TODO: Implement logic to cross-check user identity, address, and payment details for consistency and legitimacy.
    """
    pass


def review_flagged_transaction(transaction):
    """
    Review transactions that have been flagged by AML checks.
    TODO: Implement logic for manual or automated review, and prepare reports for compliance officers if required.
    """
    pass
