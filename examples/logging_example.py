import logging
from sinch import Sinch
"""
Simple example for implementing custom logging handler.
"""

logger = logging.getLogger("myapp.sinch")
logger.setLevel(logging.DEBUG)

sinch_log_file_handler = logging.FileHandler("/tmp/spam.log")
sinch_log_file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sinch_log_file_handler.setFormatter(formatter)


sinch_client = Sinch(
    key_id="knights",
    key_secret="of Ni!",
    logger=logger
)
