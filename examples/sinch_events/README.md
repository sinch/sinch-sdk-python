# Sinch Events Handlers for Sinch Python SDK

This directory contains a server application built with [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python)
to process incoming webhooks from Sinch services.

The Sinch Events Handlers are organized by service:
- **SMS**: Handlers for SMS events (`sms_api/`)
- **Numbers**: Handlers for Numbers API events (`numbers_api/`)
- **Conversation**: Handlers for Conversation API events (`conversation_api/`)

This directory contains both the Event handlers and the server application (`server.py`) that uses them.

## Requirements

- [Python 3.9+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- [ngrok](https://ngrok.com/docs)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment Variables**:  
   Rename [.env.example](.env.example) to `.env` in this directory (`examples/sinch_events/`), then add your credentials from the Sinch dashboard under the Access Keys section.
   
   - Server Port:  
   Define the port your server will listen to on (default: 3001):
   ```
   SERVER_PORT=3001
   ```
   
   - Controller Settings
    - Numbers controller: Set the `numbers` Sinch Event secret. You can retrieve it using the `/event_destination` endpoint (see SDK implementation: [event_destinations_apis.py](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/numbers/api/v1/event_destinations_apis.py); for additional details, refer to the [Numbers API callbacks documentation](https://developers.sinch.com/docs/numbers/api-reference/numbers/tag/Numbers-Callbacks/)):
   ```
   NUMBERS_SINCH_EVENT_SECRET=Your Sinch Numbers Sinch Event Secret
   ```
     - SMS controller: To configure the `sms` Sinch Event secret, contact your account manager to enable authentication for SMS callbacks. For more details, refer to
       [SMS API](https://developers.sinch.com/docs/sms/api-reference/sms/tag/Webhooks/#tag/Webhooks/section/Callbacks), 

   ```
   SMS_SINCH_EVENT_SECRET=Your Sinch SMS Sinch Event Secret
   ```
     - Conversation controller: Set the webhook secret you configured when creating the webhook (see [Conversation API callbacks](https://developers.sinch.com/docs/conversation/callbacks)):
   ```
   CONVERSATION_WEBHOOKS_SECRET=Your Conversation Webhook Secret
   ```

## Usage

### Running the server application

1. Navigate to the examples events directory:
```
   cd examples/sinch_events
```

2. Install the project dependencies:
``` bash
   poetry install
```

3. Start the server:
``` bash
   poetry run python server.py
```
Or run it directly:
``` bash
   python server.py
```

The server will start on the port specified in your `.env` file (default: 3001).

### Endpoints

The server exposes the following endpoints:

| Service      | Endpoint             |
|--------------|----------------------|
| Numbers      | /NumbersEvent        |
| SMS          | /SmsEvent            |
| Conversation | /ConversationEvent   |

## Using ngrok to expose your local server

To test your webhook locally, you can tunnel requests to your local server using ngrok.

*Note: The default port is `3001`, but this can be changed (see [Server port](#Configuration))*

```bash
  ngrok http 3001
```

You'll see output similar to this:
```
ngrok                                                                           (Ctrl+C to quit)
...
Forwarding                    https://adbd-79-148-170-158.ngrok-free.app -> http://localhost:3001
```
Use the `https` forwarding URL in your event destination configuration. For example:
 - Numbers: https://adbd-79-148-170-158.ngrok-free.app/NumbersEvent
 - SMS: https://adbd-79-148-170-158.ngrok-free.app/SmsEvent
 - Conversation: https://adbd-79-148-170-158.ngrok-free.app/ConversationEvent

Use this value to configure the Sinch Events URLs:
- **Numbers**: Set the `event_destination_target` parameter when renting or updating a number via the SDK (e.g., `available_numbers_apis` rent/update flow: [rent](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/numbers/api/v1/available_numbers_apis.py#L69), [update](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/numbers/api/v1/available_numbers_apis.py#L89)); you can also update active numbers via `active_numbers_apis` ([example](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/numbers/api/v1/active_numbers_apis.py#L64)).
- **SMS**: Set the `event_destination_target` parameter when configuring your SMS service plan via the SDK (see `batches_apis` examples: [send/dry-run callbacks](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/sms/api/v1/batches_apis.py#L146), [update/replace callbacks](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/sms/api/v1/batches_apis.py#L491)); you can also set it directly via the SMS API.
- **Conversation**: Set the `callback_url` parameter when sending a message via the SDK (see `messages_apis` example: [send_text_message](https://github.com/sinch/sinch-sdk-python/blob/v2.0/sinch/domains/conversation/api/v1/messages_apis.py#L420)).

You can also set these Sinch Events URLs in the Sinch dashboard; the API parameters above override the default values configured there.

> **Note**: If you have set a Sinch Event secret (e.g., `SMS_SINCH_EVENT_SECRET`), the Sinch Event URL must be configured in the Sinch dashboard
> and cannot be overridden via API parameters. The Sinch Event secret is used to validate incoming webhook requests,
> and the URL associated with it must be set in the dashboard.
