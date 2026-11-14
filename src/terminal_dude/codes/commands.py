import click
from gspread import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets, tools


@click.group()
@click.pass_context
def dude(ctx):
    ctx.ensure_object(dict)


# ================================================Create============================================================
@dude.group(
    invoke_without_command=True,
    help="Creating a brand new Spreadsheets file or Worksheets",
)
@click.pass_context
def create(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("...?")
    else:
        pass


@create.command(help="Creating a new Spreadsheets site")
@click.argument("title", type=click.STRING)
def sheet(title):
    try:
        editor = sheets.SheetsEditor()
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


# ================================================Convert============================================================
@dude.group(
    invoke_without_command=True, help="Convert Spreadsheets file into CSV format"
)
@click.pass_context
def convert(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("...?")
    else:
        pass


@convert.command(help="Converting Spreadsheets file into CSV format")
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
@dude.group(invoke_without_command=True, help="Showing visualization of Worksheets")
@click.option("-s", "--stitle", type=click.STRING)
@click.option("-w", "--wstitle", type=click.STRING, required=False)
@click.pass_context
def show(ctx, stitle, wstitle):
    if ctx.invoked_subcommand is None:
        try:
            if wstitle is None:
                editor = sheets.SheetsEditor()
                editor.stitle = stitle
                editor.worksheet_sheet1()
                click.echo(editor.graph)
            else:
                editor = sheets.SheetsEditor()
                editor.stitle = stitle
                editor.wstitle = wstitle
                click.echo(editor.graph)
        except (SpreadsheetNotFound, WorksheetNotFound) as err:
            click.echo(err)

    else:
        ctx.ensure_object(dict)
        ctx.obj["editor"] = sheets.SheetsEditor()
        ctx.obj["sheets"] = stitle
        ctx.obj["worksheets"] = wstitle


@show.command(help="Showing lists of Worksheets")
@click.pass_context
def lists(ctx):
    editor = ctx.obj["editor"]
    editor.stitle = str(ctx.obj["sheets"])
    editor.wstitle = str(ctx.obj["worksheets"])

    click.echo("")
    click.echo(f'Spreadsheets title - "{ctx.obj["sheets"]}"')
    click.echo("")
    for workspace in editor.all_worksheet:
        click.echo(workspace.title)


@show.command(help="Showing lists of rows within index")
@click.argument("index", type=click.STRING)
@click.pass_context
def row(ctx, index):
    editor = ctx.obj["editor"]
    editor.stitle = str(ctx.obj["sheets"])
    editor.wstitle = str(ctx.obj["worksheets"])
    rows = editor.see_rows(index)

    count = 0
    result = ""
    while count < len(rows):
        result += f"{rows[count]:^12.12}" + " | "
        count += 1

    click.echo(result)


@show.command(help="Showing lists of rows within index")
@click.argument("index", type=click.STRING)
@click.pass_context
def column(ctx, index):
    editor = ctx.obj["editor"]
    editor.stitle = str(ctx.obj["sheets"])
    editor.wstitle = str(ctx.obj["worksheets"])
    cols = editor.see_cols(int(index))

    for col in cols:
        click.echo(f"| {col:^12.12} |")


@show.command(help="Showing spesific cells by specified it's cells coordinate")
def cell():
    pass


@show.command(help="Showing current head by meaning it's top of the rows")
def head():
    pass


@show.command(help="Showing the last rows have been insert")
def peek():
    pass


# =================================================Update=============================================================
@dude.group(help="Updating Worksheets cells")
def update():
    pass


@update.command(help="Updating Spreadsheets title")
def spreadsheets():
    pass


@update.command(help="Updating Worksheets title")
def worksheets():
    pass


@update.command(help="Updating spesific style")
def style():
    pass


@update.command(help="Updating specific cells by input the coordinate")
def cells():
    pass


@update.command(help="Updating spesific ranges of rows by input the range")
def ranges():
    pass


if __name__ == "__main__":
    dude()
