from click.testing import CliRunner

from .... import cli


def test_set_control_sum(valid_transaction_file):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=valid_transaction_file.tmp_path):

        result = runner.invoke(
            cli, [valid_transaction_file.file_path, "set", "control-sum", "180"], obj={}
        )
        assert result.exit_code == 2
        assert result.output.split("\n")[-2] == "Error: No such command 'control-sum'."
