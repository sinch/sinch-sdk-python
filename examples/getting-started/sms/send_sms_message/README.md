# Getting Started: Send an SMS Message (SMS API)

This code is related to [Send an SMS Message with the Python SDK](https://developers.sinch.com/docs/sms/getting-started/python/send-sms-sdk).

It sends an SMS message to a recipient phone number through the SMS API, using
the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing SMS service plan (with a Sinch number)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key
   - `SINCH_SMS_REGION`: the SMS region of your service plan (e.g. `us`, `eu`)

   Optionally, to use a region other than `us` or `eu`, set your SMS service plan credentials (both are required;
   when set, they are used instead of the Access Key credentials for the SMS API):

   - `SINCH_SERVICE_PLAN_ID`: your SMS Service Plan ID
   - `SINCH_API_TOKEN`: the API token associated to your SMS Service Plan

2. **Message parameters**  
   Edit [app.py](app.py) and replace the placeholder values:

   - `SENDER_NUMBER`: the Sinch number used as SMS sender
   - `RECIPIENT_PHONE_NUMBER`: the phone number of the recipient, in E.164 format (e.g. `+46701234567`)

3. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/sms/send_sms_message
   ```

2. Run the code:
   ```bash
   poetry run python app.py
   ```
   Or run it directly:
   ```bash
   python app.py
   ```
