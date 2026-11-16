import click
from gspread import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets

# Editor
editor = sheets.SheetsEditor()


@click.group(
    invoke_without_command=True,
    help="Creating a brand new Spreadsheets file or Worksheets",
)
@click.pass_context
def create(ctx):
    click.echo(create.get_help(ctx))


@create.command(help="Creating a new Spreadsheets site")
@click.argument("title", type=click.STRING)
@click.pass_context
def sheet(ctx, title):
    try:
        # basic spreadsheets creation
        editor.stitle = title
        editor.creates(title=title)
        click.echo(f"Sheet '{title}' is created!")
    except SpreadsheetNotFound as err:
        click.echo(err)


@create.command(help="Creating a new Worksheets sheets")
@click.option("-s", "--stitle", type=click.STRING)
@click.option("-w", "--wstitle", type=click.STRING)
def worksheet(stitle, wstitle):
    try:
        editor = sheets.SheetsEditor()
        editor.stitle = stitle
        editor.createws(wstitle)
        click.echo(f"Worksheets '{wstitle}' is created!")
    except (SpreadsheetNotFound, WorksheetNotFound) as err:
        click.echo(err)


if __name__ == "__main__":
    pass
