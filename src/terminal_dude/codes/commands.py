import click
from gspread import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets, tools

# Editor
editor = sheets.SheetsEditor()


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
@click.option("-s", "--stitle", type=click.STRING, required=True)
@click.option("-w", "--wstitle", type=click.STRING, required=False)
@click.pass_context
def show(ctx, stitle, wstitle):
    # checked if user isn't invoked the next command
    if ctx.invoked_subcommand is None:
        try:
            # if worksheets title is None, then showing the first sheets graph
            if wstitle is None:
                editor = sheets.SheetsEditor()
                editor.stitle = stitle
                editor.worksheet_sheet1()
                click.echo(editor.graph)
            # if everything is okay, then showing the graph
            else:
                editor = sheets.SheetsEditor()
                editor.stitle = stitle
                editor.wstitle = wstitle
                click.echo(editor.graph)
        except (SpreadsheetNotFound, WorksheetNotFound) as err:
            click.echo(err)

    # if theres a next command invoked, then pass the object to next command
    else:
        ctx.ensure_object(dict)
        editor = sheets.SheetsEditor()
        ctx.obj["editor"] = editor
        ctx.obj["sheets"] = stitle
        ctx.obj["worksheets"] = wstitle


@show.command(help="Showing lists of Worksheets")
@click.pass_context
def lists(ctx):

    # this code simply assuming that previous context is always true
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

    # this code simply assuming that previous context is always true
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

    # this code simply assuming that previous context is always true
    editor = ctx.obj["editor"]
    editor.stitle = str(ctx.obj["sheets"])
    editor.wstitle = str(ctx.obj["worksheets"])
    cols = editor.see_cols(int(index))

    for col in cols:
        click.echo(f"| {col:^12.12} |")


@show.command(help="Showing spesific cells by specified it's cells coordinate")
@click.argument("range", type=click.STRING, default="A1:E6", required=False)
@click.pass_context
def range(ctx, range):
    try:
        # if worksheets is empty, using the first sheets
        if ctx.obj["worksheets"] is None:
            editor = ctx.obj["editor"]
            editor.stitle = str(ctx.obj["sheets"])
            editor.worksheet_sheet1()
            click.echo(editor.get(range))
        # if the condition is okay, using the worksheets that've been inputed
        else:
            editor = ctx.obj["editor"]
            editor.stitle = str(ctx.obj["sheets"])
            editor.wstitle = str(ctx.obj["worksheets"])

            if editor.get(range):
                click.echo(editor.get(range))
            else:
                click.echo(f"Range '{range}' is not a valid coordinate")

    # error situation
    except (SpreadsheetNotFound, WorksheetNotFound) as err:
        # if sheets or worksheets is empty then should show the error
        if ctx.obj["sheets"] or ctx.obj["worksheets"] is None:
            click.echo(err)
        # if everything is okay, using the first worksheet
        else:
            editor = ctx.obj["editor"]
            editor.stitle = str(ctx.obj["sheets"])
            editor.worksheet_sheet1()

            if editor.get(range):
                click.echo(editor.get(range))
            else:
                click.echo(f"Range '{range}' is not a valid coordinate")


@show.command(help="Showing current head by meaning it's top of the rows")
@click.pass_context
def head(ctx):

    # NOT FINISHED
    sheet = str(ctx.obj["sheets"])
    worksheet = str(ctx.obj["worksheets"])

    editor = ctx.obj["editor"]
    editor.stitle = sheet
    editor.wstitle = worksheet

    head = editor.see_rows(1)

    count = 0
    result = ""
    while count < len(head):
        result += f"{head[count]:^12.12}" + " | "
        count += 1

    click.echo(result)


@show.command(help="Showing the last rows have been insert")
@click.pass_context
def peek(ctx):

    # NOT FINISHED
    sheet = str(ctx.obj["sheets"])
    worksheet = str(ctx.obj["worksheets"])

    editor = ctx.obj["editor"]
    editor.stitle = sheet
    editor.wstitle = worksheet
    length = len(editor.get_list)

    click.echo(editor.get_list[length - 1])


# =================================================Update=============================================================


@dude.group(invoke_without_command=True, help="Updating Worksheets cells")
@click.argument("sheets", type=click.STRING, required=False)
@click.argument("new_title", type=click.STRING, required=False)
@click.option("-w", "--worksheets", type=click.STRING, default=False, required=False)
@click.pass_context
def update(ctx, sheets, new_title, worksheets):
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


@update.command(help="Updating spesific style")
@click.pass_context
def style(ctx):
    pass


@update.command(help="Updating specific range of cells by coordinate range")
@click.pass_context
def cells(ctx):
    pass


@update.command(help="Updating spesific cells")
@click.pass_context
def cell(ctx):
    pass


@update.command(help="Updating spesific ranges of rows by input the range")
@click.pass_context
def ranges(ctx):
    pass


if __name__ == "__main__":
    dude()
