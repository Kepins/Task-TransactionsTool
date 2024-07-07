import os
from typing import Tuple

from .file_components import Footer
from .file_components.header import Header
from .file_components import Transaction


class Model:
    def __init__(self, file_path: str | os.PathLike):
        self.file_path = file_path

    def load_components_from_file(self) -> Tuple[Header, list[Transaction], Footer]:
        with open(self.file_path, "r", encoding="UTF-8") as file:
            lines = file.read().splitlines()

            lines_not_120s = [len(line) != 120 for line in lines]
            if any(lines_not_120s):
                first_line_not_120 = lines_not_120s.index(True)
                raise ValueError(
                    f"Line {first_line_not_120} has {len(lines[first_line_not_120])} characters should have 120"
                )

            header_line = lines[0]
            header = Header.from_line(header_line)

            footer_line = lines[-1]
            footer = Footer.from_line(footer_line)

            transactions = [
                Transaction.from_line(line, line_num)
                for line_num, line in zip(range(1, 1 + len(lines[1:-1])), lines[1:-1])
            ]

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
