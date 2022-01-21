"""File with the implementation of all custom exceptions of PotatoParser
"""


class PotatoParserError(Exception):
    """Common base class for all errors of PotatoParser. Has
    additional :meth:`log` function to log current error to
    console
    """

    def _log_func(self, msg):
        """Local function which used only to print log message to console.
        Used by :meth:`log` and must be redefined

        Args:
            msg (str): a message to print in the console
        """
        pass

    def log(self):
        """Public function which generates message of the current error and
        logs it to the console. Should be redefined in your error
        """
        self._log_func(str(self))


class CommandArgumentError(PotatoParserError):
    def log(self):
        self._log_func('Invalid command argument(s): ' + str(self))


class CommandUsageError(PotatoParserError):
    def log(self):
        self._log_func('Invalid command usage: ' + str(self))


class PotatoParserWarning(Exception):
    """Common base class for all warnings of PotatoParser. Has
    additional :meth:`log` function to log current warning to
    console
    """

    def _log_func(self, msg):
        """Local function which used only to print log message to console.
        Used by :meth:`log` and must be redefined

        Args:
            msg (str): a message to print in the console
        """
        pass

    def log(self):
        """Public function which generates message of the current warning and
        logs it to the console. Should be redefined in your warning
        """
        self._log_func(str(self))


class CommandInfoWarning(PotatoParserWarning):
    pass
