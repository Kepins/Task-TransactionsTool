import click
from click import Context

from cli.groups.add import add_group
from transactions.controller.controller import Controller


@add_group.command()
@click.pass_context
@click.argument("amount", type=int)
@click.argument("currency", type=str)
def transaction(ctx: Context, amount: int, currency: str):
    manager: Controller = ctx.obj["controller"]
    manager.add_transaction(amount=amount, currency=currency)
