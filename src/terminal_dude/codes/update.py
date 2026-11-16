import click

# from gspread import SpreadsheetNotFound, WorksheetNotFound
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
        editor.worksheet_sheet1()
        editor.update_stitle(new_title=new_title)
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


@update.command(help="Updating spesific cells")
@click.argument("row", type=click.INT, required=False)
@click.argument("col", type=click.INT, required=False)
@click.argument("value", type=click.STRING, required=False)
@click.option("-n", "--notation", type=click.STRING, required=False)
@click.pass_context
def cell(ctx, row, col, value):
    editor.stitle = ctx.obj["sheets"]
    editor.worksheet_sheet1().update_cell(row=row, col=col, value=value)


@update.command(help="Updating specific range of cells by coordinate range")
@click.pass_context
def cells(ctx):
    pass


@update.command(help="Updating spesific ranges of rows by input the range")
@click.pass_context
def ranges(ctx):
    pass


if __name__ == "__main__":
    pass
