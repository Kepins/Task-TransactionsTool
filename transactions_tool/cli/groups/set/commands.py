import click
from click import Context

from .group import set_group
from ..error_wrapper import click_error_wrapper
from ....controller import Controller


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
@click_error_wrapper
def name(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.name = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
@click_error_wrapper
def surname(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.surname = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
@click_error_wrapper
def patronymic(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.patronymic = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
@click_error_wrapper
def address(ctx: Context, value: str):
    manager: Controller = ctx.obj["controller"]
    manager.address = value


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=int)
@click.pass_context
@click_error_wrapper
def transaction_amount(ctx: Context, idx: int, value: int):
    manager: Controller = ctx.obj["controller"]
    try:
        click.echo(manager.set_transaction_amount(idx, value))
    except IndexError as e:
        click.echo(e, err=True)


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=str)
@click.pass_context
@click_error_wrapper
def transaction_currency(ctx: Context, idx: int, value: str):
    manager: Controller = ctx.obj["controller"]
    try:
        click.echo(manager.set_transaction_currency(idx, value))
    except IndexError as e:
        click.echo(e, err=True)
