from click.testing import CliRunner

from .... import cli


def test_set_patronymic(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):
        result = runner.invoke(
            cli,
            [valid_transaction_file.file_path, "set", "patronymic", "NEW PATRONYMIC"],
            obj={},
        )

        assert result.exit_code == 0
        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            patronymic = header[60:90].lstrip()

            assert patronymic == "NEW PATRONYMIC"


def test_set_patronymic_to_long(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli,
            [
                valid_transaction_file.file_path,
                "set",
                "patronymic",
                "NEW PATRONYMIC THAT EXCEEDS 30 characters limit",
            ],
            obj={},
        )

        assert result.exit_code == 1
        assert result.output == "String should have at most 30 characters\n"

        with open(valid_transaction_file.file_path, "r") as file:
            header = file.readline()
            patronymic = header[60:90].lstrip()

            # Assert not changed
            assert patronymic == valid_transaction_file.patronymic
