import json
import random

# all the values are in percent
stagnant_random = 5
downhill_random = 5
max_multiplier = 300

class Stocks:
    def __init__(self, file, database_manager) -> None:
        self.file = file
        self.database_manager = database_manager

    def on_match_increment(self, current_match):
        with open(self.file, "r") as file:
            stocks = json.load(file)

        # update value of stocks by "cutting edge backend algorithm"
        if current_match >= 1:
            self.update_price(stocks)

        # reset net_bought stocks
        for stock_id, data in stocks.items():
            if data.get("net_bought"):
                data["net_bought_prev"] = data["net_bought"]
                data["net_bought"] = 0

            else:
                data["net_bought"] = 0
                data["net_bought_prev"] = 0

        with open(self.file, "w") as file:
            json.dump(stocks, file)


    def update_price(self, stocks=None):
        if not stocks:
            with open(self.file, "r") as file:
                stocks = json.load(file)

        changes = self.get_market_sentiment(stocks)
        news_changes = self.get_news_changes()

    # rajdeep 
    def get_news_changes(self):
        pass

    # this returns stockwise percent change due to market sentiment
    def get_market_sentiment(self, stocks=None):
        if not stocks:
            with open(self.file, "r") as file:
                stocks = json.load(file)

        market_cap = self.get_market_value(stocks)
        print(f"market_cap: {market_cap}")

        stocks_filtered = {stock: (data.get("net_bought", 0), data.get("net_bought_prev", 0)) for stock, data in stocks.items()}
        stocks_change = {}

        # random change for stagnant stock
        stagnant_stocks = {stock: val for stock, val in stocks_filtered.items() if val == (0, 0)}
        stagnant_key = random.choice(list(stagnant_stocks.keys()))
        stocks_filtered.pop(stagnant_key)
        choosen_stagnant_stock = {stagnant_key: stagnant_stocks[stagnant_key]}
        print(f"choosen stagnant {choosen_stagnant_stock}")
        
        # add stagnant stock to change list
        stocks_change[stagnant_key] = random.randint(-stagnant_random, stagnant_random)
        
        # random chaneg for downhill stocks
        downhill_stocks = {stock:val for stock, val in stocks_filtered.items() if val[0] < 0 and val[1] < 0}
        downhill_key = random.choice(list(downhill_stocks.keys()))
        stocks_filtered.pop(downhill_key)
        choosen_downhill_stock = {downhill_key: downhill_stocks[downhill_key]}
        print(f"downhill {downhill_stocks}, choosen {choosen_downhill_stock}")
        
        # add downhill stock to change list
        stocks_change[downhill_key] = random.randint(0, downhill_random)

        for stock, val in stocks_filtered.items():
            stocks_change[stock] = val[0] * max_multiplier / market_cap

        print(stocks_change)
        return stocks_change


    def get_market_value(self, stocks):
        market_cap = 0
        
        if not stocks:
            with open(self.file, "r") as file:
                stocks = json.load(file)

        for stock, data in stocks.items():
            market_cap += data["amount"] * data.get("total_bought", 0)
        
        users = self.database_manager.get_users()

        for user, data in users.items():
            market_cap += data.get("balance", 0)

        return market_cap


