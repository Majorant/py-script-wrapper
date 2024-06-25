import argparse


class Wargs(argparse.ArgumentParser):
    def add_defult_arguments(self, *args, **kwargs):
        """Set default arguments to parse:

            -c, --config    `config file`

            -d, --debug     `debug mode`

            -l, --log       `set logfile`
        """
        self.add_argument('-c', '--config', dest='config', help='config file')
        self.add_argument('-d', '--debug', dest='debug', help='enable debug mode', action='store_true')
        self.add_argument('-l', '--log', dest='log_file', help='log file')
