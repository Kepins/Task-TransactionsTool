import sys

import click
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from ..model import Model
from ..controller import Controller

from .groups.add import add_group
from .groups.set import set_group
from .groups.get import get_group


@click.group()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def cli(ctx, file_path):
    try:
        model = Model(file_path)
        ctx.obj["controller"] = Controller(model=model)
    except ValidationError as e:
        click.echo("File is in invalid state:", err=True)
        for err in e.errors():
            click.echo(err["msg"], err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo("File is in invalid state:", err=True)
        click.echo(e, err=True)
        sys.exit(1)


cli.add_command(add_group)
cli.add_command(set_group)
cli.add_command(get_group)
