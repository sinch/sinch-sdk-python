# Getting Started: Make an Outbound Text-to-Speech Call (Voice API v2)

This code is related to [Make an outbound call with text-to-speech](https://developers.sinch.com/docs/voice-2.0/tutorials/outbound-tts).

It places a call to a recipient phone number through the Voice API v2, using
the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python). When the call is answered, it plays an audio file
followed by a text-to-speech message, then hangs up.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Sinch account](https://dashboard.sinch.com/)
- A Sinch virtual number assigned to a Voice service
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_NUMBER`: the Sinch number used as caller ID, in E.164 format (e.g. `+14045001000`)
   - `DESTINATION_NUMBER`: the phone number to call, in E.164 format (e.g. `+14155551234`)

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/outbound_text_to_speech
   ```

2. Run the code:
   ```bash
   poetry run python callout.py
   ```
   Or run it directly:
   ```bash
   python callout.py
   ```
