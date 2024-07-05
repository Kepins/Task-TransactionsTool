from typing import Self, ClassVar, Literal, Annotated

from annotated_types import Interval
from pydantic import BaseModel


class Transaction(BaseModel):
    FIELD_ID: ClassVar[str] = "02"

    counter: Annotated[int, Interval(ge=1, le=20000)]
    amount: Annotated[int, Interval(ge=1, le=999999999999)]
    currency: Literal["DOL", "PLN", "EUR"]

    @classmethod
    def from_line(cls, line: str) -> Self:
        field_id = line[0:2].strip()
        counter = int(line[2:8])
        amount = int(line[8:20])
        currency = line[20:23].strip()
        reserved = line[23:120]

        return cls(counter=counter, amount=amount, currency=currency)

    def to_line(self) -> str:
        return (
            self.FIELD_ID
            + str(self.counter).rjust(6, "0")
            + str(self.amount).rjust(12, "0")
            + self.currency.rjust(3)
            + " " * 97
            + "\n"
        )

    class Config:
        validate_assignment = True
