from typing import ClassVar

from pydantic import BaseModel, field_validator, model_validator

from transactions.file_components.footer import Footer
from transactions.file_components.header import Header
from transactions.file_components.transaction import Transaction


def validate(header: Header, transactions: list[Transaction], footer: Footer) -> None:
    StateValidator(header=header, transactions=transactions, footer=footer)


class StateValidator(BaseModel):
    MAX_NUMBER_OF_TRANSACTIONS: ClassVar[int] = 20_000

    header: Header
    transactions: list[Transaction]
    footer: Footer

    @classmethod
    @field_validator("transactions")
    def validate_transactions_counters(
        cls, transactions: list[Transaction]
    ) -> list[Transaction]:
        errors = [
            f"Transaction {i} in order has counter value of {t.counter}."
            for i, t in zip(range(1, len(transactions) + 1), transactions)
            if t.counter != i
        ]
        if errors:
            raise ValueError(errors)
        return transactions

    @model_validator(mode="after")
    def validate_number_of_transactions_matches_total_counter(self):
        transactions = self.transactions
        footer = self.footer

        num_transactions = len(transactions)
        if footer.total_counter != num_transactions:
            raise ValueError(
                f'Total counter "{footer.total_counter}" does not match number of transactions "{num_transactions}".'
            )
        return self

    @model_validator(mode="after")
    def validate_control_sum_equal_to_sum_of_amounts(self):
        transactions = self.transactions
        footer = self.footer

        sum_amounts = sum([t.amount for t in transactions])
        if sum_amounts != footer.control_sum:
            raise ValueError(
                f'Sum of amounts "{sum_amounts}" does not match control sum which is "{footer.control_sum}".'
            )
        return self

    @model_validator(mode="after")
    def validate_number_of_transactions(self):
        transactions = self.transactions
        footer = self.footer

        num_transactions = len(transactions)

        if footer.total_counter != num_transactions:
            raise ValueError(
                f'Total counter "{footer.total_counter}" does not match number of transactions "{num_transactions}".'
            )

        MAX_NUMBER_OF_TRANSACTIONS = StateValidator.MAX_NUMBER_OF_TRANSACTIONS
        if num_transactions > MAX_NUMBER_OF_TRANSACTIONS:
            raise ValueError(
                f'Number of transactions cannot exceed "{MAX_NUMBER_OF_TRANSACTIONS}".'
            )
        return self
