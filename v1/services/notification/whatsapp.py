import requests


def send_whatsapp_message(phone_number: str, message: str) -> dict:
    url = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
