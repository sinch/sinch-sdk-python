# Getting Started: Mask a Phone Call (Number Masking) (Voice API v2)

This code is related to [Mask a Phone Call (Number Masking)](https://developers.sinch.com/docs/voice-2.0/tutorials/number-masking).

It connects two parties through your Sinch number so neither sees the other's real phone number, using the Voice API
v2 through the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python):

- [validate.py](validate.py) checks the masking SVAML that `server.py` returns with `POST /svaml/validate` in `STRICT`
  mode, using the same rules as a live call (no phone needed).
- [server.py](server.py) is a webhook server that, on `call.incoming`, answers Party A, plays a hold greeting, adds
  Party A to a bridge and dials `DESTINATION_NUMBER` (Party B) from the Sinch number.
- [configure_service.py](configure_service.py) points your Voice service's call events at the server.
- [masked_bridge_call.py](masked_bridge_call.py) triggers a fully outbound masked bridge: it dials Party A and, once
  answered, dials Party B and bridges them. No webhook server is needed.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/) (for `server.py`)
- [Sinch account](https://dashboard.sinch.com/)
- A Voice API v2 service with a Sinch number associated to it
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server (for `server.py`)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_SERVICE_ID`: the ID of the Voice service that owns your Sinch number (Dashboard → Voice → Services),
     used by `configure_service.py`
   - `SINCH_NUMBER`: your Sinch number, in E.164 format (e.g. `+14045001000`). This is the masking number both
     parties see
   - `DESTINATION_NUMBER`: Party B, the number the inbound caller gets bridged to, in E.164 format
     (e.g. `+15551234567`)
   - `PORT` (optional, default `3000`): the local server port
   - `WEBHOOK_URL`: the public URL of the server, set in step 4 below
   - `PARTY_A_NUMBER` / `PARTY_B_NUMBER` (optional): the two parties `masked_bridge_call.py` bridges, in E.164 format.
     They default to `DESTINATION_NUMBER` and `SINCH_NUMBER`, so out of the box one leg dials your Sinch number
     itself. For a real two-party test, set both to phones you can answer

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/number_masking
   ```

2. Smoke-test the SVAML (no phone needed):
   ```bash
   poetry run python validate.py
   ```
   Expected: `is_valid=True`. A successful request means validation ran, not that the payload passed; always read
   `is_valid`.

3. Start the server:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `3000`) at `POST /webhook`.

4. Expose the server with ngrok:
   ```bash
   ngrok http 3000
   ```
   Set `WEBHOOK_URL` to the HTTPS URL ngrok prints plus the `/webhook` path
   (e.g. `https://<id>.ngrok-free.app/webhook`).

5. Point the service at your server:
   ```bash
   poetry run python configure_service.py
   ```
   The same URL is set as `fallbackUrl`: once the primary URL starts returning errors, Sinch switches future requests
   to the fallback.

6. Call `SINCH_NUMBER` from a phone (this is Party A). Party A hears the hold greeting, then `DESTINATION_NUMBER`
   (Party B) rings and sees the Sinch number as the caller ID. Once Party B answers, both parties are bridged. When
   either party hangs up, the other leg drops.

### Trigger a fully outbound masked bridge

To have your platform initiate the call to both parties instead:

```bash
poetry run python masked_bridge_call.py
```

Party A is dialed first; once answered, Party A hears a hold message and Party B is dialed. Both parties see the
Sinch number as the caller ID.
