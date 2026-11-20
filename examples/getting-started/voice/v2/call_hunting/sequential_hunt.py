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

# Agent answered: stop the hold message and bridge them in
join_bridge = (
    CommandsSequenceCreator().stop_messages("hold").bridge_call("hunt-bridge")
)

# SVAML commands: dial the customer -> on answer play a hold message, join the
# bridge and dial agent 1 -> on timeout dial agent 2 -> on timeout dial agent 3
# -> on timeout hang up the customer
commands = CommandsSequenceCreator().dial(
    customer_number,
    from_=sinch_number,
    name="customer",
    timeout_duration_seconds=30,
    on_answer=CommandsSequenceCreator()
    .text(
        "Please hold while we connect you to an agent.",
        "Emma_3",
        name="hold",
    )
    .bridge_call("hunt-bridge")
    .dial(
        agent_1,
        from_=sinch_number,
        name="agent-1",
        timeout_duration_seconds=20,
        on_answer=join_bridge,
        on_timeout=Calls.dial(
            agent_2,
            from_=sinch_number,
            name="agent-2",
            timeout_duration_seconds=20,
            on_answer=join_bridge,
            on_timeout=Calls.dial(
                agent_3,
                from_=sinch_number,
                name="agent-3",
                timeout_duration_seconds=20,
                on_answer=join_bridge,
                on_timeout=Calls.hangup("customer"),
            ),
        ),
    ),
    on_hangup=Calls.hangup(),
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created successfully:\n{response}")
