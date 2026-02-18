from dataclasses import dataclass
from .enums import ProcessResult

@dataclass
class GameProcessResult:
    status: ProcessResult
    data: dict | int | None
    msg: str | None