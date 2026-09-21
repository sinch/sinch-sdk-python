from sinch.domains.voice.models.v2.svaml.shared.answer_command import (
    AnswerCommand,
)


def test_answer_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AnswerCommand(command="answer")

    assert model.command == "answer"
