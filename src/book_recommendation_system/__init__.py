"""
This module sets up logging for the Book Recommendation System project.
Logs are saved to a file and also printed to the console.
"""

import logging
import os
import sys

FORMAT = "[%(asctime)s]:%(levelname)s:%(filename)s:%(message)s"
LOG_DIR = "logs"
LOG_FILEPATH = os.path.join(LOG_DIR,"running_logs.log")

os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILEPATH),
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)