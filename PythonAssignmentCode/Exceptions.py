
class FileNotFoundException(Exception):
    def __init__(self, message="Unable to find the specified file!"):
        super().__init__(message)

class SQLQueryException(Exception):
    def __init__(self, message="Unable to perform the sql command!"):
        super().__init__(message)