# Getting Started: Rent the First Available Number (Numbers API)

This code is related to [Rent the first available number](https://developers.sinch.com/docs/numbers/getting-started).

It rents the first available `LOCAL` number in the `US` region and associates it with your SMS service plan,
in a single call to the Numbers API, using the [Sinch Python SDK](https://github.com/sinch/sinch-sdk-python).

> **Note:** running this code rents a real virtual number, which is charged to your Sinch account.

## Requirements

- [Python 3.10+](https://www.python.org/)
- [Sinch account](https://dashboard.sinch.com/)
- An existing SMS service plan
- [Poetry](https://python-poetry.org/)

## Configuration

1. **Environment variables**  
   Copy [.env.example](.env.example) to `.env` in this directory, then set your credentials:

   - `SINCH_PROJECT_ID`: your Sinch Project ID
   - `SINCH_KEY_ID`: your Sinch Access Key ID
   - `SINCH_KEY_SECRET`: your Sinch Key Secret associated to your Sinch Access Key

2. **Rent parameters**  
   Edit [app.py](app.py) and replace the placeholder value:

   - `MY_SERVICE_PLAN_ID`: the ID of the SMS service plan to associate with the rented number

3. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/numbers/rent_first_available_number
   ```

2. Run the code:
   ```bash
   poetry run python app.py
   ```
   Or run it directly:
   ```bash
   python app.py
   ```
