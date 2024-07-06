from click.testing import CliRunner

from .... import cli


def test_set_transaction_amount(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "set", "transaction-amount", "1", "1250"],
            obj={},
        )
        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            lines = file.readlines()
            transaction_1 = lines[1]
            amount = transaction_1[8:20].lstrip("0")

            assert amount == "1250"

            footer = lines[-1]
            control_sum = footer[8:20].lstrip("0")

            previous_amount = valid_transaction_file.transactions[1].amount
            new_amount = 1250
            diff = new_amount - previous_amount

            assert control_sum == str(valid_transaction_file.control_sum + diff)


