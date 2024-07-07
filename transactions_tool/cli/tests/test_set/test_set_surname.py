from click.testing import CliRunner

from .... import cli


def test_set_surname(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "set", "surname", "NEW SURNAME"],
            obj={},
        )

        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            surname = header[30:60].lstrip()

            assert surname == "NEW SURNAME"


def test_set_surname_to_long(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "surname",
                "NEW SURNAME THAT EXCEEDS 30 characters limit",
            ],
            obj={},
        )

        assert result.exit_code == 1
        assert result.output == "String should have at most 30 characters\n"

        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            surname = header[30:60].lstrip()

            # Assert not changed
            assert surname == valid_transaction_file.surname
