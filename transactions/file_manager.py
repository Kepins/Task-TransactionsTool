import os
from typing import TextIO, Tuple

from .file_components.factory import FileComponentFactory
from .file_components.footer import Footer
from .file_components.header import Header
from .file_components.transaction import Transaction


class FileManager:
    def __init__(self, file_path: str | os.PathLike):
        self._file_path = file_path
        with open(file_path, "r", encoding="UTF-8") as file:
            self._header, self._transactions, self._footer = self._components_from_file(file)

    @staticmethod
    def _components_from_file(file: TextIO) -> Tuple[Header, list[Transaction], Footer]:
        lines = file.readlines()

        header = FileComponentFactory.file_component_from_line(lines[0])
        assert type(header) is Header
        footer = FileComponentFactory.file_component_from_line(lines[-1])
        assert type(footer) is Footer

        transactions = [FileComponentFactory.file_component_from_line(line) for line in lines[1:-1]]
        assert all([type(transaction) is Transaction for transaction in transactions])

        return (
            header,
            transactions,
            footer,
        )

    def _update_file(self) -> None:
        with open(self._file_path, "w", encoding="UTF-8") as file:
            file.writelines(
                [self._header.to_line(), *[t.to_line() for t in self._transactions], self._footer.to_line(),]
            )

    def add_transaction(self, amount: int, currency: str) -> None:
        self._footer.total_counter += 1
        self._footer.control_sum += amount
        self._transactions.append(Transaction(counter=self._footer.total_counter, amount=amount, currency=currency))
        self._update_file()

    @property
    def name(self) -> str:
        return self._header.name

    @name.setter
    def name(self, value: str) -> None:
        self._header.name = value
        self._update_file()

    @property
    def surname(self) -> str:
        return self._header.surname

    @surname.setter
    def surname(self, value: str) -> None:
        self._header.surname = value
        self._update_file()

    @property
    def patronymic(self) -> str:
        return self._header.patronymic

    @patronymic.setter
    def patronymic(self, value: str) -> None:
        self._header.patronymic = value
        self._update_file()

    @property
    def address(self) -> str:
        return self._header.address

    @address.setter
    def address(self, value: str) -> None:
        self._header.address = value
        self._update_file()

    def get_transaction_amount(self, idx: int) -> int:
        return self._transactions[idx].amount

    def set_transaction_amount(self, idx: int, value: int) -> None:
        transaction = self._transactions[idx]

        amount_diff = value - transaction.amount
        transaction.amount = value
        self._footer.control_sum += amount_diff
        self._update_file()

    def get_transaction_currency(self, idx: int) -> str:
        return self._transactions[idx-1].currency

    def set_transaction_currency(self, idx: int, value: str) -> None:
        transaction = self._transactions[idx - 1]
        transaction.currency = value
        self._update_file()

    @property
    def total_counter(self) -> int:
        return self._footer.total_counter

    @property
    def control_sum(self) -> int:
        return self._footer.control_sum
