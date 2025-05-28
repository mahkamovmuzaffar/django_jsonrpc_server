import os
import requests
import logging
from typing import Dict, Any

FIREBASE_SERVER_KEY = os.getenv("FIREBASE_SERVER_KEY")
FIREBASE_API_URL = "https://fcm.googleapis.com/fcm/send"
logger = logging.getLogger(__name__)


def fire(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core method to send Firebase request.

    Args:
        payload (dict): The full payload to be sent to Firebase.

    Returns:
        dict: Firebase response.
    """
    headers = {
        "Authorization": f"key={FIREBASE_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(FIREBASE_API_URL, json=payload, headers=headers)
        response_data = response.json()
        logger.info(f"Firebase response: {response_data}")
        return response_data
    except Exception as e:
        logger.error(f"Firebase request failed: {e}")
        return {"error": str(e)}


def send_notification(token: str, title: str, body: str, data: dict = None) -> Dict[str, Any]:
    """
    Prepares and sends notification to a single device.

    Args:
        token (str): Firebase device token.
        title (str): Notification title.
        body (str): Notification body.
        data (dict): Optional payload data.

    Returns:
        dict: Firebase response.
    """
    payload = {
        "to": token,
        "notification": {"title": title, "body": body},
        "data": data or {}
    }
    return fire(payload)


def send_bulk_notification(tokens: list[str], title: str, body: str, data: dict = None) -> Dict[str, Any]:
    """
    Sends notification to multiple device tokens.

    Args:
        tokens (list): List of Firebase tokens.
        title (str): Notification title.
        body (str): Notification body.
        data (dict): Optional payload data.

    Returns:
        dict: Firebase response.
    """
    payload = {
        "registration_ids": tokens,
        "notification": {"title": title, "body": body},
        "data": data or {}
    }
    return fire(payload)
