from enum import Enum


class Status(Enum):
    """
    Status of a job.
    """
    SUCCESS = 0  # Success
    UNKNOWN = 1  # Unknown error
    FILE_NOT_FOUND = 2  # FileNotFoundError; use an output folder that does not exist
    FILE_EXISTS = 3  # FileExistsError; create data in an already existing folder

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value
