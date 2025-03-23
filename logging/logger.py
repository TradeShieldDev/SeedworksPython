from loguru import logger
from sdk.config.config_loader import ConfigManager

from sdk.contracts.logging_settings import LoggingSettings

import os

def _get_log_level(level:str):
    
    if (level.lower() == 'trace'):
        return "TRACE"

    if (level.lower() == 'debug'):
        return "DEBUG"
    
    if (level.lower() == 'info'):
        return "INFO"
    
    if (level.lower() == 'warn'):
        return "WARNING"
    
    if (level.lower() == 'error'):
        return "ERROR"
    
    if (level.lower() == 'critical'):
        return "CRITICAL"
    
    raise ValueError('Unknown log level specified in configuration')

class Logger:
    _logger_instance = None

    @staticmethod
    def get_instance():
        if Logger._logger_instance is None:
            Logger._logger_instance = Logger._setup_logger()
        return Logger._logger_instance

    @staticmethod
    def _setup_logger():
        try:
            config_reader:ConfigManager = ConfigManager.get_instance()
            logger_settings:LoggingSettings = config_reader.get_logger_config()

            os.makedirs(logger_settings.path, exist_ok=True)

            log_format:str = None

            if (hasattr(logger_settings, "log_format") == False or logger_settings.log_format == ""):
                log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {module}.{function}:{line} - {message}"
            else:
                log_format = logger_settings.log_format            

            logger.add(
                f"{logger_settings.path}/{logger_settings.file_name}",
                level= _get_log_level(logger_settings.level),
                rotation=f"{str(logger_settings.max_file_size_in_mb)} MB",
                retention=f"{str(logger_settings.max_retention_days)} days",
                enqueue=True,  # Safe in multi-threaded apps
                backtrace=True,
                compression="zip",  # Compress old log files
                format=log_format
            )

            return logger

        except Exception as ex:
            print(f"Oops! {ex.__class__} occurred. Unable to initialize the logger. Details: {ex}")
            raise