import yaml
import sys
import os
from rich import print


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
                print(f":thumbs_up: Settings loaded: {cfg}")
        except IOError as e:
            print(
                f":sad_but_relieved_face: Settings file {filename} does not exist.")
            print(e)
            sys.exit(os.EX_OSFILE)
        except yaml.YAMLError as e:
            print(
                f":sad_but_relieved_face: Cannot parse settings yaml data.")
            print(e)
            sys.exit(os.EX_OSFILE)
