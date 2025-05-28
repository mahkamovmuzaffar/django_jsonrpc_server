import requests
import logging
import os

logger = logging.getLogger(__name__)


def send(phone: str, message: str) -> dict:
    """
    Public method to send an SMS message.

    Args:
        phone (str): Recipient's phone number in international format (e.g. +998901234567).
        message (str): The SMS message content.

    Returns:
        dict: Response from the SMS provider.
    """
    payload = {
        "phone": phone,
        "message": message
    }
    return fire(payload)


def fire(payload: dict) -> dict:
    """
    Core SMS dispatch method that interacts with the SMS provider API.

    Args:
        payload (dict): Dictionary with 'phone' and 'message' keys.

    Returns:
        dict: Provider response or error.
    """
    try:
        # Replace with actual provider URL and headers
        url = os.getenv("SMS_GATEWAY_URL")
        api_key = os.getenv("SMS_API_KEY")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        logger.info(f"SMS sent to {payload['phone']}: {result}")
        return result

    except Exception as e:
        logger.error(f"SMS sending failed: {e}")
        return {"error": str(e)}
