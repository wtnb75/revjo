import sys
import json
import functools
from logging import getLogger, basicConfig, INFO, DEBUG
import click
from .version import VERSION
from .revjo import convert

log = getLogger(__name__)


@click.version_option(version=VERSION, prog_name="revjo")
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def set_verbose(flag):
    fmt = '%(asctime)s %(levelname)s %(message)s'
    if flag:
        basicConfig(level=DEBUG, format=fmt)
    else:
        basicConfig(level=INFO, format=fmt)


_cli_option = [
    click.option("--verbose/--no-verbose"),
]


def multi_options(decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def cli_option(func):
    @functools.wraps(func)
    def wrap(verbose, *args, **kwargs):
        set_verbose(verbose)
        return func(*args, **kwargs)
    return multi_options(_cli_option)(wrap)


@cli.command("convert")
@cli_option
@click.option("--input", type=click.File('r'))
@click.argument("data", type=str, default="")
def do_convert(input, data):
    if input is not None:
        d = json.load(input)
    elif data != "":
        d = json.loads(data)
    else:
        d = json.load(sys.stdin)
    click.echo(convert(d))


if __name__ == "__main__":
    cli()
