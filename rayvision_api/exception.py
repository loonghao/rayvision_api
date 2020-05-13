"""CG errors."""

from future.moves.urllib.request import HTTPErrorProcessor
from pprint import pformat


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


class RayvisonTaskIdError(RayvisionError):
    """Raise RayVisonTaskIdError."""

    def __init__(self, error_code, error):
        """Initialize Task error message, inherited RayvisionError."""
        super(RayvisionError, self).__init__(error_code, error)
        self.error_code = 2000
        self.error = error

    def __str__(self):
        """Let its  object  out an error message."""
        return 'Error code: {}, Error message: {}'.format(
            self.error_code,
            self.error,
        )


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
                'Post data: {}, '
                'URL: {}'.format(self.error_code,
                                 self.error_message,
                                 pformat(self.post_data),
                                 self.request_url))


class AnalyzeError(Exception):
    """Analyze has a damage error."""


class MaxDamageError(AnalyzeError):
    """Max has a damage error."""


class MaxExeNotExistError(AnalyzeError):
    """There are no errors in the Max startup file."""


class CGExeNotExistError(AnalyzeError):
    """No errors in CG boot."""


class ProjectMaxVersionError(AnalyzeError):
    """Project Max version error."""


class GetCGVersionError(AnalyzeError):
    """Error getting CG version."""


class GetRendererError(AnalyzeError):
    """Get renderer error."""


class GetCGLocationError(AnalyzeError):
    """Error getting CG local path."""


class MultiScatterAndVrayConfilictError(AnalyzeError):
    """Multi scatter and vray Confilict error."""


class VersionNotMatchError(AnalyzeError):
    """Version not match error."""


class CGFileNotExistsError(AnalyzeError):
    """CG file does not exist error."""


class CGFileZipFailError(AnalyzeError):
    """CG file compression failed error."""


class CGFileNameIllegalError(AnalyzeError):
    """CG File Name Illegal Error."""


class AnalyseFailError(AnalyzeError):
    """Analyse Fail Error."""


class FileNameContainsChineseError(AnalyzeError):
    """File Name Contains Chinese Error."""


class CompressionFailedError(Exception):
    """Compression failed error."""


class DecompressionFailedError(Exception):
    """Unzip failed error."""
