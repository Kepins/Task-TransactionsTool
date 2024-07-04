from dataclasses import dataclass
from typing import Self


@dataclass
class Footer:
    FIELD_ID = "03"

    total_counter: int
    control_sum: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        field_id = line[0:2].strip()
        total_counter = int(line[2:8])
        control_sum = int(line[8:20])
        reserved = line[20:120]

        return cls(total_counter=total_counter, control_sum=control_sum)

    def to_line(self) -> str:
        return (
            self.FIELD_ID
            + str(self.total_counter).rjust(6, "0")
            + str(self.control_sum).rjust(12, "0")
            + " " * 100
            + "\n"
        )
