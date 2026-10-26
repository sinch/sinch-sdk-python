# Getting Started: Send a Text Message (Conversation API)

This code is related to [Send a Text Message with the Python SDK](https://developers.sinch.com/docs/conversation/getting-started#4-send-the-message).

It sends an SMS text message to a recipient phone number through the Conversation API, using
the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing Conversation API app configured for SMS (with a Sinch number)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_CONVERSATION_REGION`: the region where your Conversation App is configured (e.g. `us`, `eu`)

2. **Message parameters**  
   Edit [app.py](app.py) and replace the placeholder values:

   - `CONVERSATION_APPLICATION_ID`: the ID of your Conversation API app
   - `SINCH_VIRTUAL_PHONE_NUMBER`: the Sinch number used as SMS sender
   - `RECIPIENT_PHONE_NUMBER`: the phone number of the recipient, in E.164 format (e.g. `+46701234567`)

3. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/conversation/send_text_message
   ```

2. Run the code:
   ```bash
   poetry run python app.py
   ```
   Or run it directly:
   ```bash
   python app.py
   ```
