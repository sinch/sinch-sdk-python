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
customer_number = os.environ.get("CUSTOMER_NUMBER") or "MY_CUSTOMER_NUMBER"
agent_numbers = os.environ.get("AGENT_NUMBERS") or "MY_AGENT_NUMBER"

# Read the first three agents; missing ones repeat the previous agent
agents = [n.strip() for n in agent_numbers.split(",") if n.strip()]
agent_1 = agents[0]
agent_2 = agents[1] if len(agents) > 1 else agent_1
agent_3 = agents[2] if len(agents) > 2 else agent_2

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)


def ring_agent(number, name, others):
    # First agent to answer stops the hold message, hangs up the other agent
    # legs and joins the bridge
    return Calls.dial(
        number,
        from_=sinch_number,
        name=name,
        timeout_duration_seconds=25,
        on_answer=CommandsSequenceCreator()
        .stop_messages("hold")
        .hangup(others[0])
        .hangup(others[1])
        .bridge_call("hunt-bridge"),
    )


# SVAML commands: dial the customer -> on answer play a hold message and ring
# the three agents at once (dial is non-blocking) -> first to answer wins
commands = CommandsSequenceCreator().dial(
    customer_number,
    from_=sinch_number,
    name="customer",
    timeout_duration_seconds=30,
    on_answer=CommandsSequenceCreator()
    .text("Connecting you now.", "Emma_3", name="hold")
    .command(ring_agent(agent_1, "agent-A", ["agent-B", "agent-C"]))
    .command(ring_agent(agent_2, "agent-B", ["agent-A", "agent-C"]))
    .command(ring_agent(agent_3, "agent-C", ["agent-A", "agent-B"])),
    on_hangup=Calls.hangup(),
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created successfully:\n{response}")
