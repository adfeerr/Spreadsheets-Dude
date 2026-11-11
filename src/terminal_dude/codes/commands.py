import click
from gspread import GSpreadException, SpreadsheetNotFound

from terminal_dude import sheets, tools


@click.group()
def dude():
    pass


# ================================================Create============================================================
@dude.group(invoke_without_command=True)
@click.pass_context
def create(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("...?")
    else:
        pass


@create.command()
@click.option("-t", "--title", type=click.STRING)
def sheet(title):
    editor = sheets.SheetsEditor()
    editor.stitle = title
    editor.creates(title=title)
    click.echo(f"Sheet '{title}' is created!")


@create.command()
@click.option("-s", "--stitle", type=click.STRING)
@click.option("-w", "--wstitle", type=click.STRING)
def worksheet(stitle, wstitle):
    editor = sheets.SheetsEditor()
    editor.stitle = stitle
    editor.createws(wstitle)
    click.echo(f"Worksheets '{wstitle}' is created!")


# ================================================Convert============================================================
@dude.group(invoke_without_command=True)
@click.pass_context
def convert(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("...?")
    else:
        pass


@convert.command()
@click.option("-s", "--stitle", type=click.STRING)
@click.option("-w", "--wstitle", type=click.STRING)
@click.option("-sft", "--set-title", type=click.STRING, default="FromTerminal.csvv")
def csv(stitle, wstitle, set_title):

    rule = tools.Rules(r"[a-zA-Z0-9]+\.csv")

    if rule.verify(strings=set_title) is True:
        editor = sheets.SheetsEditor()
        editor.stitle = stitle
        editor.wstitle = wstitle
        editor.csv_list(set_title=set_title)
        click.echo(f"'{set_title}' is created!")
    else:
        click.echo(f"Perhaps '{set_title}f' format is not '.csv'")


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
