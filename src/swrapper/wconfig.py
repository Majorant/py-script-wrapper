from __future__ import annotations
import sys
import logging
import yaml
import json
import swrapper.exceptions


class Config():
    def __init__(self, filename: str, type: str='yaml', sensetive_attributes: list[str]=None) -> None:
        self.sensetive_attributes = [] if sensetive_attributes is None else sensetive_attributes
        try:
            with open(filename, 'r') as f:
                if type == 'yaml':
                    conf = yaml.safe_load(f)
                elif type == 'json':
                    conf = json.load(f)
                else:
                    raise swrapper.exceptions.UnknownConfigType

            for name, value in conf.items():
                self.__setattr__(name, value)
        except FileNotFoundError:
            logging.error('Config file not found: %s', filename)
            sys.exit(1)
        except KeyError as e:
            logging.exception('Error during config loading. Require variables are absent.')
            sys.exit(1)
        except yaml.YAMLError as e:
            logging.error('Error yaml file reading. Check config file type')
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            logging.error('Error json decode file. Check config file type')
            sys.exit(1)
        except swrapper.exceptions.UnknownConfigType as e:
            logging.exception('Unknown config type. Expected "json" or "yaml"')
            sys.exit(1)


    def __str__(self) -> str:
        _l = []
        for k,v in self.__dict__.items():
            v = '***hidden***' if self.is_sensetive(k) else v
            _l.append(f'{k} = {v}')

        return '\n'.join(_l)

    def is_sensetive(self, attribute_name: str) -> bool:
        if attribute_name in self.sensetive_attributes:
            return True
        return False
