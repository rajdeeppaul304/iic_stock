import json
import random

class Ipo:
    def __init__(self, file, manager) -> None:
        self.file = file
        self.database_manager = manager

    def distribute_lots(self):
        with open(self.file, "r") as file:
            requested_lots = json.load(file)

        stocks = self.database_manager.get_stocks(only_ipos=True)
        distributed_lots = {ipo:{} for ipo in requested_lots.keys()}

        for ipo, requests in requested_lots.items():
            lots_remaining = stocks.get(ipo, {}).get("lots")

            distributed = False
            while not distributed:
                distributed = True

                for user, number_of_requests in requests.items():
                    if number_of_requests and lots_remaining:
                        distributed = False
                        num = random.randint(0, min(5, number_of_requests, lots_remaining))

                        requested_lots[ipo][user] -= num
                        lots_remaining -= num

                        if distributed_lots[ipo].get(user): 
                            distributed_lots[ipo][user] += num
                        else: 
                            distributed_lots[ipo][user] = num

        print("------------------------------------")
        print(requested_lots)
        print(distributed_lots)
        print("------------------------------------")

        user_data_dict = self.database_manager.get_users(no_pass=False)

        for ipo, dist_lots in distributed_lots.items():
            print(f"ipo: {ipo}, dist_lots: {dist_lots}")
            for user, amount in dist_lots.items():
                if not user_data_dict[user].get("stocks"):
                    user_data_dict[user]["stocks"]={}
                user_data_dict[user]["stocks"][ipo] = amount * stocks.get(ipo, {}).get("shares_per_lot", 0)

        with open(self.file, "w") as file:
            json.dump({}, file)

        with open(self.database_manager.file, "w") as file:
            json.dump(user_data_dict, file)
class FD:
    def __init__(self, file, interest) -> None:
        self.file = file
        self.interest = interest


    def increase_interest(self):
        with open(self.file, "r") as file:
            fds = json.load(file)

        for user, amount in fds.items():
            fds[user] += amount * self.interest

        with open(self.file, "w") as file:
            json.dump(fds, file)


