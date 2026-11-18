import click

from terminal_dude.codes.convert import convert
from terminal_dude.codes.create import create
from terminal_dude.codes.show import show
from terminal_dude.codes.update import update


@click.group(invoke_without_command=True)
@click.pass_context
def universe(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(universe.get_help(ctx=ctx))
    else:
        ctx.ensure_object(dict)
        ctx.obj["sheets"] = None
        ctx.obj["worksheets"] = None


universe.add_command(convert)
universe.add_command(create)
universe.add_command(show)
universe.add_command(update)

if __name__ == "__main__":
    # dude()
    universe()
