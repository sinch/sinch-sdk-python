# Getting Started: Record Calls & Transcribe Audio (Voice API v2)

This code is related to [Record Calls & Transcribe Audio](https://developers.sinch.com/docs/voice-2.0/tutorials/recording-and-transcription).

It records calls through the Voice API v2, using the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).
Sinch uploads each recording (MP3, both parties) straight to your own cloud storage bucket as soon as it stops, together
with a JSON transcript file:

- [trigger_call.py](trigger_call.py) places an outbound call to `DESTINATION_NUMBER`. When it is answered, it starts
  recording and plays a recording notice. When the call ends, it stops the recording. No webhook server is needed.
- [server.py](server.py) is a webhook server that, on `call.incoming`, answers the call, starts recording and plays a
  recording notice.

The storage provider is inferred from the `STORAGE_DESTINATION_URL` scheme: `s3://` → AWS, `gs://` → GCP, anything
else → Azure.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/) (for `server.py`)
- [Sinch account](https://dashboard.sinch.com/)
- A Sinch virtual number assigned to a Voice service
- A storage bucket and write-scoped credentials.
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server (for `server.py`)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_NUMBER`: your Sinch number, in E.164 format (e.g. `+14045001000`)
   - `DESTINATION_NUMBER`: the number to call with `trigger_call.py`, in E.164 format (e.g. `+14155551234`)
   - `STORAGE_DESTINATION_URL`: the bucket path where recordings are uploaded (e.g. `s3://my-voice-recordings/recordings/`)
   - `STORAGE_CREDENTIALS`: the storage credentials. For AWS, exactly `ACCESS_KEY:SECRET_KEY:REGION`
   - `PORT` (optional, default `8081`): the local server port

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/recording_and_transcription
   ```

### Record an outbound call (fastest path)

2. Place the call:
   ```bash
   poetry run python trigger_call.py
   ```
   Answer the call and hang up. A few seconds later an `.mp3` file and its JSON transcript appear in
   `STORAGE_DESTINATION_URL`. If nothing shows up in the bucket, the credentials or bucket permissions are almost
   certainly wrong.

### Record inbound calls

2. Start the server:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `8081`) at `POST /webhook`.

3. Expose the server with ngrok:
   ```bash
   ngrok http 8081
   ```

4. Set the HTTPS URL ngrok prints plus the `/webhook` path (e.g. `https://<id>.ngrok-free.app/webhook`) as your
   service's webhook in the Sinch dashboard. See the
   [Handle Inbound PSTN Call](../handle_inbound_pstn_call) example to do it with the SDK.

5. Call `SINCH_NUMBER` from any phone. You should hear the recording notice; the recording is uploaded once the call
   ends.
