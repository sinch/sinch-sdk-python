import os

import requests
from dotenv import load_dotenv

load_dotenv()

port = os.environ.get("PORT") or "3000"

# A simulated call.incoming event, with every field Sinch sends
resp = requests.post(
    f"http://localhost:{port}/voice/events",
    json={
        "event": "call.incoming",
        "call": {
            "callId": "test",
            "projectId": "test",
            "serviceId": "test",
            "sessionId": "test",
            "direction": "INBOUND",
            "originationType": "PHONE",
            "callType": "PHONE",
            "from": {"type": "PHONE", "phone": {"number": "+15551112222"}},
            "to": {"type": "PHONE", "phone": {"number": "+14045001000"}},
            "callResult": "INITIATED",
            "startTime": "2025-06-01T10:00:00Z",
            "callRate": {"currencyCode": "USD", "amount": "0.0000"},
            "callResourceUrl": "https://voice.api.sinch.com",
        },
    },
)
resp.raise_for_status()
print(resp.status_code, resp.json())
