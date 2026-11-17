import click

# from gspread import SpreadsheetNotFound, WorksheetNotFound
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets

# Editor
editor = sheets.SheetsEditor()


@click.group(invoke_without_command=True, help="Updating Worksheets cells")
@click.option("-s", "--sheets", type=click.STRING, required=True)
@click.option("-w", "--worksheets", type=click.STRING, default=False, required=False)
@click.option("-nt", "new_title", type=click.STRING, required=False)
@click.pass_context
def update(ctx, sheets, worksheets, new_title):

    if ctx.invoked_subcommand is None:
        editor.stitle = sheets
        editor.worksheet1()
        editor.update_sheet_title(new_title=new_title)
        click.echo(f"Spreadsheets name changed from: '{sheets}' --> '{new_title}'")

    else:
        ctx.obj["sheets"] = sheets
        if worksheets:
            ctx.obj["worksheets"] = worksheets
        else:
            ctx.obj["worksheets"] = False


# @update.command(help="Updating spesific style")
# @click.pass_context
# def style(ctx):
#     editor.stitle = ctx.obj["sheets"]


@update.command(invoke_without_command=True, help="Updating Worksheets name")
@click.argument("current", type=click.STRING, required=True)
@click.argument("new", type=click.STRING, default="Untitled - CLI", required=False)
@click.pass_context
def worksheets(ctx, current, new):
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    if worksheet is False:
        editor.stitle = sheet
        editor.wstitle = current
        editor.update_worksheet_title(new)
        click.echo(f"'{current}' ---> '{new}'")
    else:
        editor.stitle = sheet
        editor.worksheet1()
        editor.update_worksheet_title(new)
        click.echo(f"'[FIRST]' ---> '{new}'")


@update.command(help="Updating spesific cells")
@click.argument("row", type=click.INT, required=False)
@click.argument("col", type=click.INT, required=False)
@click.option("-val", "--value", type=click.STRING, required=False)
@click.pass_context
def cell(ctx, row: int, col: int, value, notation: bool, notation_value):
    editor.stitle = ctx.obj["sheets"]
    editor.worksheet1().update_cell(row=row, col=col, value=value)


@update.command(help="Updating specific range of cells by coordinate range")
@click.argument("cell_coor", type=click.STRING)
@click.argument("value", type=click.STRING)
@click.pass_context
def cells(ctx, cell_coor, value):
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        if worksheet is True:
            editor.stitle = sheet
            editor.wstitle = str(worksheet)
            editor.open_worksheet.update_acell(cell_coor, value=value)
        elif worksheet is False:
            editor.stitle = sheet
            editor.worksheet1()
            editor.open_worksheet.update_acell(cell_coor, value=value)
        else:
            click.echo("do this")
    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(error)


@update.command(help="Updating spesific ranges of rows by input the range")
# i still don't know how should i set the default "value" params
@click.argument("value")  # i think it is string
@click.argument("cell", type=click.STRING)
@click.pass_context
def ranges(ctx, value: list, cell: str):
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        if worksheet is True:
            editor.stitle = sheet
            editor.wstitle = str(worksheet)
            editor.open_worksheet.update(values=value, range_name=cell)
        elif worksheet is False:
            editor.stitle = sheet
            editor.worksheet1()
            editor.open_worksheet.update(values=value, range_name=cell)
        else:
            click.echo("do this")
    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(error)


if __name__ == "__main__":
    pass
