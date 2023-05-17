from fastapi import FastAPI
from sinch import ClientAsync
from sinch import Client

"""
Run with: uvicorn fast_api_example:app --reload
"""

app = FastAPI()

sinch_client = ClientAsync(
    key_id="KEY_ID",
    key_secret="KEY_SECRET",
    project_id="PROJECT_ID"
)


@app.get("/available_numbers")
async def project():
    numbers = await sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL",
    )
    return {"available_numbers": numbers.available_numbers}
