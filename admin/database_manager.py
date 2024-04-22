from os import path
import json

from flask_login import UserMixin

class Database():
    def __init__(self, file:str, stocks_file:str) -> None:
        self.file = file
        self.stocks_file = stocks_file
        if not path.exists(file):
            open(file, "w").close()

    # whats hashing?
    def add_user(self, name:str, email:str, password:str, intial_balance:float):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if not user_data_dict.get(email):
            user_data_dict[email] = {"name":name, "password":password, "balance":intial_balance}

            with open(self.file, "w") as database:
                json.dump(user_data_dict, database)

    def add_balance(self, email:str, extra_balance:int):
        user_data_dict = self.get_users()
        user_data_dict[email]["balance"] += extra_balance

        user_data_dict[email]["balance"] = user_data_dict[email]["balance"] if user_data_dict[email]["balance"] >= 0 else 0
        print(user_data_dict)
            
        with open(self.file, "w") as database:
            json.dump(user_data_dict, database)

    def update_stocks(self, stock_id_str:str, new_price:int) -> bool:
        stocks = self.get_stocks()[stock_id_str]
        return False

    def reset(self, email:str):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if user_data_dict.get(email):
            user_data_dict[email]["balance"] = 10000
            user_data_dict[email]["stocks"] = {}

            with open(self.file, "w") as database:
                json.dump(user_data_dict, database)

        else: print("could not find user")

    def get_stocks(self) -> dict:
        with open(self.stocks_file) as stocks:
            stocks_dict = json.load(stocks)

        return stocks_dict

    def get_users(self, no_pass=False) -> dict:
        with open(self.file) as stocks:
            user_data_dict = json.load(stocks)

        if no_pass:
            for user_data in user_data_dict.values():
                del user_data["password"]

        return user_data_dict

    def dump_data(self):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)
        
        print(json.dumps(user_data_dict, indent=4))

