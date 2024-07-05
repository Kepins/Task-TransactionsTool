from dataclasses import dataclass
from typing import Self


@dataclass
class Transaction:
    FIELD_ID = "02"

    counter: int
    amount: int
    currency: str

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
