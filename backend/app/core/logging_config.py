import logging
import sys

def setup_logging():
    logger = logging.getLogger("synexa_api")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [ReqID: %(request_id)s] - %(message)s'
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
