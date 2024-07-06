import os

from .file_components.transaction import Transaction
from .state import load_components_from_file
from .state import save_components_to_file


class FileController:
    def __init__(self, file_path: str | os.PathLike) -> None:
        self._file_path = file_path
        self._header, self._transactions, self._footer = load_components_from_file(
            file_path
        )

    def save(self) -> None:
        save_components_to_file(
            self._file_path, self._header, self._transactions, self._footer
        )

    def add_transaction(self, amount: int, currency: str) -> None:
        self._footer.total_counter += 1
        self._footer.control_sum += amount
        self._transactions.append(
            Transaction(
                counter=self._footer.total_counter, amount=amount, currency=currency
            )
        )
        self.save()

    @property
    def name(self) -> str:
        return self._header.name

    @name.setter
    def name(self, value: str) -> None:
        self._header.name = value
        self.save()

    @property
    def surname(self) -> str:
        return self._header.surname

    @surname.setter
    def surname(self, value: str) -> None:
        self._header.surname = value
        self.save()

    @property
    def patronymic(self) -> str:
        return self._header.patronymic

    @patronymic.setter
    def patronymic(self, value: str) -> None:
        self._header.patronymic = value
        self.save()

    @property
    def address(self) -> str:
        return self._header.address

    @address.setter
    def address(self, value: str) -> None:
        self._header.address = value
        self.save()

    def get_transaction_amount(self, idx: int) -> int:
        return self._transactions[idx].amount

    def set_transaction_amount(self, idx: int, value: int) -> None:
        transaction = self._transactions[idx]

        amount_diff = value - transaction.amount
        transaction.amount = value
        self._footer.control_sum += amount_diff
        self.save()

    def get_transaction_currency(self, idx: int) -> str:
        return self._transactions[idx - 1].currency

    def set_transaction_currency(self, idx: int, value: str) -> None:
        transaction = self._transactions[idx - 1]
        transaction.currency = value
        self.save()

    @property
    def total_counter(self) -> int:
        return self._footer.total_counter

    @property
    def control_sum(self) -> int:
        return self._footer.control_sum
