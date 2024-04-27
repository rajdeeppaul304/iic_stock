import json

# starting trade as dhruvdubey32@gmail.com
# manual-input-qr dhruv
# give-selected-stock 1001
# give-value-stock 23
# take-selected-stock 1011
# take-value-stock 232
# list-radio bartnorm

class Barter:
    def __init__(self, file:str) -> None:
        self.file = file

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
                                 "trade-type" : form_data["list-radio"]}


        with open(self.file, "w") as file:
            json.dump(active_trades, file)
                        



