
import os
from ConfigParser import ConfigParser

config_location = 'config.ini'
base_directory = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser()
config.read(config_location)

config_output_directory = config.get('output', 'directory')

# Export config variables
__all__ = ['config_output_directory']