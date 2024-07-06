import click

from transactions import Controller, Model

from .groups.add import add_group
from .groups.set import set_group
from .groups.get import get_group


@click.group()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def cli(ctx, file_path):
    model = Model(file_path)
    ctx.obj["controller"] = Controller(model=model)


cli.add_command(add_group)
cli.add_command(set_group)
cli.add_command(get_group)
