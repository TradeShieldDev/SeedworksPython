
from enum import Enum
from sdk.logging.logging_settings import LoggingSettings

import configparser
import os

class ConfigType(Enum):
    INI = 1
    JSON = 2

class ConfigManager:

    # Static Variables  
    DEFAULT_INI_FILENAME:str = 'config.ini'
    DEFAULT_JSON_FILENAME:str = 'app_config.json'      
    _instance = None

    type:ConfigType = None
    file_name:str = None

    def __init__(self, type:ConfigType, file_name:str):
        self.type = type
        self.file_name = file_name

    @staticmethod
    def get_instance():

        type:ConfigType = None
        file_name:str = None

        if ConfigManager._instance is not None:
            return ConfigManager._instance

        found_json = os.path.exists(ConfigManager.DEFAULT_JSON_FILENAME)
        found_ini = os.path.exists(ConfigManager.DEFAULT_INI_FILENAME)   

        if (found_json):
            type = ConfigType.JSON
            ConfigManager._file_name = ConfigManager.DEFAULT_JSON_FILENAME

        elif (found_ini):
            ConfigManager._type = ConfigType.INI
            ConfigManager._file_name = ConfigManager.DEFAULT_INI_FILENAME

        else: raise Exception(f'No default config file found, expected [{ConfigManager.DEFAULT_INI_FILENAME}] or [{ConfigManager.DEFAULT_JSON_FILENAME}].')    

        ConfigManager._instance = ConfigManager.__create_instance__(ConfigManager._type, ConfigManager._file_name)
        return ConfigManager._instance


    def _get_ini_logger_config(self) -> LoggingSettings:
        config = configparser.ConfigParser()
        log_settings = LoggingSettings()

        # Read the config.ini file
        config.read(self.file_name)

        log_settings.level = config['logger_settings']['level']
        log_settings.file_name = config['logger_settings']['file_name']
        log_settings.path = config['logger_settings']['path']
        log_settings.max_file_size_in_mb = config['logger_settings']['max_file_size']
        log_settings.max_retention_days = config['logger_settings']['max_retention_days']

        return log_settings


    def _get_json_logger_config(self) -> LoggingSettings:
        raise Exception('[__get_json_logger_config] is not implimented')

        logger_settings = config_reader.section('logging', Logging)            
        log_level = _get_log_level(logger_settings.level)
        log_filename =  logger_settings.file_name
        log_file_path = logger_settings.path
        max_file_size_mb = logger_settings.max_file_size_in_mb
        max_number_of_files = logger_settings.max_number_of_files


    def __create_instance__(type:ConfigType, file_name:str):
        # Check if the file exists
        if not os.path.exists(file_name):
            print(f'Cannot find the specified configuration file [{file_name}]')
        
        instance = ConfigManager(type, file_name)
        return instance      


    def get_logger_config(self) -> LoggingSettings:
        
        if (ConfigManager._type == ConfigType.INI):
            return self._get_ini_logger_config()
        
        elif (ConfigManager._type == ConfigType.JSON):
            return self._get_json_logger_config()

        else: raise Exception(f"Type [{ConfigManager._type}] does not have method for getting the logger config.")

