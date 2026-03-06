# Getting Started: Receive Mobile-originated (MO) SMS and send Mobile-terminated (MT) reply (Conversation API)


This directory contains a small server built with the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python)
that receives mobile-originated (MO) SMS on your Sinch number and sends a mobile-terminated (MT) SMS back
to the same phone. The reply echoes the incoming text (e.g. *"Your message said: &lt;content of MO&gt;"*) so you can
see that the MO was received and processed.



## Requirements

- [Python 3.9+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing Conversation API app configured for SMS (with a Sinch number)
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

   - Conversation API: set `SINCH_CONVERSATION_REGION` to the same region as the one your app was created in (e.g. `eu`).
   ```
   SINCH_CONVERSATION_REGION=
   ```

   - Server port (optional; default 3001):
   ```
   SERVER_PORT=3001
   ```

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```
   Install the Sinch SDK from the **repository root**: `pip install -e .` (recommended when developing from this repo).  
   Alternatively, install with pip: `flask`, `python-dotenv`, and `sinch` (e.g. from PyPI).

## Usage

### Running the server

1. Navigate to this directory:
   ```
   cd examples/getting-started/conversation/send_handle_incoming_sms
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

To receive webhooks on your machine, expose the server with a tunnel (e.g. ngrok).


```bash
ngrok http 3001
```

You will see output similar to:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:3001
```

Use the **HTTPS** URL when configuring the callback:  
`https://<your-ngrok-host>/ConversationEvent`

Configure this callback URL in the Sinch dashboard for your Conversation API app.

### Sending an SMS to your Sinch number

Send an SMS from your phone to the **Sinch number** linked to your Conversation API app. You should receive the echo reply on your phone.
