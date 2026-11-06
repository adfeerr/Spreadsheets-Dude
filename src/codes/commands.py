import click
import sheets
from gspread import GSpreadException, SpreadsheetNotFound


@click.group()
def dude():
    pass


# ================================================Create============================================================
@dude.group(invoke_without_command=True)
@click.pass_context
def create(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Execute here")
    else:
        pass


@create.command()
@click.option("-s", "--stitle", type=click.STRING)
def sheet(stitle):
    editor = sheets.SheetsEditor()
    editor.stitle = stitle
    editor.creates(title=stitle)
    click.echo(f"Sheet '{stitle}' is created!")


@create.command()
@click.option("-s", "--stitle", type=click.STRING)
@click.option("-w", "--wstitle", type=click.STRING)
def worksheets(stitle, wstitle):
    editor = sheets.SheetsEditor()
    editor.stitle = stitle
    editor.createws(wstitle)
    click.echo(f"Worksheets '{wstitle}' is created!")


# ================================================Convert============================================================
@dude.command()
def convert():
    pass


# ==================================================Show==============================================================
@dude.command()
def show():
    pass


# =================================================Update=============================================================
@dude.command()
def update():
    pass


if __name__ == "__main__":
    dude()
