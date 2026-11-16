# Getting Started: Respond to an Incoming SMS Message (SMS API)

This code is related to [Receive an SMS Message with the Python SDK](https://developers.sinch.com/docs/sms/getting-started/python/receive-sms-sdk).

It starts a small server that receives incoming SMS messages on your Sinch number and replies to the sender
with the received text (*"You sent: &lt;content of the incoming message&gt;"*), using
the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing SMS service plan (with a Sinch number)
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_SMS_REGION`: the SMS region of your service plan (e.g. `us`, `eu`)
   - `SERVER_PORT`: the port to be used to listen to incoming requests (default: `3001`)

   Optionally, to use a region other than `us` or `eu`, set your SMS service plan credentials (both are required;
   when set, they are used instead of the Access Key credentials for the SMS API):

   - `SINCH_SERVICE_PLAN_ID`: your SMS Service Plan ID
   - `SINCH_API_TOKEN`: the API token associated to your SMS Service Plan

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

### Running the server

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/sms/respond_to_incoming_message
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

To receive SMS Sinch Events on your machine, expose the server with a tunnel (e.g. ngrok):

```bash
ngrok http 3001
```

You will see output similar to:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:3001
```

Use the **HTTPS** URL when configuring the callback:  
`https://<your-ngrok-host>/SmsEvent`

Configure this callback URL in the Sinch dashboard for your SMS service plan.

### Sending an SMS to your Sinch number

Send an SMS from your phone to the **Sinch number** of your service plan. You should receive the reply on your phone.
