from typing import Self, ClassVar, Annotated

from annotated_types import Interval
from pydantic import BaseModel


class Footer(BaseModel):
    FIELD_ID: ClassVar[str] = "03"

    total_counter: Annotated[int, Interval(ge=0, le=20000)]
    control_sum: Annotated[int, Interval(ge=0, le=999999999999)]

    @classmethod
    def from_line(cls, line: str) -> Self:
        field_id = line[0:2]

        if field_id != Footer.FIELD_ID:
            raise ValueError(
                f'Field ID of Footer is equal to "{field_id}" should be "{Footer.FIELD_ID}"'
            )

        total_counter = line[2:8]
        control_sum = line[8:20]
        reserved = line[20:120]

        if reserved != " " * 100:
            raise ValueError(f"Reserved buffer in Footer is not spaces")

        return cls(total_counter=total_counter, control_sum=control_sum)

    def to_line(self) -> str:
        return (
            self.FIELD_ID
            + str(self.total_counter).rjust(6, "0")
            + str(self.control_sum).rjust(12, "0")
            + " " * 100
            + "\n"
        )

    class Config:
        validate_assignment = True
