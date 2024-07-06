from typing import Self, ClassVar, Annotated

from pydantic import BaseModel, StringConstraints


class Header(BaseModel):
    FIELD_ID: ClassVar[str] = "01"

    name: Annotated[str, StringConstraints(max_length=28)]
    surname: Annotated[str, StringConstraints(max_length=30)]
    patronymic: Annotated[str, StringConstraints(max_length=30)]
    address: Annotated[str, StringConstraints(max_length=30)]

    @classmethod
    def from_line(cls, line: str) -> Self:
        field_id = line[0:2]
        name = line[2:30].lstrip()
        surname = line[30:60].lstrip()
        patronymic = line[61:90].lstrip()
        address = line[91:120].lstrip()

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

    class Config:
        validate_assignment = True
