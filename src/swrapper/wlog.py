from __future__ import annotations
import sys
import re
import logging
from collections.abc import Mapping


class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information from logs.

        find remove bot_token from log
        there is some interest example here: https://stackoverflow.com/questions/48380452/mask-out-sensitive-information-in-python-log
    """
    def __init__(self, fmt: str | None = None, datefmt: str | None = None, style="%", validate: bool = True, *, defaults: Mapping[str] | None = None, sensitive_filter: str | None = None) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        # no need to use default here really
        self.sensitive_filter = sensitive_filter


    @staticmethod
    def _filter(st: str, regex: str|None = None):
        return re.sub(regex, '*****', st)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original, self.sensitive_filter)


class Wlog():
    def __init__(self,
                 log_file: str='logfile',
                 log_level: str='info',
                 log_format: str | None = None,
                 stderr_output: bool = False,
                 sensetive_formatter: bool = False,
                 sensitive_filter: str | None = None
                 ) -> None:
        default_log_format = "%(filename)s[LINE:%(lineno)d]# %(levelname)-6s [%(asctime)s] %(funcName)s: %(message)s"

        self.log_file = log_file
        self.log_level = logging.__getattribute__(log_level.upper())
        self.log_format = default_log_format if log_format is None else log_format
        self.stderr_output = stderr_output
        self.sensetive_formatter = sensetive_formatter
        self.sensitive_filter = sensitive_filter

    def set_logging(self):
        """Config log. When DEBUG mode enabled send messages to the log file and to the cli.

        Args:
            logfile (str)
            log_level (str, optional): logging.level
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level) # only messages with root_logger log level or higher will be passed

        file_handler = logging.FileHandler(self.log_file)
        srteam_handler = logging.StreamHandler(sys.stderr)
        file_handler.setLevel = self.log_level
        srteam_handler.setLevel = self.log_level

        if self.sensetive_formatter and self.sensitive_filter is not None:
            file_handler.setFormatter(SensitiveFormatter(self.log_format, sensitive_filter=self.sensitive_filter))
            srteam_handler.setFormatter(SensitiveFormatter(self.log_format, sensitive_filter=self.sensitive_filter))
        else:
            file_handler.setFormatter(logging.Formatter(self.log_format))
            srteam_handler.setFormatter(logging.Formatter(self.log_format))

        # log to file always. Add stderr if enabled or debug-mode
        handlers = [file_handler,]
        if self.stderr_output or self.log_level == logging.DEBUG:
            handlers.append(srteam_handler)

        for _h in handlers:
            root_logger.addHandler(_h)
