import traceback
import logging
from botocore import exceptions
logger = logging.getLogger("app")

def logging_warn_exception(e: Exception):
    if (isinstance(e, exceptions.ClientError)):
        logger.warn(e.response)
    logger.warning("{}\n{}".format(str(e), traceback.format_exc()))

def logging_error_exception(e: Exception):
    if (isinstance(e, exceptions.ClientError)):
        logger.error(e.response)
    logger.error("{}\n{}".format(str(e), traceback.format_exc()))