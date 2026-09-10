# Getting Started: Handle Inbound PSTN Call and Bridge to an Agent

This directory contains a small server built with the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python)
that handles inbound PSTN calls to your Sinch number using the Voice API v2. When someone dials the number, Sinch
sends a `call.incoming` sinch event to the server, which answers the call, plays a greeting, and bridges the caller to
an agent phone number (`DESTINATION_NUMBER`). This lets you confirm the sinch event is received and the call is
answered and routed correctly.


## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing Voice API v2 service with a Sinch number associated to it, and `callBehavior.type` set to `WEBHOOK`
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials and app settings.

   - Sinch credentials (from the Sinch dashboard, Access Keys):
   ```
   SINCH_PROJECT_ID=your_project_id
   SINCH_KEY_ID=your_key_id
   SINCH_KEY_SECRET=your_key_secret
   ```

   - Voice service and phone numbers (from the Sinch dashboard, Voice -> Services):
   ```
   SINCH_SERVICE_ID=your_voice_service_id
   SINCH_SERVICE_SECRET=your_voice_service_secret # Only visible on the dashboard once the webhook URL has been defined


   SINCH_NUMBER=your_sinch_number
   DESTINATION_NUMBER=your_destination_number
   ```

   - Server port (optional; default 3001):
   ```
   PORT=3001
   ```

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

### Running the server

1. Navigate to this directory:
   ```
   cd examples/getting-started/voice/v2/handle_inbound_pstn_call
   ```


2. Start the server:
   ```bash
   poetry run python server.py
   ```
   Or run it directly:
   ```bash
   python server.py
   ```

The server listens on the port set in your `.env` file (default: 3001).

### Exposing the server with ngrok

To receive Voice V2 API Sinch Events on your machine, expose the server with a tunnel (e.g. ngrok).

```bash
ngrok http 3001
```

You will see output similar to:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:3001
```

Use the **HTTPS** URL when configuring the callback:  
`https://<your-ngrok-host>/VoiceSinchEvent`

Configure this callback URL in the Sinch dashboard for your Voice service.

### Calling your Sinch number

Call the **Sinch number** configured on your Voice service from any phone. The server will answer the call,
play a greeting, and bridge you to `DESTINATION_NUMBER`.