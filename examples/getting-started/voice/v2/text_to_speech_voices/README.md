# Getting Started: Text-to-Speech & Available Voices (Voice API v2)

This code is related to [Text-to-Speech & Available Voices](https://developers.sinch.com/docs/voice-2.0/tutorials/tts-voices).

It synthesizes speech on the fly inside a call through the Voice API v2, using the
[Sinch Python SDK](https://github.com/sinch/sinch-sdk-python). No audio files to host and no separate TTS service:

- [tts_call.py](tts_call.py) calls `DESTINATION_NUMBER` and, when answered, speaks one line of text-to-speech in the
  Emma voice, then hangs up.
- [tts_sampler.py](tts_sampler.py) calls `DESTINATION_NUMBER` and, when answered, plays three items in sequence: a
  plain text message, a short audio clip, and an SSML message (slow prosody, a code spelled character by character and
  a pause). Then it hangs up.

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
   - `VOICE_PLAIN` / `VOICE_SSML` (optional, default `Emma` / `Brian`): the voices `tts_sampler.py` uses for the plain
     text and SSML messages, to compare options

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/voice/v2/text_to_speech_voices
   ```

2. Place a single text-to-speech call:
   ```bash
   poetry run python tts_call.py
   ```

3. Place the full sampler call (plain text, audio clip and SSML):
   ```bash
   poetry run python tts_sampler.py
   ```
