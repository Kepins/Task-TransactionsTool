import os

from ...model import Model
from ...model.file_components import Header, Transaction, Footer


def create_valid_transactions_file(file_path: str | os.PathLike, num_transactions: int):
    header = Header(
        name="TEST NAME",
        surname="TEST SURNAME",
        patronymic="TEST PATRONYMIC",
        address="TEST ADDRESS",
    )
    transactions = [
        Transaction(counter=i, amount=100 * i, currency="PLN")
        for i in range(1, num_transactions + 1)
    ]
    footer = Footer(
        total_counter=num_transactions,
        control_sum=sum([t.amount for t in transactions]),
    )

    model = Model(file_path)
    model.save_components_to_file(header, transactions, footer)
