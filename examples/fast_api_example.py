from fastapi import FastAPI
from sinch import ClientAsync

"""
Run with: uvicorn fast_api_example:app --reload
"""

app = FastAPI()

sinch_client = ClientAsync(
    key_id="Spodek",
    key_secret="wKatowicach"
)


@app.get("/available_numbers")
async def project():
    numbers = await sinch_client.numbers.list_available_numbers(
        region_code="US",
        number_type="LOCAL",
        project_id="e15b2651-daac-4ccb-92e8-e3066d1d033b"
    )
    return {"available_numbers": numbers.available_numbers}
