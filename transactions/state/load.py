import os
from typing import Tuple

from .state_validator import validate
from ..file_components.factory import FileComponentFactory
from ..file_components.footer import Footer
from ..file_components.header import Header
from ..file_components.transaction import Transaction


def load_components_from_file(
    file_path: str | os.PathLike,
) -> Tuple[Header, list[Transaction], Footer]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

        header = FileComponentFactory.file_component_from_line(lines[0])
        assert type(header) is Header
        footer = FileComponentFactory.file_component_from_line(lines[-1])
        assert type(footer) is Footer

        transactions = [
            FileComponentFactory.file_component_from_line(line) for line in lines[1:-1]
        ]
        assert all([type(transaction) is Transaction for transaction in transactions])

        validate(header, transactions, footer)

        return (
            header,
            transactions,
            footer,
        )
