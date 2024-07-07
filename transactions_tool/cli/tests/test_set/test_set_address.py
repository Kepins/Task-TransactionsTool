from click.testing import CliRunner

from .... import cli


def test_set_address(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "set", "address", "NEW ADDR"],
            obj={},
        )

        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            address = header[90:120].lstrip()

            assert address == "NEW ADDR"


def test_set_address_to_long(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "address",
                "NEW ADDRESS THAT EXCEEDS 30 characters limit",
            ],
            obj={},
        )

        assert result.exit_code == 1
        assert result.output == "String should have at most 30 characters\n"

        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            address = header[90:120].lstrip()

            # Assert not changed
            assert address == valid_transaction_file.address
