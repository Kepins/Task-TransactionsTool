import functools
import sys

import click
from pydantic import ValidationError


def click_error_wrapper(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            if len(e.errors()) == 1:
                click.echo(e.errors()[0]["msg"], err=True)
                sys.exit(1)
            click.echo("Errors:", err=True)
            for err in e.errors():
                click.echo(err["msg"], err=True)
        except ValueError as e:
            click.echo(e, err=True)
            sys.exit(1)

    return wrapped_func
