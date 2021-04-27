"""
Application configuration module
"""
from os.path import join, dirname

from dynaconf.base import Settings

CONFIGS_PATH = join(dirname(__file__), 'configs')
config = Settings()
