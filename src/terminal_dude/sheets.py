import csv
from pathlib import Path

from gspread.exceptions import WorksheetNotFound

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

    @property
    def open_sheet(self):
        if not isinstance(self.stitle, str):
            raise TypeError("Spreadsheets title it's either None or not a String")
        else:
            spreadsheets = self.sheets.open(str(self.stitle))
            return spreadsheets

    @property
    def open_worksheet(self):
        try:
            if isinstance(self.wstitle, str):
                ws = self.open_sheet.worksheet(str(self.wstitle))
                return ws
            else:
                return self.open_sheet.sheet1
        except WorksheetNotFound:
            return self.open_sheet.sheet1

    # def worksheet1(self):
    #     return self.open_sheet.sheet1

    def create_sheet(self, title: str):
        self.sheets.create(title=title)

    def create_worksheet(self, title: str, rows: int = 100, cols: int = 26):
        self.open_sheet.add_worksheet(title=title, rows=rows, cols=cols)

    # This delete method is confusing in the original documentation
    def del_worksheet(self, title):
        self.open_sheet.del_worksheet(title)

    def update_sheet_title(self, new_title: str):
        self.open_sheet.update_title(new_title)

    def update_worksheet_title(self, new_title: str):
        self.open_worksheet.update_title(new_title)

    def see_rows(self, index: int):
        return self.open_worksheet.row_values(index)

    def see_cols(self, index: int):
        return self.open_worksheet.col_values(index)

    def find(self, value: str):
        self.open_worksheet.find(value)

    def get(self, position: str):
        rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")
        if rules.verify(strings=position) is True:
            return list(self.open_worksheet.get(position))
        else:
            return False

    @property
    def get_list(self):
        return self.open_worksheet.get_all_values()

    @property
    def get_dict(self):
        return self.open_worksheet.get_all_records()

    def insert(self, list_of_value: list, position: str):
        rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")
        if rules.verify(strings=position) is True:
            self.open_worksheet.append_row(values=list_of_value, table_range=position)
        else:
            return False

    def csv_list(self, set_title: str):
        rules = Rules(r"[a-zA-Z0-9]+\.csv")

        if rules.verify(strings=set_title) is True:
            DIR = Path.cwd()
            DEST = DIR / set_title
            with open(DEST, "w", newline="") as csv_files:
                csv_write = csv.writer(csv_files)

                for row in self.get_list:
                    csv_write.writerow(row)

            return True
        else:
            raise TypeError("Please write '.csv' files")

    @property
    def graph(self):
        lists = self.get_list
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

        return result

    def share(self, account: str, permission: str, roles: str):
        pass

    @property
    def all_worksheet(self) -> list:
        worksheets = self.open_sheet.worksheets()
        return worksheets


if __name__ == "__main__":
    editor = SheetsEditor()
    editor.stitle = "LearnCLI"
    editor.wstitle = "test"
    print(editor.wstitle)
    print(editor.graph)

    # print(editor.all_worksheet)
