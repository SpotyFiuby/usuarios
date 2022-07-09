import requests
from fastapi import HTTPException

NOTIFICATION_URL = "https://exp.host/--/api/v2/push/send"


def sendNotification(
    tokenNotification, title, body, userAdresseeId, userAddresseeUsername
):
    """Send a notification to a user.
    https://exp.host/--/api/v2/push/send with the following HTTP headers:
    host: exp.host
    accept: application/json
    accept-encoding: gzip, deflate
    content-type: application/json

    This is a "hello world" push notification using cURL that you can send using your CLI (replace the placeholder push token with your own):
    curl -H "Content-Type: application/json" -X POST "https://exp.host/--/api/v2/push/send" -d '{
      "to": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]",
      "title":"hello",
      "body": "world"
    }'
    """

    headers = {
        "host": "exp.host",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }

    data = {
        "to": tokenNotification,
        "title": title,
        "body": body,
        "userAdresseeId": userAdresseeId,
        "userAdresseeUsername": userAddresseeUsername,
    }

    response = requests.post(NOTIFICATION_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error sending notification: {response.text}",
        )
    return response.json()
