from enum import Enum

class ProcessResult(Enum):
    CREATED = "created"
    SKIPPED = "skipped"
    FAILED = "failed"