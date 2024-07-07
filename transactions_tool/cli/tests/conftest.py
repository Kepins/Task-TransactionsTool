import os
from dataclasses import dataclass

import pytest


@dataclass
class ValidTransaction:
    counter: int
    amount: int
    currency: str


@dataclass
class ValidTransactionsFile:
    tmp_path: str | os.PathLike
    file_path: str
    name: str
    surname: str
    patronymic: str
    address: str
    transactions: dict[int, ValidTransaction]
    total_counter: int
    control_sum: int


@pytest.fixture
def valid_transaction_file(tmp_path):
    file_name = "test.trans"
    file_path = os.path.join(tmp_path, file_name)

    transactions = {
        1: ValidTransaction(counter=1, amount=200, currency="DOL"),
        2: ValidTransaction(counter=2, amount=400, currency="PLN"),
        3: ValidTransaction(counter=3, amount=137, currency="EUR"),
    }

    fixture = ValidTransactionsFile(
        file_path=file_path,
        tmp_path=tmp_path,
        name="TEST NAME",
        surname="TEST SURNAME",
        patronymic="TEST PATRONYMIC",
        address="TEST ADDRESS",
        transactions=transactions,
        total_counter=3,
        control_sum=transactions[1].amount
        + transactions[2].amount
        + transactions[3].amount,
    )

    header = (
        "01"
        + fixture.name.rjust(28)
        + fixture.surname.rjust(30)
        + fixture.patronymic.rjust(30)
        + fixture.address.rjust(30)
        + "\n"
    )
    transaction_1 = (
        "02"
        + str(fixture.transactions[1].counter).rjust(6, "0")
        + str(fixture.transactions[1].amount).rjust(12, "0")
        + fixture.transactions[1].currency.rjust(3)
        + " " * 97
        + "\n"
    )
    transaction_2 = (
        "02"
        + str(fixture.transactions[2].counter).rjust(6, "0")
        + str(fixture.transactions[2].amount).rjust(12, "0")
        + fixture.transactions[2].currency.rjust(3)
        + " " * 97
        + "\n"
    )
    transaction_3 = (
        "02"
        + str(fixture.transactions[3].counter).rjust(6, "0")
        + str(fixture.transactions[3].amount).rjust(12, "0")
        + fixture.transactions[3].currency.rjust(3)
        + " " * 97
        + "\n"
    )
    footer = (
        "03"
        + str(fixture.total_counter).rjust(6, "0")
        + str(fixture.control_sum).rjust(12, "0")
        + " " * 100
        + "\n"
    )
    with open(file_path, "w") as file:
        file.writelines(
            [
                header,
                transaction_1,
                transaction_2,
                transaction_3,
                footer,
            ]
        )

    return fixture


@pytest.fixture
def valid_transaction_file_max_transactions(tmp_path):
    file_name = "test.trans"
    file_path = os.path.join(tmp_path, file_name)

    transactions = {
        i: ValidTransaction(counter=i, amount=1000, currency="DOL")
        for i in range(1, 20_001)
    }

    fixture = ValidTransactionsFile(
        file_path=file_path,
        tmp_path=tmp_path,
        name="TEST NAME",
        surname="TEST SURNAME",
        patronymic="TEST PATRONYMIC",
        address="TEST ADDRESS",
        transactions=transactions,
        total_counter=20_000,
        control_sum=1000 * 20_000,
    )

    header = (
        "01"
        + fixture.name.rjust(28)
        + fixture.surname.rjust(30)
        + fixture.patronymic.rjust(30)
        + fixture.address.rjust(30)
        + "\n"
    )
    transactions_str = [
        (
            "02"
            + str(t.counter).rjust(6, "0")
            + str(t.amount).rjust(12, "0")
            + t.currency.rjust(3)
            + " " * 97
            + "\n"
        )
        for t in fixture.transactions.values()
    ]

    footer = (
        "03"
        + str(fixture.total_counter).rjust(6, "0")
        + str(fixture.control_sum).rjust(12, "0")
        + " " * 100
        + "\n"
    )
    with open(file_path, "w") as file:
        file.writelines(
            [
                header,
                *transactions_str,
                footer,
            ]
        )

    return fixture
