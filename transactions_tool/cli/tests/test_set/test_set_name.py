from click.testing import CliRunner

from .... import cli


def test_set_name(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli, [valid_transaction_file.file_path, "set", "name", "NEW NAME"], obj={}
        )

        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            name = header[2:30].lstrip()

            assert name == "NEW NAME"


def test_set_name_to_long(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "name",
                "NEW NAME THAT EXCEEDS 28 characters limit",
            ],
            obj={},
        )

        assert result.exit_code == 1
        assert result.output == "String should have at most 28 characters\n"

        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            name = header[2:30].lstrip()

            # Assert not changed
            assert name == valid_transaction_file.name
