import csv

from terminal_dude.auth import client
from terminal_dude.tools import Rules


class SheetsEditor:
    def __init__(self):
        self.sheets = client.get_client()
        self.worksheets = None
        self.__stitle = None
        self.__wstitle = None

    # getter and setter
    @property
    def stitle(self):
        return self.__stitle

    @stitle.setter
    def stitle(self, new_title: str):
        if isinstance(new_title, str):
            self.__stitle = new_title
        else:
            raise TypeError("Spreadsheets title must be a string")

    # getter and setter
    @property
    def wstitle(self):
        return self.__wstitle

    @wstitle.setter
    def wstitle(self, new_title: str):
        if isinstance(new_title, str):
            self.__wstitle = new_title
        else:
            raise TypeError("Worksheets title must be a string")

    # ===============================================Method=====================================================================

    def open(self):
        if not isinstance(self.stitle, str):
            raise TypeError("You need to declare spreadsheets title")

        spreadsheets = self.sheets.open(str(self.stitle))
        return spreadsheets

    def worksheet(self):
        if not isinstance(self.wstitle, str):
            raise TypeError("You need to declare worksheets title")

        worksheets = self.open().worksheet(str(self.wstitle))
        return worksheets

    def creates(self, title: str):
        self.sheets.create(title=title)

    def createws(self, title: str, rows: int = 100, cols: int = 26):
        self.open().add_worksheet(title=title, rows=rows, cols=cols)

    # This delete method is confusing in the original documentation
    def deletews(self, title):
        self.open().del_worksheet(title)

    def update_stitle(self, new_title: str):
        self.open().update_title(new_title)

    def update_wstitle(self, new_title: str):
        self.worksheet().update_title(new_title)

    def see_rows(self, index: int):
        return self.worksheet().row_values(index)

    def see_cols(self, index: int):
        return self.worksheet().col_values(index)

    def find(self, value: str):
        self.worksheet().find(value)

    @property
    def get_list(self):
        return self.worksheet().get_all_values()

    @property
    def get_dict(self):
        return self.worksheet().get_all_records()

    def insert(self, list_of_value: list, position: str):
        rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")
        if rules.verify(strings=position) is True:
            self.worksheet().append_row(values=list_of_value, table_range=position)
        else:
            return False

    def get(self, position: str):
        rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")
        if rules.verify(strings=position) is True:
            self.worksheet().get(position)
            return True
        else:
            return False

    def csv_list(self, set_title: str):
        rules = Rules(r"[a-zA-Z0-9]+\.csv")
        if rules.verify(strings=set_title) is True:
            with open(set_title, "w", newline="") as csv_files:
                csv_write = csv.writer(csv_files)

                for row in self.get_list:
                    csv_write.writerow(row)

            return True
        else:
            raise TypeError("Please write '.csv' files")

    def graph(self):
        result = ""
        count = 0

        while count < self.get_list[0][0]:
            pass


if __name__ == "__main__":
    editor = SheetsEditor()
    editor.stitle = "LearnCLI"
    editor.wstitle = "From Class"
    editor.graph()
