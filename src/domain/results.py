from dataclasses import dataclass
from .enums import ProcessResult

@dataclass
class GameProcessResult:
    status: ProcessResult
    game_data: dict | int | None