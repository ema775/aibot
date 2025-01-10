import os

import pytz
from dotenv import load_dotenv

load_dotenv()
_tz: str = os.environ.get("TIMEZONE", "Asia/Tokyo")
TIMEZONE = pytz.timezone(_tz)
