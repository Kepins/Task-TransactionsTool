import click
from click import Context

from .group import add_group
from ..error_wrapper import click_error_wrapper
from ....controller import Controller


@add_group.command()
@click.pass_context
@click.argument("amount", type=int)
@click.argument("currency", type=str)
@click_error_wrapper
def transaction(ctx: Context, amount: int, currency: str):
    manager: Controller = ctx.obj["controller"]
    manager.add_transaction(amount=amount, currency=currency)
