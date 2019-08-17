import logging
import os

# logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))
log = logging.getLogger("debug_logger")
