# Webhook Handlers for Sinch Python SDK

This directory contains a server application built with [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python)
to process incoming webhooks from Sinch services.

The webhook handlers are organized by service:
- **SMS**: Handlers for SMS webhook events (`sms_api/`)
- **Numbers**: Handlers for Numbers API webhook events (`numbers_api/`)

This directory contains both the webhook handlers and the server application (`server.py`) that uses them.

## Requirements

- [Python 3.9+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- [ngrok](https://ngrok.com/docs)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment Variables**:  
   Rename [.env.example](.env.example) to `.env` in this directory (`examples/webhooks/`), then add your credentials from the Sinch dashboard under the Access Keys section.
   
   - To use [Numbers](https://developers.sinch.com/docs/numbers/), you need to fill the following variables 
   with the values from your Sinch account:
   ``` 
   SINCH_PROJECT_ID=Your Sinch Project ID
   SINCH_KEY_ID=Your Sinch Access Key ID
   SINCH_KEY_SECRET=Your Sinch Key Secret associated to your Sinch Access Key
   ```
   
   - Server Port:  
   Define the port your server will listen to on (default: 3001):
   ```
   SERVER_PORT=3001
   ```
   
   - Controller Settings
     - Numbers controller: Set the webhook secret, which you can retrieve from the [Numbers API](https://developers.sinch.com/docs/numbers/api-reference/numbers/tag/Numbers-Callbacks/), 
       using the `/callbackConfiguration` endpoint:
   ```
   NUMBERS_WEBHOOKS_SECRET=Your Sinch Webhook Secret
   ```

## Usage

### Running the server application

1. Navigate to the webhooks' directory:
```
   cd examples/webhooks
```

2. Install the project dependencies:
``` bash
   poetry install
```

3. Rename `.env.example` to `.env` and update it with your configuration (see above).

4. Start the server:
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

| Service      | Endpoint           |
|--------------|--------------------|
| Numbers      | /NumbersEvent      |
| SMS          | /SmsEvent          |

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
Use the `https` forwarding URL in your callback configuration. For example:
 - Numbers: https://adbd-79-148-170-158.ngrok-free.app/NumbersEvent
 - SMS: https://adbd-79-148-170-158.ngrok-free.app/SmsEvent

Use this value to configure the callback URLs:
 - **Numbers**: Set the `callbackUrl` parameter when renting or updating a number via the API
 - **SMS**: Set the `callback_url` parameter when configuring your SMS service plan via the API
