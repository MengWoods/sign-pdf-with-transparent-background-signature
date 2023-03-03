#!/usr/bin/python3
# Config parser
import configargparse
# Colored output
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger,fmt='[%(levelname)s] %(message)s')