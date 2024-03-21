import os.path
from api import GitHubAPI
from flask import send_file
from string import ascii_uppercase
from datetime import datetime
from gen import LRGenerator


class BillDesk:

    def __init__(self) -> None:
        self.data = {}

    def add_company(self, company_name):
        self.data.update({company_name: {}})



class PostLR:
    def __init__(self, data) -> None:
        self.data = data
        self.git = GitHubAPI()

    def get_lr(self):
        
        date = datetime.now().strftime("%d-%m-%Y")

        if not self.git.isexist("LR.txt"):
            self.git.create("LR.txt", f"0-A\n{date}")

        lr_date = self.git.read("LR.txt")
        lr = lr_date.split("\n")[0]
        local_date = lr_date.split("\n")[1]

        if date == local_date:
            num = lr.split("-")[0]
            letter = lr.split("-")[1]
            index = ascii_uppercase.find(letter)
            index += 1
            new_letter = ascii_uppercase[index]
            lr = f"{num}-{new_letter}"
        else:
            num = lr.split("-")[0]
            num = int(num) + 1
            lr = f"{num}-A"

        final = f"{lr}\n{date}"
        self.git.update("LR.txt", str(final))
        return lr


    def check_month(self):
        pass

    def process_lr(self):
        lr = self.get_lr()
        date = datetime.now().strftime("%d-%m-%Y")
        monthname_year = datetime.now().strftime("%b, %Y")
        month_folder = f"/{monthname_year}"
        file = os.path.join(month_folder, f"{lr} {date}")

        self.data.update({"LR": lr})

        if not os.path.exists(month_folder):
            os.makedirs(month_folder)

        generator = LRGenerator(self.data, filename=file)
        generator.generate_invoice()
        return file

