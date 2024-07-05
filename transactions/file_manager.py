import functools
import os
from typing import TextIO, Tuple

from .file_components.factory import FileComponentFactory
from .file_components.footer import Footer
from .file_components.header import Header
from .file_components.transaction import Transaction


class FileManager:
    MAX_NUMBER_OF_TRANSACTIONS = 20_000

    def __init__(self, file_path: str | os.PathLike):
        self._file_path = file_path
        with open(file_path, "r", encoding="UTF-8") as file:
            self._header, self._transactions, self._footer = self._components_from_file(
                file
            )

    @classmethod
    def _validate_transactions_counters(cls, transactions: list[Transaction]):
        errors = [
            ValueError(f"Transaction {i} in order has counter value of {t.counter}.")
            for i, t in zip(range(1, len(transactions) + 1), transactions)
            if t.counter != i
        ]

        if errors:
            raise ExceptionGroup("Transactions counters are not valid.", errors)

    @classmethod
    def _validate_number_of_transactions_matches_total_counter(
        cls, transactions: list[Transaction], total_counter: int
    ):
        num_transactions = len(transactions)
        if total_counter != num_transactions:
            raise ValueError(
                f'Total counter "{total_counter}" does not match number of transactions "{num_transactions}".'
            )

    @classmethod
    def _validate_max_number_of_transactions(cls, number_of_transactions: int):
        if number_of_transactions > cls.MAX_NUMBER_OF_TRANSACTIONS:
            raise ValueError(
                f'Number of transactions cannot exceed "{cls.MAX_NUMBER_OF_TRANSACTIONS}".'
            )

    @classmethod
    def _validate_control_sum_equal_to_sum_of_amounts(
        cls, transactions: list[Transaction], control_sum: int
    ):
        sum_amounts = sum([t.amount for t in transactions])
        if sum_amounts != control_sum:
            raise ValueError(
                f'Sum of amounts "{sum_amounts}" does not match control sum which is "{control_sum}".'
            )

    @classmethod
    def _validate_state_after_loading(
        cls, header: Header, transactions: list[Transaction], footer: Footer
    ):
        validators = [
            functools.partial(
                cls._validate_transactions_counters,
                transactions=transactions,
            ),
            functools.partial(
                cls._validate_number_of_transactions_matches_total_counter,
                transactions=transactions,
                total_counter=footer.total_counter,
            ),
            functools.partial(
                cls._validate_max_number_of_transactions,
                number_of_transactions=len(transactions),
            ),
            functools.partial(
                cls._validate_control_sum_equal_to_sum_of_amounts,
                transactions=transactions,
                control_sum=footer.control_sum,
            ),
        ]

        errors = []
        for validator in validators:
            try:
                validator()
            except Exception as e:
                errors.append(e)

        if errors:
            raise ExceptionGroup("Validation failed", errors)

    @classmethod
    def _components_from_file(
        cls, file: TextIO
    ) -> Tuple[Header, list[Transaction], Footer]:
        lines = file.readlines()

        header = FileComponentFactory.file_component_from_line(lines[0])
        assert type(header) is Header
        footer = FileComponentFactory.file_component_from_line(lines[-1])
        assert type(footer) is Footer

        transactions = [
            FileComponentFactory.file_component_from_line(line) for line in lines[1:-1]
        ]
        assert all([type(transaction) is Transaction for transaction in transactions])

        cls._validate_state_after_loading(header, transactions, footer)
        return (
            header,
            transactions,
            footer,
        )

    def _update_file(self) -> None:
        with open(self._file_path, "w", encoding="UTF-8") as file:
            file.writelines(
                [
                    self._header.to_line(),
                    *[t.to_line() for t in self._transactions],
                    self._footer.to_line(),
                ]
            )

    def add_transaction(self, amount: int, currency: str) -> None:
        self._validate_max_number_of_transactions(self._footer.total_counter + 1)

        self._footer.total_counter += 1
        self._footer.control_sum += amount
        self._transactions.append(
            Transaction(
                counter=self._footer.total_counter, amount=amount, currency=currency
            )
        )
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
        return self._transactions[idx - 1].currency

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
