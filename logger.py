import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter


class LockIdFilter(logging.Filter):
    def __init__(self, lock):
        logging.Filter.__init__(self)
        self._lock = lock

    def filter(self, record):
        if self._lock:
            record.lock_id = str(self._lock.id)
        else:
            record.lock_id = ""
        return True


def create_logger(logfile, lock):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(logfile, maxBytes=1044480, backupCount=10)
    handler.setFormatter(Formatter('''%(asctime)s %(levelname)s %(lock_id)s %(pathname)s:%(lineno)d (%(funcName)s) : %(message)s'''))
    logger.addHandler(handler)
    logger.addFilter(LockIdFilter(lock))
    return logger