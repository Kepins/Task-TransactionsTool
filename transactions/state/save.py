import os

from .state_validator import validate
from ..file_components.footer import Footer
from ..file_components.header import Header
from ..file_components.transaction import Transaction


def save_components_to_file(
    file_path: str | os.PathLike,
    header: Header,
    transactions: list[Transaction],
    footer: Footer,
) -> None:
    validate(header, transactions, footer)

    with open(file_path, "w", encoding="UTF-8") as file:
        file.writelines(
            [
                header.to_line(),
                *[t.to_line() for t in transactions],
                footer.to_line(),
            ]
        )
