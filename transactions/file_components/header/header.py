from dataclasses import dataclass
from typing import Self


@dataclass
class Header:
    FIELD_ID = "01"

    name: str
    surname: str
    patronymic: str
    address: str

    @classmethod
    def from_line(cls, line: str) -> Self:
        field_id = line[0:2].strip()
        name = line[2:30].strip()
        surname = line[30:60].strip()
        patronymic = line[61:90].strip()
        address = line[91:120].strip()

        return cls(name=name, surname=surname, patronymic=patronymic, address=address)

    def to_line(self) -> str:
        return (
            self.FIELD_ID
            + self.name.rjust(28)
            + self.surname.rjust(30)
            + self.patronymic.rjust(30)
            + self.address.rjust(30)
            + "\n"
        )
