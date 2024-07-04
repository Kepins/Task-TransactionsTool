import click

from cli.groups.add import add_group
from cli.groups.set import set_group
from cli.groups.get import get_group
from transactions.file_manager import FileManager


@click.group()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def cli(ctx, file_path):
    ctx.obj["manager"] = FileManager(file_path)


cli.add_command(add_group)
cli.add_command(set_group)
cli.add_command(get_group)
