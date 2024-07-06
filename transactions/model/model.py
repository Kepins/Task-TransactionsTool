import os
from typing import Tuple

from ..file_components.factory import FileComponentFactory
from ..file_components.footer import Footer
from ..file_components.header import Header
from ..file_components.transaction import Transaction


class Model:
    def __init__(self, file_path: str | os.PathLike):
        self.file_path = file_path

    def load_components_from_file(self) -> Tuple[Header, list[Transaction], Footer]:
        with open(self.file_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()

            header = FileComponentFactory.file_component_from_line(lines[0])
            assert type(header) is Header
            footer = FileComponentFactory.file_component_from_line(lines[-1])
            assert type(footer) is Footer

            transactions = [
                FileComponentFactory.file_component_from_line(line)
                for line in lines[1:-1]
            ]
            assert all(
                [type(transaction) is Transaction for transaction in transactions]
            )

            return (
                header,
                transactions,
                footer,
            )

    def save_components_to_file(
        self,
        header: Header,
        transactions: list[Transaction],
        footer: Footer,
    ) -> None:
        with open(self.file_path, "w", encoding="UTF-8") as file:
            file.writelines(
                [
                    header.to_line(),
                    *[t.to_line() for t in transactions],
                    footer.to_line(),
                ]
            )
