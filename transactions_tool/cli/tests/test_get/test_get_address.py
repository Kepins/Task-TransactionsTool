from click.testing import CliRunner

from .... import cli


def test_get_address(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli, [valid_transaction_file.file_path, "get", "address"], obj={}
        )
        assert result.exit_code == 0
        assert result.output == f"{valid_transaction_file.address}\n"
