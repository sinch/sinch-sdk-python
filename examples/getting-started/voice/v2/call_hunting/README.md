# Getting Started: Call Hunting (Voice API v2)

This code is related to [Call Hunting](https://developers.sinch.com/docs/voice-2.0/tutorials/call-hunting).

It calls a customer and tries a list of agents until one answers, then bridges that agent with the customer, using the
Voice API v2 through the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python):

- [sequential_hunt.py](sequential_hunt.py) (Pattern 1) dials the customer and, on answer, tries agent 1, then 2, then 3,
  moving on each time an agent doesn't answer within 20 seconds. The whole flow is sent inline, so no webhook server is
  needed. Start here.
- [configure_service.py](configure_service.py), [start_customer_call.py](start_customer_call.py) and
  [server.py](server.py) (Pattern 2) run the same sequential hunt from a webhook server, which picks the next agent on
  every event and can hunt through any number of agents.
- [sim_ring.py](sim_ring.py) (Pattern 3) rings three agents at once; the first to answer is bridged and the other legs
  are hung up. No webhook server is needed.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/) (for `server.py`)
- [Sinch account](https://dashboard.sinch.com/)
- A Voice API v2 service with a Sinch number associated to it
- [ngrok](https://ngrok.com/docs) (or similar) to expose your local server (for `server.py`)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory (or `export` them in your shell), then set:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_NUMBER`: your Sinch number, in E.164 format (e.g. `+15551234567`). Used as the caller ID on every
     outbound leg
   - `CUSTOMER_NUMBER`: the customer you connect the agent to, in E.164 format
   - `AGENT_NUMBERS`: comma-separated agent numbers, in E.164 format
     (e.g. `+15551110001,+15551110002,+15551110003`). `sequential_hunt.py` and `sim_ring.py` read the first three
     (missing ones repeat the previous agent); `server.py` reads the whole list
   - `SINCH_SERVICE_ID`: the ID of the Voice service that owns your Sinch number (Dashboard → Voice → Services),
     used by `configure_service.py`
   - `CALLBACK_URL`: the public HTTPS base URL of the server, without path, set in step 3 of the webhook-driven hunt
   - `PORT` (optional, default `3000`): the local server port

2. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

Navigate to this directory:
```bash
cd examples/getting-started/voice/v2/call_hunting
```

### Sequential hunt (static SVAML)

```bash
poetry run python sequential_hunt.py
```

The customer number rings; on answer the customer hears "Please hold…" and agent 1 rings. Answer it to be bridged with
the customer, or let it ring out to move on to agent 2, and so on. If all three agents time out, the customer is hung
up. This flow only moves on when an agent times out; busy, rejected or failed agent calls are not handled.

### Sequential hunt (webhook-driven)

1. Start the server:
   ```bash
   poetry run python server.py
   ```
   The server listens on `PORT` (default `3000`) at `POST /voice/events`.

2. Expose the server with ngrok:
   ```bash
   ngrok http 3000
   ```

3. Set `CALLBACK_URL` to the HTTPS URL ngrok prints and point the service at your server:
   ```bash
   poetry run python configure_service.py
   ```
   The service sends its call events to `CALLBACK_URL/voice/events`, with the same URL as `fallbackUrl`.

4. Start the customer call:
   ```bash
   poetry run python start_customer_call.py
   ```
   The dial has no events of its own, so its events go to the server. When the customer answers, the server plays a
   hold message and dials the first agent. When an agent times out, is busy, rejects or fails, it dials the next one;
   when the list runs out, it apologizes and hangs up. You can also call `SINCH_NUMBER` from a phone to start an
   inbound hunt.

### Simultaneous ring

```bash
poetry run python sim_ring.py
```

On customer answer, the three agents ring at the same time. The first agent to answer is bridged with the customer, and
the other two agent calls are hung up.
