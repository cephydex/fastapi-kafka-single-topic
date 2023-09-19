import logging

# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)-4s - %(funcName)s() L%(lineno)-4d - %(message)s")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-4s - %(funcName)s() L%(lineno)-4d - %(message)s")
LOGGER = logging.getLogger(__name__)
# LOGGER = logging.getLogger('main_logger')
