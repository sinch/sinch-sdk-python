import os
from fastapi import FastAPI
from sinch import SinchClientAsync

"""
Run with: uvicorn fast_api_example:app --reload
"""

app = FastAPI()

sinch_client = SinchClientAsync(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID")
)


@app.get("/available_numbers")
async def project():
    numbers_api_response = await sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL"
    )
    return {"available_numbers": numbers_api_response.available_numbers}
