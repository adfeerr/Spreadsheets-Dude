import click
from gspread import SpreadsheetNotFound

from terminal_dude import sheets

# Editor
editor = sheets.SheetsEditor()


@click.group(
    invoke_without_command=True,
    help="Creating a brand new Spreadsheets file or Worksheets",
)
@click.pass_context
def create(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(create.get_help(ctx))
    else:
        pass


@create.command(help="Creating a new Spreadsheets site")
@click.argument("title", type=click.STRING)
def sheet(title):
    editor.stitle = title
    editor.create_sheet(title=title)
    click.echo(f"Sheet '{title}' is created!")


@create.command(help="Creating a new Worksheets sheets")
@click.argument("sheet", type=click.STRING)
@click.argument("worksheet", type=click.STRING)
def worksheet(sheet, worksheet):
    try:
        editor = sheets.SheetsEditor()
        editor.stitle = sheet
        editor.create_worksheet(worksheet)
        click.echo(f"Worksheets '{worksheet}' is created!")
    except SpreadsheetNotFound:
        click.echo("Error: response is okay, but spreadsheet is not found")


if __name__ == "__main__":
    pass
