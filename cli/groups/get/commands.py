import click
from click import Context

from cli.groups.get import get_group
from transactions.file_manager import FileManager


@get_group.command()
@click.pass_context
def name(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.name)


@get_group.command()
@click.pass_context
def surname(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.surname)


@get_group.command()
@click.pass_context
def patronymic(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.patronymic)


@get_group.command()
@click.pass_context
def address(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.address)


@get_group.command()
@click.argument("idx", type=int)
@click.pass_context
def transaction_amount(ctx: Context, idx: int):
    manager: FileManager = ctx.obj["manager"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    click.echo(manager.get_transaction_amount(idx - 1))


@get_group.command()
@click.argument("idx", type=int)
@click.pass_context
def transaction_currency(ctx: Context, idx: int):
    manager: FileManager = ctx.obj["manager"]
    if idx < 1:
        click.echo("TODO")  # TODO
        return
    click.echo(manager.get_transaction_currency(idx - 1))


@get_group.command()
@click.pass_context
def total_counter(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.total_counter)


@get_group.command()
@click.pass_context
def control_sum(ctx: Context):
    manager: FileManager = ctx.obj["manager"]
    click.echo(manager.control_sum)
