import os
import logging.config
import yaml

from enum import Enum
from logging import FileHandler, DEBUG, INFO, ERROR, WARNING, CRITICAL
import logging


class LogParam(str, Enum):
    EVENT = "_ao_event"
    OPERATOR_COMMAND = "_ao_operator_command"
    TIME_STAMP = "_ao_time_stamp"
    TARGET_IP = "_ao_target_ip"
    TARGET_HOST_NAME = "_ao_target_host_name"
    PROCEDURE_NAME = "_ao_procedure_name"
    PROCEDURE_DESCRIPTION = "_ao_procedure_description"
    PROCEDURE_GUID = "_ao_procedure_guid"
    EXECUTION_ID = "_ao_execution_id"
    EVENT_PROCEDURE = '_ao_event_procedure'
    EVENT_TECHNIQUE_ID = '_ao_technique_id'
    EXECUTOR_COMMAND = "_ao_executor_command"
    EXECUTOR ="_ao_executor"
    TIME_START = "_ao_time_start"
    TIME_STOP="_ao_time_stop"
    STD_OUTPUT = "_ao_std_output"
    STD_ERROR = "_ao_std_error"

class Event(str, Enum):
    ATOMIC_RUN_EXEC = "atomic_run_exec"
    ATOMIC_TEST_COMPLETE = "atomic_test_complete"


class DebugFileHandler(FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        if not record.levelno == DEBUG:
            return
        super().emit(record)


class LoggingBase(type):
    def __init__(cls, *args):
        super().__init__(*args)
        cls.setup_logging()

        # Explicit name mangling
        logger_attribute_name = '_' + cls.__name__ + '__logger'

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = '.'.join([c.__name__ for c in cls.mro()[-2::-1]])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))

    def setup_logging(cls, default_path='./atomic_operator/data/logging.yml', default_level=logging.INFO, env_key='LOG_CFG'):
        """Setup logging configuration
        """
        path = os.path.abspath(os.path.expanduser(os.path.expandvars(default_path)))
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(os.path.abspath(path)):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logger = logging.config.dictConfig(config)
        else:
            logger = logging.basicConfig(level=default_level)
