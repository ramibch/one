class BaseSubmoduleException(Exception):
    pass


class SubmoduleException(BaseSubmoduleException):
    pass


class SubmoduleFolderModelUnknow(BaseSubmoduleException):
    pass
