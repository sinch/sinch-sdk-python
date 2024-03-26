import os
import logging
from sinch import SinchClient
"""
Custom logger configuration example.
"""

logger = logging.getLogger("myapp.sinch")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("/tmp/test_python_logging.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

sinch_client = SinchClient(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID"),
    logger=logger
)


def main():
    available_numbers_response = sinch_client.numbers.available.list(
        region_code="US",
        number_type="LOCAL"
    )
    print(available_numbers_response)


if __name__ == "__main__":
    main()
