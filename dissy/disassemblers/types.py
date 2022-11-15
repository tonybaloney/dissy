from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class NativeType(Enum):
    X86_64 = auto()
    PYTHON = auto()


@dataclass
class DisassembledImage:
    instructions: List
    offsets: List
    entry_point: int
    native_type: NativeType
