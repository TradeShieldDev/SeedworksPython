
from enum import Enum
from sdk.contracts.logging_settings import LoggingSettings

import configparser
import os

class ConfigType(Enum):
    INI = 1
    JSON = 2

class DataType(Enum):
    String = 1
    Integer = 2
    Float = 3
    Boolean = 4

class ConfigManager:

    # Static Variables  
    DEFAULT_INI_FILENAME:str = 'config.ini'
    DEFAULT_JSON_FILENAME:str = 'app_config.json'      
    DEFAULT_LOGGER_SECTION = 'logger_settings'

    _instance = None
    _ini_config:configparser.ConfigParser = None

    type:ConfigType = None
    file_name:str = None

    def __init__(self, type:ConfigType, file_name:str):
        self.type = type
        self.file_name = file_name

        # Load INI Config Reader
        if (self.type == ConfigType.INI):
            self._ini_config = configparser.ConfigParser()
            self._ini_config.read(self.file_name)


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

        log_settings = LoggingSettings()      

        log_settings.level = self._ini_config.get(ConfigManager.DEFAULT_LOGGER_SECTION, 'level', fallback=None)
        log_settings.file_name = self._ini_config.get(ConfigManager.DEFAULT_LOGGER_SECTION, 'file_name', fallback=None)
        log_settings.path = self._ini_config.get(ConfigManager.DEFAULT_LOGGER_SECTION, 'path', fallback=None)
        log_settings.max_file_size_in_mb = self._ini_config.get(ConfigManager.DEFAULT_LOGGER_SECTION, 'max_file_size', fallback=None)
        log_settings.max_retention_days = self._ini_config.get(ConfigManager.DEFAULT_LOGGER_SECTION, 'max_retention_days', fallback=None)

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
        
        logger_config:LoggingSettings = None

        if (ConfigManager._type == ConfigType.INI):
            logger_config = self._get_ini_logger_config()
        
        elif (ConfigManager._type == ConfigType.JSON):
            logger_config = self._get_json_logger_config()

        else: raise Exception(f"Type [{ConfigManager._type}] does not have method for getting the logger config.")


        if logger_config.file_name == None:
            logger_config.file_name = 'app.log'
        
        if logger_config.level == None:
            logger_config.level = 'warn'

        if logger_config.path == None:
            logger_config.path = 'logs/'

        if logger_config.max_file_size_in_mb == None:
            logger_config.max_file_size_in_mb = 15

        if logger_config.max_retention_days == None:
            logger_config.max_retention_days = 90

        return logger_config
    

    def get_ini_config_value(self, section, key, default=None, data_type=DataType.String):
        # If section is an Enum, use its value; otherwise, use it directly
        section_name = section.value if isinstance(section, Enum) else section

        string_value = self._ini_config.get(section_name, key, fallback=default)

        # If the config doesn’t have the key at all, return default right away
        if string_value is None:
            return default

        # Convert the string_value to the requested data type
        try:
            if data_type == DataType.Integer:
                return int(string_value)
            
            elif data_type == DataType.Float:
                return float(string_value)
            
            elif data_type == DataType.Boolean:
                # Decide how to handle booleans; here we convert common strings like "true", "false"
                # or "1", "0" to a Boolean value
                lower_val = str(string_value).lower()
                if lower_val in ['true', '1', 'yes', 'on']:
                    return True
                elif lower_val in ['false', '0', 'no', 'off']:
                    return False
                
                else:
                    # If it’s an unrecognized string, fall back to default or raise an error
                    return default
            else:
                # Default is just returning the string as-is
                return string_value
            
        except (ValueError, TypeError):
            # If parsing fails, you could raise or return the default
            return default
