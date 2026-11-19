# Getting Started: Detect Voicemail & Beeps (AMD) (Voice API v2)

This code is related to [Detect Voicemail & Beeps (AMD)](https://developers.sinch.com/docs/voice-2.0/tutorials/amd).

It uses Answering Machine Detection (AMD) through the Voice API v2, using the
[Sinch Python SDK](https://github.com/sinch/sinch-sdk-python). The `amd` command analyses the call audio once it is
answered and runs a different branch of SVAML commands depending on the verdict:

- `on_human`: a live person picked up. Plays a greeting, then hangs up.
- `on_machine`: a machine answered and is playing its greeting (beep not yet detected). Hangs up silently.
- `on_beep`: a voicemail beep was detected. Leaves a voicemail message, then hangs up.
- `on_unknown`: detection was inconclusive. Hangs up.

There are two scripts:

- [amd_callout.py](amd_callout.py) places an outbound call to `DESTINATION_NUMBER` with `amd` as the first command of
  the dial's `on_answer` event. No webhook server is needed: the matching branch runs on the call itself.
- [server.py](server.py) is a webhook server that, on `call.incoming`, answers the call and runs `amd`. It also logs the
  `call.amd.*` verdict events Sinch posts back, so you can see which branch fired.

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
   - `DESTINATION_NUMBER`: the number to call with `amd_callout.py`, in E.164 format (e.g. `+14155551234`)
   - `PORT` (optional, default `3000`): the local server port

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/answering_machine_detection
   ```

### Inline AMD callout (fastest path)

2. Place the call:
   ```bash
   poetry run python amd_callout.py
   ```
   The script only confirms the call was created; it does not print which AMD branch fired. Answer the phone to hear
   it: a person answering hears the greeting, and a voicemail gets the message right after the beep. To see the
   verdict server-side, use the callback server below.

### Dynamic AMD via a callback server

2. Start the server:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `3000`) at `POST /webhook`.

3. Expose the server with ngrok:
   ```bash
   ngrok http 3000
   ```

4. Set the HTTPS URL ngrok prints plus the `/webhook` path (e.g. `https://<id>.ngrok-free.app/webhook`) as your
   service's webhook in the Sinch dashboard. See the
   [Handle Inbound PSTN Call](../handle_inbound_pstn_call) example to do it with the SDK.

5. Call `SINCH_NUMBER` from any phone. The server logs the AMD verdict:

   | Scenario         | On the answering phone                   | In the server log                    |
   |------------------|------------------------------------------|--------------------------------------|
   | Human answers    | Hears the greeting                       | `call.amd.human`                     |
   | Voicemail        | Beep, then hears the voicemail message   | `call.amd.machine`, `call.amd.beep`  |
   | Machine, no beep | Silence, then hangup                     | `call.amd.machine`                   |
   | Inconclusive     | Hangup                                   | `call.amd.unknown`                   |
