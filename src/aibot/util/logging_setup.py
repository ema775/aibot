import logging

LOG_FILE_NAME = "gptbot.log"
LOG_FORMAT = "%(asctime)s | [%(levelname)s] | [%(filename)s:ln%(lineno)d] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    filename=LOG_FILE_NAME,
    format=LOG_FORMAT,
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
