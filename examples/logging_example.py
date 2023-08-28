import os
import logging
from sinch import Client
"""
Custom logger configuration example.
"""

logger = logging.getLogger("myapp.sinch")
logger.setLevel(logging.DEBUG)

sinch_log_file_handler = logging.FileHandler("/tmp/spam.log")
sinch_log_file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sinch_log_file_handler.setFormatter(formatter)


sinch_client = Client(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID"),
    logger=logger
)
