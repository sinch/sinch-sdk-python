import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
)

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
sinch_number = os.environ.get("SINCH_NUMBER") or "MY_SINCH_NUMBER"
destination_number = (
    os.environ.get("DESTINATION_NUMBER") or "MY_DESTINATION_NUMBER"
)
# Override voices: VOICE_PLAIN=Emma VOICE_SSML=Brian
voice_plain = os.environ.get("VOICE_PLAIN") or "Emma"
voice_ssml = os.environ.get("VOICE_SSML") or "Brian"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# SVAML commands: dial -> on answer play a plain text SAY, a PLAY clip and an
# SSML SAY in sequence -> hangup
commands = CommandsSequenceCreator().dial(
    destination_number,
    from_=sinch_number,
    name="tts-sampler",
    timeout_duration_seconds=30,
    max_duration_seconds=120,
    on_answer=CommandsSequenceCreator()
    .messages(name="sampler", on_finish=Calls.hangup())
    .text(
        f"Hello, this is a plain text message with the {voice_plain} voice.",
        voice_plain,
    )
    .play("https://samplelib.com/mp3/sample-3s.mp3")
    .ssml(
        "<speak>"
        "<prosody rate='slow'>"
        "Now hear an S S M L example. "
        "Your code is <say-as interpret-as='characters'>4837</say-as>."
        "</prosody>"
        "<break time='400ms'/>"
        "Goodbye."
        "</speak>",
        voice_ssml,
    ),
    on_hangup=Calls.hangup(),
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created successfully:\n{response}")
