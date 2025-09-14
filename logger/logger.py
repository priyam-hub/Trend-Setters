# DEPENDENCIES

import sys
import logging
from pathlib import Path
from colorama import Fore
from colorama import Style
from datetime import datetime

class LoggerSetup:
    """
    A class to configure and manage logging setup with stylish console output.
    """

    def __init__(self, logger_name: str = "default_logger", log_filename_prefix: str = "log") -> None:
        """
        Initialize the logger setup.

        arguments:
        ----------
        logger_name              {str}       : Name of the logger (useful for multiple loggers).
        
        log_filename_prefix      {str}       : Prefix for log file name.
        
        """
        
        self.log_dir       = Path('logs')
        self.log_dir.mkdir(exist_ok = True)

        log_file           = self.log_dir / f"{log_filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        FORMAT             = "[%(asctime)s %(filename)s->%(funcName)s()] | [line no.:%(lineno)d] %(levelname)s: %(message)s"
        
        self.logger        = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            file_handler   = logging.FileHandler(log_file)
            stream_handler = logging.StreamHandler(sys.stdout)

            formatter      = logging.Formatter(FORMAT)
            file_handler.setFormatter(formatter)

            stream_handler.setFormatter(StyledFormatter(FORMAT))  
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        """
        Returns the configured logger instance.
        """
        return self.logger

    @staticmethod
    def log_info(logger, message):
        """ Logs an info-level message. """
        logger.info(message)

    @staticmethod
    def log_warning(logger, message):
        """ Logs a warning-level message. """
        logger.warning(message)

    @staticmethod
    def log_error(logger, message):
        """ Logs an error-level message with exception info. """
        logger.error(message, exc_info=True)

    @staticmethod
    def log_debug(logger, message):
        """ Logs a debug-level message. """
        logger.debug(message)


class StyledFormatter(logging.Formatter):
    """
    Custom log formatter to add colors to console output using colorama.
    """

    COLOR_MAP               = {"DEBUG"     : Fore.CYAN,
                               "INFO"      : Fore.GREEN,
                               "WARNING"   : Fore.YELLOW,
                               "ERROR"     : Fore.RED + Style.BRIGHT,
                               "CRITICAL"  : Fore.MAGENTA + Style.BRIGHT,
                               "EXCEPTION" : Fore.RED + Style.BRIGHT
                               }

    def format(self, record : str) -> str:

        """
        Formats the log record with colors for console output.

        Arguments:
        ----------
            record                           {logging.LogRecord}            : The log record containing log message, level, 
                                                                              timestamp, and other metadata.

        Returns:
        --------
            formatter_log_string                    {str}                   : A formatted log string with colorized output 
                                                                              based on the log level.
        """
        
        log_color            = self.COLOR_MAP.get(record.levelname, Fore.WHITE)
        reset_color          = Style.RESET_ALL
        formatter_log_string = f"{log_color}{super().format(record)}{reset_color}"
        
        return formatter_log_string