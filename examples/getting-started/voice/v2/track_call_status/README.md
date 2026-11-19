# Getting Started: Track Call Status (Voice API v2)

This code is related to [Track Call Status](https://developers.sinch.com/docs/voice-2.0/tutorials/track-call-status).

It shows the two ways to know what is happening with a call in the Voice API v2, using the
[Sinch Python SDK](https://github.com/sinch/sinch-sdk-python):

- **Events (recommended for real-time).** Sinch pushes lifecycle events (`call.incoming`, `call.answered`,
  `call.hangup`, ...) to your server as they happen:
  - [server.py](server.py) is a minimal event receiver that logs every event with its CloudEvents headers. It answers
    `call.incoming` with a short goodbye and acknowledges every other event with no commands.
- **Polling (fallback / on-demand).** Read the platform's authoritative state when you cannot run a public endpoint, for
  reconciliation and reporting, or to recover events you may have missed:
  - [track_session.py](track_session.py) starts an outbound call, then polls its session until it reaches `COMPLETED`,
    with a bounded number of attempts and backoff, and prints the result of each call leg.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/) (for `server.py`)
- [Sinch account](https://dashboard.sinch.com/)
- A Sinch virtual number assigned to a Voice service
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server (for `server.py`)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_NUMBER`: your Sinch number, in E.164 format (e.g. `+14045001000`)
   - `DESTINATION_NUMBER`: the number to call with `track_session.py`, in E.164 format (e.g. `+14155551234`)
   - `PORT` (optional, default `3000`): the local server port

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/track_call_status
   ```

### Track a call in real time with events

2. Start the receiver:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `3000`) at `POST /voice/events`.

3. Expose the server with ngrok:
   ```bash
   ngrok http 3000
   ```

4. Set the HTTPS URL ngrok prints plus the `/voice/events` path (e.g. `https://<id>.ngrok-free.app/voice/events`) as
   your service's webhook in the Sinch dashboard. See the [Handle Inbound PSTN Call](../handle_inbound_pstn_call)
   example to do it with the SDK.

5. Start an outbound call (e.g. with `track_session.py`), or call `SINCH_NUMBER` from any phone. The server logs each
   event as it arrives. When `call.hangup` arrives with a final `call_result`, the call is done.

### Poll call state

2. Start a call and poll it to completion:
   ```bash
   poetry run python track_session.py
   ```
   A healthy outbound call walks the session through `QUEUED` → `IN_PROGRESS` → `COMPLETED`, then the script prints
   each call leg, e.g. `call_result=COMPLETED call_reason=CALLEE_HANGUP`. If nobody answers, the leg shows
   `call_result=NO_ANSWER` and the session still reaches `COMPLETED`.

