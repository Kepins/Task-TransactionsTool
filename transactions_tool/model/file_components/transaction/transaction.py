from typing import Self, ClassVar, Literal, Annotated

from annotated_types import Interval
from pydantic import BaseModel

from transactions_tool.constants import MAX_TRANSACTION_AMOUNT, MAX_COUNTER


class Transaction(BaseModel):
    FIELD_ID: ClassVar[str] = "02"

    counter: Annotated[int, Interval(ge=1, le=MAX_COUNTER)]
    amount: Annotated[int, Interval(ge=1, le=MAX_TRANSACTION_AMOUNT)]
    currency: Literal["DOL", "PLN", "EUR"]

    @classmethod
    def from_line(cls, line: str, line_num: int) -> Self:
        field_id = line[0:2]
        if field_id != Transaction.FIELD_ID:
            raise ValueError(
                f"Line {line_num}: Field ID of Transaction is equal to {field_id} should be {Transaction.FIELD_ID}"
            )

        counter = int(line[2:8])
        amount = int(line[8:20])
        currency = line[20:23].lstrip()
        reserved = line[23:120]

        if reserved != " " * 97:
            raise ValueError(
                f"Line {line_num}: Reserved buffer in Transaction is not spaces"
            )

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
