import click
from click import Context

from cli.groups.set import set_group
from transactions.file_manager import FileManager


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def name(ctx: Context, value: str):
    manager: FileManager = ctx.obj["manager"]
    manager.name = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def surname(ctx: Context, value: str):
    manager: FileManager = ctx.obj["manager"]
    manager.surname = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def patronymic(ctx: Context, value: str):
    manager: FileManager = ctx.obj["manager"]
    manager.patronymic = value


@set_group.command()
@click.pass_context
@click.argument("value", type=str)
def address(ctx: Context, value: str):
    manager: FileManager = ctx.obj["manager"]
    manager.address = value


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=int)
@click.pass_context
def transaction_amount(ctx: Context, idx:int, value: int):
    manager: FileManager = ctx.obj["manager"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    manager.set_transaction_amount(idx - 1, value)


@set_group.command()
@click.argument("idx", type=int)
@click.argument("value", type=str)
@click.pass_context
def transaction_currency(ctx: Context, idx: int, value: str):
    manager: FileManager = ctx.obj["manager"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    manager.set_transaction_currency(idx - 1, value)
