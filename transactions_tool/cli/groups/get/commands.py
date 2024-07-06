import click
from click import Context

from .group import get_group
from ....controller import Controller


@get_group.command()
@click.pass_context
def name(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.name)


@get_group.command()
@click.pass_context
def surname(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.surname)


@get_group.command()
@click.pass_context
def patronymic(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.patronymic)


@get_group.command()
@click.pass_context
def address(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.address)


@get_group.command()
@click.argument("idx", type=int)
@click.pass_context
def transaction_amount(ctx: Context, idx: int):
    manager: Controller = ctx.obj["controller"]
    try:
        click.echo(manager.get_transaction_amount(idx))
    except IndexError as e:
        click.echo(e, err=True)


@get_group.command()
@click.argument("idx", type=int)
@click.pass_context
def transaction_currency(ctx: Context, idx: int):
    manager: Controller = ctx.obj["controller"]
    try:
        click.echo(manager.get_transaction_currency(idx))
    except IndexError as e:
        click.echo(e, err=True)


@get_group.command()
@click.pass_context
def total_counter(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.total_counter)


@get_group.command()
@click.pass_context
def control_sum(ctx: Context):
    manager: Controller = ctx.obj["controller"]
    click.echo(manager.control_sum)
