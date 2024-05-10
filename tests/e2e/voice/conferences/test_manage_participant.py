from sinch.domains.voice.models.conferences.responses import ManageParticipantVoiceConferenceResponse
from sinch.domains.voice.enums import ConferenceCommand


def test_manage_conference_conference(
    sinch_client_sync,
    conference_id,
    conference_call_id
):
    manage_participant_response = sinch_client_sync.voice.conferences.manage_participant(
        conference_id=conference_id,
        call_id=conference_call_id,
        command=ConferenceCommand.MUTE.value
    )
    assert isinstance(manage_participant_response, ManageParticipantVoiceConferenceResponse)


async def test_manage_conference_conference_async(
    sinch_client_async,
    conference_id,
    conference_call_id
):
    manage_participant_response = await sinch_client_async.voice.conferences.manage_participant(
        conference_id=conference_id,
        call_id=conference_call_id,
        command=ConferenceCommand.MUTE.value
    )
    assert isinstance(manage_participant_response, ManageParticipantVoiceConferenceResponse)

