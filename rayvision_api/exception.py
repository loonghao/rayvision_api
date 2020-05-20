"""The exception for the rayvision api."""


class RayvisionError(Exception):
    """Raise RayvisionError if something wrong."""

    def __init__(self, error_code, error, *args, **kwargs):
        """Initialize error message, inherited Exception.

        Args:
            error_code (int): Error status code.
            error (str): Error message.
            args (set): Other parameters.
            kwargs (dict): Other keyword parameters.

        """
        super(RayvisionError, self).__init__(self, error, *args, **kwargs)
        self.error_code = error_code
        self.error = error

    def __str__(self):
        """Let its  object  out an error message."""
        return 'RayvisionError: {0}: {1}'.format(self.error_code, self.error)


class RayvisionAPIError(RayvisionError):
    """Raise RayVisionAPIError."""

    def __init__(self, error_code, error, request):
        """Initialize API error message, inherited RayvisionError.

        Args:
            error_code (int): Error status code.
            error (object): Error message.
            request (str): Request url.

        """
        super(RayvisionAPIError, self).__init__(error_code, error)
        self.error_code = error_code
        self.error = error
        self.request = request

    def __str__(self):
        """Let its  object print out an error message."""
        return 'Error code: {}, Error message: {}, URL: {}'.format(
            self.error_code,
            self.error,
            self.request)


class RayvisionAPIParameterError(RayvisionError):
    def __init__(self, error_message, data, request_url):
        """Initialize Task error message, inherited RayvisionError.

        Args:
            response (requests.Response): The response of the requests.

        """
        self.error_message = error_message
        self.error_code = 601
        self.request_url = request_url
        self.post_data = data

    def __str__(self):
        """Let its  object  out an error message."""
        return ('Error code: {}, '
                'Error message: Request parameter error ({}), '
                'URL: {}'.format(self.error_code,
                                 self.error_message,
                                 self.request_url))
