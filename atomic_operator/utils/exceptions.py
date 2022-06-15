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


class ContentFolderNotFound(Exception):

    """Raised when unable to find a folder containing either Adversary Emulation Library or Atomics
    """
    pass


class AdversaryEmulationFolderNotFound(Exception):

    """Raised when unable to find a folder containing adversary emulation library
    """
    pass


class MalformedFile(Exception):

    """Raised when a file does not meet an expected and defined format structure
    """
    pass