import json
import random

class Ipo:
    def __init__(self, file, database_manager) -> None:
        self.file = file
        self.database_manager = database_manager

    def get_requested_ipos(self, user_id:str):
        with open(self.file, "r") as file:
            requested_lots = json.load(file)
        return {x: y[user_id] for x, y in requested_lots.items() if user_id in y}

    def request_ipo(self, user_id:str, ipo:str, amount:int):
        with open(self.file, "r") as file:
            requested_lots = json.load(file)

        user_data_dict = self.database_manager.get_users(no_pass=False)
        stocks = self.database_manager.get_stocks()

        money_required = amount * stocks.get(ipo, {}).get("amount", 0) * stocks.get(ipo, {}).get("shares_per_lot", 0)

        if user_data_dict.get(user_id, {}).get("balance", 0) < money_required:
            print("user does not have enough balance")
            return (False, "You do not have enough balance")

        print(f"spending {money_required} on {ipo} by {user_id}")
        if requested_lots.get(ipo, {}).get(user_id):
            requested_lots[ipo][user_id] += amount
        else:
            requested_lots[ipo] = {}
            requested_lots[ipo][user_id] = amount

        user_data_dict[user_id]["balance"] -= money_required

        with open(self.file, "w") as file:
            json.dump(requested_lots, file)

        with open(self.database_manager.file, "w") as file:
            json.dump(user_data_dict, file)


        return (True, "Success")


class FD:
    def __init__(self, file) -> None:
        self.file = file

    def buy(self, user_id, amount, manager):
        user_data_dict = manager.get_users(no_pass=False)
        balance = user_data_dict.get(user_id, {}).get("balance")

        if balance == None:
            return (False, "User not found")
        
        with open(self.file, "r") as file:
            fds = json.load(file)

        if not (amount <= balance):
            return (False, "You do not have enough balance")
        if amount <= 0:
            return (False, "Amount cannot be 0 or less")

        if fds.get(user_id):
            fds[user_id] += amount
        else:
            fds[user_id] = amount

        user_data_dict[user_id]["balance"] -= amount

        with open(self.file, "w") as file:
            json.dump(fds, file)
        
        with open(manager.file, "w") as file:
            json.dump(user_data_dict, file)

        return (True, "Success")






