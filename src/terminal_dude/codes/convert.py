import click

from terminal_dude import sheets, tools

# Editor
editor = sheets.SheetsEditor()


@click.group(
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
@click.option("-sft", "--set-title", type=click.STRING, default="FromTerminal.csv")
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


if __name__ == "__main__":
    pass
