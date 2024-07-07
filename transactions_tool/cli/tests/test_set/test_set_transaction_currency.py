from click.testing import CliRunner

from .... import cli


def test_set_transaction_currency(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "transaction-currency",
                "1",
                "EUR",
            ],
            obj={},
        )
        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            lines = file.readlines()
            transaction_1 = lines[1]
            currency = transaction_1[20:23].lstrip()

            assert currency == "EUR"


def test_set_transaction_currency_invalid(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "transaction-currency",
                "1",
                "YEN",
            ],
            obj={},
        )

        assert result.exit_code == 1
        assert result.output == "Input should be 'DOL', 'PLN' or 'EUR'\n"

        with open(valid_transaction_file.file_path, "r") as file:
            lines = file.readlines()
            transaction_1 = lines[1]
            currency = transaction_1[20:23].lstrip()

            assert currency == valid_transaction_file.transactions[1].currency
