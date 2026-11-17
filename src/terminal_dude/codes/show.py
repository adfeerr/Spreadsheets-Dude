import click
from gspread import SpreadsheetNotFound, WorksheetNotFound

from terminal_dude import sheets

# Initialize Global Editor
global_edit = sheets.SheetsEditor()


@click.group(invoke_without_command=True, help="Showing visualization of Worksheets")
@click.option("-s", "--sheet", type=click.STRING, required=True)
@click.option("-w", "--worksheet", type=click.STRING, required=False, default=None)
@click.pass_context
def show(ctx, sheet, worksheet):

    # If command just only call "show", then run this condition
    if ctx.invoked_subcommand is None:
        editor = global_edit

        try:
            # If worksheet isn't invoked, then choose worksheet 1 as a default..
            # ..to show it to the terminal
            if worksheet is None:
                editor.stitle = sheet
                click.echo(editor.graph)
            # else, using choosen worksheet to show
            else:
                editor.stitle = sheet
                editor.wstitle = worksheet
                click.echo(editor.graph)

        except (SpreadsheetNotFound, WorksheetNotFound) as error:
            click.echo(f"Error: {error}")

    # Else, pass this command value to another subcommand
    else:
        ctx.obj["sheets"] = sheet
        ctx.obj["worksheets"] = worksheet


@show.command(help="Showing lists of Worksheets")
@click.pass_context
def lists(ctx):
    editor = global_edit
    sheet = ctx.obj["sheets"]

    try:
        editor.stitle = sheet

        click.echo("")
        click.echo(f'Spreadsheets title - "{ctx.obj["sheets"]}"')
        click.echo("")

        # Showing all worksheets the current spreadsheets had
        for workspace in editor.all_worksheet:
            click.echo(workspace.title)

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


@show.command(help="Showing lists of rows within index")
@click.argument("index", type=click.INT)
@click.pass_context
def row(ctx, index):
    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        # If worksheet is empty, then set this condition
        if worksheet is None:
            editor.stitle = sheet
        # Else, set some condition
        else:
            editor.stitle = sheet
            editor.wstitle = worksheet

        rows = editor.see_rows(index)
        count = 0
        result = ""

        while count < len(rows):
            result += f"{rows[count]:^12.12}" + " | "
            count += 1

        # Showing the result
        click.echo(result)

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


@show.command(help="Showing lists of rows within index")
@click.argument("index", type=click.INT)
@click.pass_context
def column(ctx, index):
    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        # If worksheet is empty, set this condition
        if worksheet is None:
            editor.stitle = sheet
        # Else, set this condition
        else:
            editor.stitle = sheet
            editor.wstitle = worksheet

        cols = editor.see_cols(index)

        # Showing the result
        for col in cols:
            click.echo(f"| {col:^12.12} |")

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


# I need regex for this kinda thing
@show.command(help="Showing spesific cells by specified it's cells coordinate")
@click.argument("range", type=click.STRING, default="A1:E3", required=False)
@click.pass_context
def range(ctx, range):
    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        # if worksheets is empty, using the first sheets
        if worksheet is None:
            editor.stitle = sheet
            # click.echo(editor.get(range))
        # if the condition is okay, using the worksheets that've been inputed
        else:
            editor.stitle = sheet
            editor.wstitle = worksheet

        if editor.get(range):
            lists = editor.get(range)
            result = ""
            line = f"{'_' * (16 * (len(lists[0])) + (3 * len(lists[0]) - 1))}"
            seperator = " | "
            indent_2 = "  "

            result += indent_2 + line + "\n"

            for item in lists:
                count = 0

                while count != len(lists[0]):
                    if item[count] == "":
                        result += seperator + f"{'-':<16.16}"
                        count += 1
                    else:
                        result += seperator + f"{item[count]:<16.16}"
                        count += 1

                result += seperator + "\n"
                if item[0] == lists[0][0]:
                    # while count != len(lists[0]):
                    result += " "
                    result += f"|{'_' * 18}" * len(lists[0])
                    result += "|\n"

            result += " "
            result += f"|{'_' * 18}" * len(lists[0])
            result += "|\n"

            click.echo(result)

        elif editor.get(range) is False:
            click.echo(f"Range '{range}' is not a valid coordinate")
        else:
            click.echo("Error: unknown given command")

    # error situation
    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


@show.command(help="Showing current head by meaning it's top of the rows")
@click.pass_context
def head(ctx):
    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        if worksheet is None:
            editor.stitle = sheet
        else:
            editor.stitle = sheet
            editor.wstitle = worksheet

        head = editor.see_rows(1)

        count = 0
        result = ""
        while count < len(head):
            result += f"{head[count]:^12.12}" + " | "
            count += 1

        click.echo(result)

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


@show.command(help="Showing the last rows have been insert")
@click.pass_context
def peek(ctx):
    editor = global_edit
    sheet = ctx.obj["sheets"]
    worksheet = ctx.obj["worksheets"]

    try:
        if worksheet is None:
            editor.stitle = sheet
        else:
            editor.stitle = sheet
            editor.wstitle = worksheet

        length = len(editor.get_list)
        data = editor.get_list[length - 1]

        count = 0
        result = ""
        while count < len(data):
            result += f"{data[count]:^12.12}" + " | "
            count += 1

        click.echo(result)

    except (SpreadsheetNotFound, WorksheetNotFound) as error:
        click.echo(f"Error: {error}")


if __name__ == "__main__":
    pass
