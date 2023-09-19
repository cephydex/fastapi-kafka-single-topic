import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

class EchoService:
  def echo(self, msg):
    logger.info("echoing something from the sponzio logger")
    print(msg)