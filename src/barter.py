import json

# starting trade as dhruvdubey32@gmail.com
# manual-input-qr dhruv
# give-selected-stock 1001
# give-value-stock 23
# take-selected-stock 1011
# take-value-stock 232
# list-radio bartnorm

class Barter:
    def __init__(self, file:str, stocks_file:str) -> None:
        self.file = file
        self.stocks_file = stocks_file

    def start_trade(self, trader:str, form_data:dict):
        with open(self.file, "r") as file:
            active_trades = json.load(file)

        print("starting trade as", trader)
        for item, value in form_data.items():
            print(item, value)

        if active_trades.get(trader):
            print("Active Trade present")
            print("Clearing trades...")
        
        active_trades[trader] = {"trade_with" : form_data["manual-input-qr"],
                                 "stocks_to_give" : [form_data.get("give-selected-stock"), form_data.get("give-value-stock")],
                                 "stocks_to_get" : [form_data.get("take-selected-stock"), form_data.get("take-value-stock")],
                                 "trade_type" : form_data["list-radio"],
                                 "money": form_data.get("money-barter-stock")}

        with open(self.file, "w") as file:
            json.dump(active_trades, file)

    def get_active_trades(self, user="", trader=""):
        with open(self.file, "r") as file:
            active_trades = json.load(file)

        if trader != "":
            sent_trade = active_trades.get(trader)
            return (trader, sent_trade) if sent_trade is not None else None
        
        user_active_trades = []
        for key, val in active_trades.items():
            if val["trade_with"] == user:
                user_active_trades.append((key, val))

        return user_active_trades

    
    def deny_trade(self, current_user, trader):
        with open(self.file, "r") as file:
            active_trades = json.load(file)
        
        if active_trades.get(trader, {}).get("trade_with") == current_user:
            del active_trades[trader]

        with open(self.file, "w") as file:
            json.dump(active_trades, file)
        
        return (False, "Trade Denied")

    def confirm_trade(self, current_user, trader, manager):
        with open(self.file, "r") as file:
            active_trades = json.load(file)
        
        trader_active_trade = active_trades.get(trader, {})
        if trader_active_trade.get("trade_with") != current_user:
            return (False, "Trader Cancelled the Trade")

        # keep in mind that trader is the one who initiated the barter
        # current_user is the one that accepted the barter
        # thus the stocks_to_give and stocks_to_get should be with respect to trader
        stocks_to_give = trader_active_trade.get("stocks_to_give")
        stocks_to_get = trader_active_trade.get("stocks_to_get")

        print(stocks_to_give, stocks_to_get)

        trader_info = manager.get_users(no_pass=False).get(trader)
        current_user_info = manager.get_users(no_pass=False).get(current_user)

        # return False if user or trader was not found in database.json
        if not (trader_info or current_user_info):
            return (False, "User or Trader not Found")

        # bartnorm -> normal barter without money
        # take-bart -> trader gets money from current_user
        # give-bart -> current_user gets money from trader
        if trader_active_trade["trade_type"] == "take-bart":
            if not current_user_info.get("balance") >= int(trader_active_trade["money"]):
                print("current user does not have enough balance")
                return (False, "You do not have enough Balance")
            
            if not (stocks_to_give[1] or stocks_to_get[1]):
                print("trade not allowed")
                return (False, "Trade Not Allowed")


        if trader_active_trade["trade_type"] == "give-bart":
            if not trader_info.get("balance") >= int(trader_active_trade["money"]):
                print("trader does not have enough balance")
                return (False, "Trader does not have enough Balance")

            if not (stocks_to_give[1] or stocks_to_get[1]):
                print("trade not allowed")
                return (False, "Trade Not Allowed")
        
        # before the and statement stuff is to avoid the case where the user does not own the stock trader wants
        # the not is to just return False if the trade is not possible
        if not (current_user_info.get("stocks").get(stocks_to_get[0]) and current_user_info.get("stocks").get(stocks_to_get[0]) >= int(stocks_to_get[1])):
            if stocks_to_get[0]:
                print("user cannot trade")
                return (False, "You do not have enough requested stocks")
        
        # before the and statement stuff is to avoid the case where the trader does not own the stock user wants
        # same logic for using not 
        if not (trader_info.get("stocks").get(stocks_to_give[0]) and trader_info.get("stocks").get(stocks_to_give[0]) >= int(stocks_to_give[1])):
            if stocks_to_give[0]:
                print("trader cannot trade")
                return (False, "Trader does not have enough stocks")

        user_data_dict = manager.get_users(no_pass=False)

        if stocks_to_give[0] and stocks_to_give[1]:
            trader_info["stocks"][stocks_to_give[0]] -= int(stocks_to_give[1])
            # add stocks trader want to give to current_user_info
            if current_user_info["stocks"].get(stocks_to_give[0]):
                current_user_info["stocks"][stocks_to_give[0]] += int(stocks_to_give[1])
            else:
                current_user_info["stocks"][stocks_to_give[0]] = int(stocks_to_give[1])

        if stocks_to_get[0] and stocks_to_get[1]:
            current_user_info["stocks"][stocks_to_get[0]] -= int(stocks_to_get[1])
            if trader_info["stocks"].get(stocks_to_get[0]):
                trader_info["stocks"][stocks_to_get[0]] += int(stocks_to_get[1])
            else:
                trader_info["stocks"][stocks_to_get[0]] = int(stocks_to_get[1])

        user_data_dict[trader]["stocks"] = trader_info["stocks"]
        user_data_dict[current_user]["stocks"] = current_user_info["stocks"]

        # handle giving or taking of money
        if trader_active_trade["trade_type"] == "take-bart":
            user_data_dict[current_user]["balance"] -= int(trader_active_trade["money"])
            user_data_dict[trader]["balance"] += int(trader_active_trade["money"])

        if trader_active_trade["trade_type"] == "give-bart":
            user_data_dict[trader]["balance"] -= int(trader_active_trade["money"])
            user_data_dict[current_user]["balance"] += int(trader_active_trade["money"])

        print("trader_info", trader_info)
        print("current_user_info", current_user_info)

        print(user_data_dict)

        # manager.save_data(user_data_dict)
        with open(manager.file, "w") as file:
            json.dump(user_data_dict, file)

        # clear the trade from active_trades
        if active_trades.get(trader):
            active_trades.pop(trader)
            
        with open(self.file, "w") as file:
            json.dump(active_trades, file)

        print("trade completed")
        return (True, "Trade Complete")
