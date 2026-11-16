# Getting Started: Search for Virtual Numbers (Numbers API)

This code is related to [Search for virtual numbers](https://developers.sinch.com/docs/numbers/getting-started).

It searches for virtual numbers available to rent (`LOCAL` numbers in the `US` region) through the Numbers API, using
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

2. **Search parameters** (optional)  
   Edit [app.py](app.py) to change the search criteria:

   - `region_code`: ISO 3166-1 alpha-2 country code (e.g. `US`, `GB`, `SE`)
   - `number_type`: the type of number (`MOBILE`, `LOCAL` or `TOLL_FREE`)

3. **Install dependencies**  
   From this directory:
   ```bash
   poetry install
   ```

## Usage

1. Navigate to this directory:
   ```bash
   cd examples/getting-started/numbers/search_available_number
   ```

2. Run the code:
   ```bash
   poetry run python app.py
   ```
   Or run it directly:
   ```bash
   python app.py
   ```
