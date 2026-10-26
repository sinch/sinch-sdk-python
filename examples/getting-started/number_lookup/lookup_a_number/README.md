# Getting Started: Look Up a Number (Number Lookup API)

This code is related to [Look up a number with the Python SDK](https://developers.sinch.com/docs/number-lookup-api-v2/getting-started/python/lookup-number).

It looks up information about a phone number (such as its carrier and line type) through the Number Lookup API, using
the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Sinch account](https://dashboard.sinch.com/)
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key

2. **Lookup parameters**  
   Edit [app.py](app.py) and replace the placeholder value:

   - `PHONE_NUMBER_TO_LOOKUP`: the phone number to look up, in E.164 format (e.g. `+46701234567`)

3. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/number_lookup/lookup_a_number
   ```

2. Run the code:
   ```bash
   poetry run python app.py
   ```
   Or run it directly:
   ```bash
   python app.py
   ```
