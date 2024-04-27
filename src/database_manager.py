import os
# from os import path
import json

from flask_login import UserMixin

class Database():
    def __init__(self, file:str, stocks_file:str) -> None:
        self.file = file
        self.stocks_file = stocks_file
        if not os.path.exists(file):
            open(file, "w").close()

    # whats hashing?
    def add_user(self, name:str, email:str, password:str, intial_balance:float):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if not user_data_dict.get(email):
            user_data_dict[email] = {"name":name, "password":password, "balance":intial_balance}

            with open(self.file, "w") as database:
                json.dump(user_data_dict, database)

    def buy_stocks(self, email:str, stock_id:int, amount:int) -> bool:
        stock_id_str = str(stock_id)
        
        with open(self.stocks_file, "r") as stocks:
            stock_price = json.load(stocks)[stock_id_str]["amount"]

        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if user_data_dict.get(email):
            if not user_data_dict[email]["stocks"].get(stock_id_str):
                user_data_dict[email]["stocks"][stock_id_str] = amount
            else:
                user_data_dict[email]["stocks"][stock_id_str] += amount
            
            user_data_dict[email]["balance"] -= amount * stock_price

            if user_data_dict[email]["balance"] < 0:
                return False

            if not os.path.exists("transaction.lock"):
                open("transaction.lock", "w").close()
                with open(self.file, "w") as database:
                    json.dump(user_data_dict, database)
                os.remove("transaction.lock")

            else:
                return False

        return True

    def sell_stocks(self, email:str, stock_id:int, amount:int) -> bool:
        stock_id_str = str(stock_id)
        
        with open(self.stocks_file, "r") as stocks:
            stock_price = json.load(stocks)[stock_id_str]["amount"]

        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if user_data_dict.get(email):
            print("stocks and amount",user_data_dict[email]["stocks"][stock_id_str], amount)
            if not user_data_dict[email]["stocks"].get(stock_id_str):
                print("no stocks owned")
                return False

            else:
                user_data_dict[email]["stocks"][stock_id_str] -= amount
            
            user_data_dict[email]["balance"] += amount * stock_price

            if user_data_dict[email]["stocks"][stock_id_str] < 0:
                print("not enought stocks")
                return False

            if not os.path.exists("transaction.lock"):
                open("transaction.lock", "w").close()
                with open(self.file, "w") as database:
                    json.dump(user_data_dict, database)
                os.remove("transaction.lock")

            else:
                return False

        return True

    def save_data(self, user_data_dict:dict):
        if not os.path.exists("transaction.lock"):
            open("transaction.lock", "w").close()
            with open(self.file, "w") as database:
                json.dump(user_data_dict, database)
            os.remove("transaction.lock")

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

    def get_users(self, no_pass=True) -> dict:
        with open(self.file) as stocks:
            user_data_dict = json.load(stocks)

        if no_pass:
            for user_data in user_data_dict.values():
                user_data.pop("password", None)
                # del user_data["password"]

        return user_data_dict

    # dumps data to serial
    def dump_data(self):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)
        
        print(json.dumps(user_data_dict, indent=4))



class User(UserMixin):
    def __init__(self, id:str|None) -> None:
        self.id = id

    def data(self, manager: Database) -> dict:
        return manager.get_users()[self.id]
