import click

from transactions import FileController

from .groups.add import add_group
from .groups.set import set_group
from .groups.get import get_group


@click.group()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def cli(ctx, file_path):
    ctx.obj["controller"] = FileController(file_path)


cli.add_command(add_group)
cli.add_command(set_group)
cli.add_command(get_group)
