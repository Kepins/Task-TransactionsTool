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
