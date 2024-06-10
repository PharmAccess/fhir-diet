import os
import sys
import yaml
from utils.logger_wrapper import get_logger

log = get_logger()

class Settings:

    def __init__(self, filename=""):
        if not filename:
            filename = "config.yaml"
        self.parse(filename)

    def parse(self, filename):
        try:
            with open(filename, "r") as ymlfile:
                cfg = yaml.safe_load(ymlfile)
                # Set values of the dictionary as class attributes
                for key in cfg:
                    setattr(self, key, cfg[key])
                log.info(f":thumbs_up: Settings file {filename} loaded")
                log.debug(f"Settings={self.__dict__}")
        except IOError as e:
            log.error(
                f":sad_but_relieved_face: Settings file {filename} does not exist.")
            log.error(e)
            sys.exit(os.EX_OSFILE)
        except yaml.YAMLError as e:
            log.error(
                f":sad_but_relieved_face: Cannot parse settings yaml data.")
            log.error(e)
            sys.exit(os.EX_OSFILE)
