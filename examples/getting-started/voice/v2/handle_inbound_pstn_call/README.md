# Getting Started: Handle Inbound PSTN Calls (Voice API v2)

This code is related to [Handle Inbound PSTN Calls](https://developers.sinch.com/docs/voice-2.0/tutorials/inbound-pstn).

It uses the Voice API v2 through the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python):

- [validate.py](validate.py) checks the SVAML you intend to return with `POST /svaml/validate`, using the same rules
  as a live call (no phone needed).
- [server.py](server.py) is a webhook server that, on `call.incoming`, answers the call, plays a greeting, and bridges
  the caller to an agent phone number (`DESTINATION_NUMBER`).
- [smoke_test.py](smoke_test.py) sends a simulated `call.incoming` event to the local server.
- [configure_service.py](configure_service.py) points your Voice service's call events at the server.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Sinch account](https://dashboard.sinch.com/)
- A Voice API v2 service with a Sinch number associated to it
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_SERVICE_ID`: the ID of the Voice service that owns your Sinch number (Dashboard → Voice → Services),
     used by `configure_service.py`
   - `SINCH_NUMBER`: your Sinch number, in E.164 format (e.g. `+14045001000`)
   - `DESTINATION_NUMBER`: the agent number the call bridges to, in E.164 format (e.g. `+14155559876`)
   - `PORT` (optional, default `3000`): the local server port
   - `WEBHOOK_URL`: the public URL of the server, set in step 5 below

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/handle_inbound_pstn_call
   ```

2. Smoke-test your SVAML (no phone needed):
   ```bash
   poetry run python validate.py
   ```
   Expected: `is_valid=True`. A successful request means validation ran, not that the payload passed; always read
   `is_valid`.

3. Start the server:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `3000`) at `POST /voice/events`.

4. In another terminal, smoke-test the server locally. You should get back the SVAML JSON and see a log line on the
   server:
   ```bash
   poetry run python smoke_test.py
   ```

5. Expose the server with ngrok:
   ```bash
   ngrok http 3000
   ```
   Set `WEBHOOK_URL` to the HTTPS URL ngrok prints plus the `/voice/events` path
   (e.g. `https://<id>.ngrok-free.app/voice/events`).

6. Point the service at your server:
   ```bash
   poetry run python configure_service.py
   ```
   The same URL is set as `fallbackUrl`: once the primary URL starts returning errors, Sinch switches future requests
   to the fallback.

7. Call `SINCH_NUMBER` from any phone. You should hear the greeting, then `DESTINATION_NUMBER` rings. Answer it and the
   two legs are bridged. If the agent doesn't answer within 30 seconds the call hangs up.
