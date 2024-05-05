import json
import random

class Ipo:
    def __init__(self, file, database_manager) -> None:
        self.file = file
        self.database_manager = database_manager

    def request_ipo(self, user_id:str, ipo:str, amount:int):
        with open(self.file, "r") as file:
            requested_lots = json.load(file)

        if requested_lots.get(ipo, {}).get(user_id):
            requested_lots[ipo][user_id] += amount

        else:
            requested_lots[ipo][user_id] = amount


        with open(self.file, "w") as file:
            json.dump(requested_lots, file)


    def distribute_lots(self):
        with open(self.file, "r") as file:
            requested_lots = json.load(file)

        ipos_list = self.database_manager.get_stocks(only_ipos=True)
        distributed_lots = {ipo:{} for ipo in requested_lots.keys()}

        for ipo, requests in requested_lots.items():
            lots_remaining = ipos_list.get(ipo, {}).get("lots")

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

        print(requested_lots)
        print(distributed_lots) 


class FD:
    def __init__(self, file) -> None:
        self.file = file

    def buy(self, user_id, amount, manager):
        user_data_dict = manager.get_users()
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






