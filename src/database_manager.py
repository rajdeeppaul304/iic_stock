from os import path
import json

class Database():
    def __init__(self, file:str) -> None:
        self.file = file
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

    def buy_stocks(self, email:str, stock_id:int, amount:int):
        stock_id_str = str(stock_id)

        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if user_data_dict.get(email):
            if not user_data_dict[email]["stocks"].get(stock_id_str):
                user_data_dict[email]["stocks"][stock_id_str] = amount
            else:
                user_data_dict[email]["stocks"][stock_id_str] += amount

            print(user_data_dict)
            with open(self.file, "w") as database:
                user_data_dict = json.dump(user_data_dict, database)


    def dump_data(self):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        json.dumps(user_data_dict, indent=4)
