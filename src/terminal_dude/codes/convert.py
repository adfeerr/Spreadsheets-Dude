from pathlib import Path

import click
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets, tools

# Editor
global_edit = sheets.SheetsEditor()


@click.group(
    invoke_without_command=True, help="Convert Spreadsheets file into CSV format"
)
@click.option("-s", "--sheet", type=click.STRING)
@click.option("-w", "--worksheet", type=click.STRING)
@click.option("-sft", "--set-title", type=click.STRING, default="FromTerminal.csv")
@click.pass_context
def convert(ctx, sheet, worksheet, set_title):
    if ctx.invoked_subcommand is None:
        click.echo(convert.get_help(ctx=ctx))
    else:
        ctx.obj["sheets"] = sheet
        ctx.obj["worksheets"] = worksheet
        ctx.obj["set_title"] = set_title


@convert.command(help="Converting Spreadsheets file into CSV format")
@click.pass_context
def csv(ctx):

    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]
    set_title = ctx.obj["set_title"]

    file = Path.cwd() / str(set_title)

    try:
        rule = tools.Rules(r"[a-zA-Z0-9]+\.csv")

        if rule.verify(strings=set_title) is True:
            if worksheet is None:
                editor.stitle = sheet
            else:
                editor.stitle = sheet
                editor.wstitle = worksheet

            editor.csv_list(set_title=set_title)
            click.echo(f"'{set_title}' is created!")
        else:
            click.echo(f"'{set_title}f' is not '.csv' file")

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


if __name__ == "__main__":
    pass
