from ..model.file_components import Transaction
from ..model import Model
from .state_validator import validate


class Controller:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._header, self._transactions, self._footer = (
            self._model.load_components_from_file()
        )
        validate(self._header, self._transactions, self._footer)

    def save(self) -> None:
        validate(self._header, self._transactions, self._footer)
        self._model.save_components_to_file(
            self._header, self._transactions, self._footer
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
        num_transactions = len(self._transactions)
        if idx < 1 or idx > num_transactions:
            raise IndexError(
                f"IDX must be greater or equal to 1 and less or equal to {num_transactions}"
            )

        return self._transactions[idx].amount

    def set_transaction_amount(self, idx: int, value: int) -> None:
        num_transactions = len(self._transactions)
        if idx < 1 or idx > num_transactions:
            raise IndexError(
                f"IDX must be greater or equal to 1 and less or equal to {num_transactions}"
            )

        transaction = self._transactions[idx]

        amount_diff = value - transaction.amount
        transaction.amount = value
        self._footer.control_sum += amount_diff
        self.save()

    def get_transaction_currency(self, idx: int) -> str:
        num_transactions = len(self._transactions)
        if idx < 1 or idx > num_transactions:
            raise IndexError(
                f"IDX must be greater or equal to 1 and less or equal to {num_transactions}"
            )

        return self._transactions[idx - 1].currency

    def set_transaction_currency(self, idx: int, value: str) -> None:
        num_transactions = len(self._transactions)
        if idx < 1 or idx > num_transactions:
            raise IndexError(
                f"IDX must be greater or equal to 1 and less or equal to {num_transactions}"
            )

        transaction = self._transactions[idx - 1]
        transaction.currency = value
        self.save()

    @property
    def total_counter(self) -> int:
        return self._footer.total_counter

    @property
    def control_sum(self) -> int:
        return self._footer.control_sum
