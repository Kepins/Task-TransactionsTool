import click
from click import Context

from .group import set_group
from ....controller import Controller


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def name(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.name = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def surname(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.surname = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def patronymic(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.patronymic = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def address(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.address = value


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=int)
@click.pass_context
def transaction_amount(ctx: Context, idx: int, value: int):
    manager: Controller = ctx.obj["controller"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    manager.set_transaction_amount(idx - 1, value)


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=str)
@click.pass_context
def transaction_currency(ctx: Context, idx: int, value: str):
    manager: Controller = ctx.obj["controller"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    manager.set_transaction_currency(idx - 1, value)
