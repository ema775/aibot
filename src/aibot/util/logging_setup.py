import inspect
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging(log_level: int) -> None:
    """Set up the logging configuration.

    Parameters
    ----------
    log_level : int, optional
        The logging level (e.g., logging.DEBUG, logging.INFO).

    """
    caller_frame = inspect.stack()[1]
    caller_file = Path(caller_frame.filename).stem + ".log"

    logging.basicConfig(
        level=log_level,  # ログレベルを引数で設定
        format="%(asctime)s | [%(levelname)s] | [%(filename)s:ln%(lineno)d] %(message)s",
        handlers=[
            logging.FileHandler(caller_file),  # ファイルにログを出力
            logging.StreamHandler(),  # コンソールにログを出力
        ],
    )
