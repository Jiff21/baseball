import argparse
import logging
import os

# logging.basicConfig(level=os.environ.get("LOGLEVEL", "ERROR"))
# log = logging.getLogger("debug_logger")


parser = argparse.ArgumentParser()

parser.add_argument( '-log',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level. Example --loglevel debug, default=warning' )

parser.add_argument( '-league',
                     '--league',
                     default='phb',
                     help='Provide league name. Example --league phb, default=igtbtk' )

args = parser.parse_args()
logging.basicConfig( level=args.loglevel.upper() )
log = logging.getLogger("log")
