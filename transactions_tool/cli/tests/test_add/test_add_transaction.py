from click.testing import CliRunner

from .... import cli


def test_add_transaction(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "add", "transaction", "1000", "DOL"],
            obj={},
        )
        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            lines = file.readlines()
            new_transaction = lines[-2]

            t_id = new_transaction[0:2]
            t_counter = new_transaction[2:8].lstrip("0")
            t_amount = new_transaction[8:20].lstrip("0")
            t_currency = new_transaction[20:23].lstrip()
            t_reserved = new_transaction[23:120]

            previous_total_counter = valid_transaction_file.total_counter + 1
            previous_control_sum = valid_transaction_file.control_sum

            assert t_id == "02"
            assert t_counter == str(previous_total_counter)
            assert t_amount == "1000"
            assert t_currency == "DOL"
            assert t_reserved == " " * 97

            new_footer = lines[-1]

            f_id = new_footer[0:2]
            f_total_counter = new_footer[2:8].lstrip("0")
            f_control_sum = new_footer[8:20].lstrip("0")
            f_reserved = " " * 100

            assert f_id == "03"
            assert f_total_counter == str(previous_total_counter)
            assert f_control_sum == str(previous_control_sum + 1000)
            assert f_reserved == " " * 100


def test_add_transaction_to_big_amount(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "add",
                "transaction",
                "100000000000000",
                "DOL",
            ],
            obj={},
        )
        assert result.exit_code == 1
        assert result.output == "Input should be less than or equal to 999999999999\n"


def test_add_transaction_wrong_currency(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "add", "transaction", "1000", "YEN"],
            obj={},
        )
        assert result.exit_code == 1
        assert result.output == "Input should be 'DOL', 'PLN' or 'EUR'\n"


def test_add_transaction_control_sum_exceeds_limit(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "add",
                "transaction",
                "999999999999",
                "DOL",
            ],
            obj={},
        )
        assert result.exit_code == 1
        assert (
            result.output == "After transaction sum of amounts exceeds 999999999999\n"
        )


def test_max_num_transactions(valid_transaction_file_max_transactions):
    runner = CliRunner()
    with runner.isolated_filesystem(
        temp_dir=valid_transaction_file_max_transactions.tmp_path
    ):
        result = runner.invoke(
            cli,
            [
                valid_transaction_file_max_transactions.file_path,
                "add",
                "transaction",
                "1000",
                "DOL",
            ],
            obj={},
        )
        assert result.exit_code == 1
        assert result.output == "Max number of transactions equal to 20000 reached\n"
