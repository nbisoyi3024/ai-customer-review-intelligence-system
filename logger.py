# logger.py
from loguru import logger
import sys
import os

os.makedirs("logs", exist_ok=True)

# Remove default logger
logger.remove()

# Log messages to terminal
logger.add(
    sys.stdout,
    level="INFO",
    format="{time::YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Log messages to file
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)