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
