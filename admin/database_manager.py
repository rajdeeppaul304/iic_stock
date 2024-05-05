from os import path
import json

# from flask_login import UserMixin

class Database():
    def __init__(self, file:str, stocks_file:str, round_match_info:str) -> None:
        self.file = file
        self.stocks_file = stocks_file
        self.round_match_info = round_match_info
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
        stocks = self.get_stocks()
        stocks[stock_id_str] = new_price

        with open(self.stocks_file, "w") as file:
            json.dump(stocks, file)

        return True

    def reset(self, email:str):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)

        if user_data_dict.get(email):
            user_data_dict[email]["balance"] = 10_00_000
            user_data_dict[email]["stocks"] = {}

            with open(self.file, "w") as database:
                json.dump(user_data_dict, database)

        else: print("could not find user")

    def round(self, increment=False):
        with open(self.round_match_info, "r") as file:
            info = json.load(file)

        if increment:
            if info.get("round"):
                info["round"] += 1
            else:
                info["round"] = 1
            with open(self.round_match_info, "w") as file:
                json.dump(info, file)

        return info.get("round", 0)

    def match(self, increment=False):
        with open(self.round_match_info, "r") as file:
            info = json.load(file)
        
        if increment:
            if info.get("match"):
                info["match"] += 1
            else:
                info["match"] = 1

            with open(self.round_match_info, "w") as file:
                json.dump(info, file)

        return info.get("match", 0)

    def get_stocks(self, only_ipos=False) -> dict:
        with open(self.stocks_file) as stocks:
            stocks_dict = json.load(stocks)

        if only_ipos:
            ipo_dict = {key:val for key, val in stocks_dict.items() if val.get("ipo")}
            return ipo_dict

        return stocks_dict

    def get_users(self, no_pass=True) -> dict:
        with open(self.file) as stocks:
            user_data_dict = json.load(stocks)

        if no_pass:
            for user_data in user_data_dict.values():
                user_data.pop("password", None)
                # del user_data["password"]

        return user_data_dict

    def dump_data(self):
        with open(self.file, "r") as database:
            user_data_dict = json.load(database)
        
        print(json.dumps(user_data_dict, indent=4))

