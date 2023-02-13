"""All custom exceptions for Atomic Operator."""


class PlatformNotSupportedError(Exception):
    """Raised when a platform is not supported by Atomic Operator."""

    def __init__(self, provided_platform: str, supported_platforms: list = []) -> None:
        """Main init for the PlatformNotSupportedError exception."""
        from ..base import Base

        Base().log(message=f"Provided platform '{provided_platform}' is not supported by Atomic Operator. Supported platforms are: {supported_platforms}", level='error')


class IncorrectParameters(Exception):

    """
    Raised when the incorrect configuration of parameters is passed into a Class
    """
    pass


class MissingDefinitionFile(Exception):

    """
    Raised when a definition file cannot be find
    """
    pass


class AtomicsFolderNotFound(Exception):

    """Raised when unable to find a folder containing Atomics
    """
    pass

class MalformedFile(Exception):

    """Raised when a file does not meet an expected and defined format structure
    """
    pass