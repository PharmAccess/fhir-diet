import logging
from logging import Logger

from rich.console import Console
from rich.logging import RichHandler

_LOGGER_NAME = 'fhir-diet'


def _translate_level(level):
    level_translation = {
        1: logging.FATAL,
        2: logging.ERROR,
        3: logging.WARN,
        4: logging.INFO,
        5: logging.DEBUG
    }

    return level_translation.get(level, logging.INFO)


def _setup_log_format():
    msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    msg_format_rich = '%(message)s'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    error_console = Console(stderr=True)
    rh = RichHandler(console=error_console, markup=True)
    rh.setFormatter(logging.Formatter(msg_format_rich, datefmt='[%X]'))

    logging.basicConfig(
        format=msg_format,
        datefmt=datetime_format,
        handlers=[rh]
    )

def _init_root_level():
    root_log = logging.getLogger()
    root_log.setLevel(logging.WARN)


def _init_app_level(level):
    log = logging.getLogger(_LOGGER_NAME)
    log.setLevel(_translate_level(level))

    log.info("Log level is set to %s (input was: %i)",
             logging.getLevelName(log.getEffectiveLevel()), level)



def init_logger(level: int):
    """
    Initialize the logger. The next translation happens for setting up the log level:

    1: logging.FATAL
    2: logging.ERROR
    3: logging.WARN
    4: logging.INFO
    5: logging.DEBUG

    :param level: integer value used to configure the log level for the logger
    :return: None
    """

    _setup_log_format()
    _init_root_level()
    _init_app_level(int(level))


def get_logger() -> Logger:
    """
    Retrieve a logger specific for the application. This logger is an implementation of the default Python
    logger but can be configured by init_logger().

    :return: The CareAnalytics logger.
    """
    return logging.getLogger(_LOGGER_NAME)
