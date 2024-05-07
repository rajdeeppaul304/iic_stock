import json
import random
import csv
from re import S

# all three values are in percent
stagnant_random = 5
downhill_random = 5
max_multiplier = 300

market_change_cap = 1/2

def signum(num):
    if num == 0:
        return 1

    return num / abs(num)

class Stocks:
    def __init__(self, file, database_manager) -> None:
        self.file = file
        self.database_manager = database_manager

    def on_match_increment(self, current_match):
        with open(self.file, "r") as file:
            stocks = json.load(file)

        # update value of stocks by "cutting edge backend algorithm"
        if current_match >= 1:
            self.update_price(stocks, current_match)

        # reset net_bought stockss
        for stock_id, data in stocks.items():
            if data.get("net_bought"):
                data["net_bought_prev"] = data["net_bought"]
                data["net_bought"] = 0

            else:
                data["net_bought"] = 0
                data["net_bought_prev"] = 0

        with open(self.file, "w") as file:
            json.dump(stocks, file)


    def update_price(self, stocks=None, current_match=0):
        if not stocks:
            with open(self.file, "r") as file:
                stocks = json.load(file)

        market_changes = self.get_market_sentiment(stocks)
        news_changes = self.get_news_changes(current_match)

        changes = {}

        for stock, change in market_changes.items():
            if news_changes.get(stock):
                print(f"for {stock} market {change} news {news_changes[stock]}")
                changes[stock] = signum(change) * signum(news_changes[stock]) * min(abs(change), abs(news_changes[stock]) * market_change_cap)

                print("--------------------------")
                print(f"for {stock} changes {changes[stock]}")
                changes[stock] += news_changes[stock]
                print(f"for {stock} changes {changes[stock]}")
                print("--------------------------")

            else:
                changes[stock] = change

        # print(changes)

        for stock, data in stocks.items():
            print(f"old value for {stock} is {stocks[stock]['amount']}")
            stocks[stock]["amount"] = (data.get("amount", 0) * changes.get(stock, 0) / 100) + data.get("amount", 0)
            print(f"new value for stock {stock} is {stocks[stock]['amount']}")

        # write to stocks.json
        with open(self.file, "w") as file:
            json.dump(stocks, file)

    # rajdeep 
    def get_news_changes(self, current_match):
        result_dict = {}
        file_path = "./admin/news_change.csv"
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                row_dict = {}
                for index, value in enumerate(row[1:], start=1):
                    row_dict[str(index+1000)] = int(value)
                result_dict[row[0]] = row_dict

        print(f"news change for {current_match}: {result_dict[str(current_match)]}")
        return result_dict[str(current_match)]

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
        stagnant_keys = list(stagnant_stocks.keys())
        # random.choice does not work with empty lists
        if len(stagnant_keys):
            stagnant_key = random.choice(list(stagnant_stocks.keys()))
            stocks_filtered.pop(stagnant_key)
            choosen_stagnant_stock = {stagnant_key: stagnant_stocks[stagnant_key]}
            print(f"choosen stagnant {choosen_stagnant_stock}")
            # add stagnant stock to change list
            stocks_change[stagnant_key] = random.randint(-stagnant_random, stagnant_random)
        
        # random chaneg for downhill stocks
        downhill_stocks = {stock:val for stock, val in stocks_filtered.items() if val[0] < 0 and val[1] < 0}
        downhill_keys = list(downhill_stocks.keys())
        # random.choice does not work with empty lists
        if len(downhill_keys):
            downhill_key = random.choice(list(downhill_stocks.keys()))
            stocks_filtered.pop(downhill_key)
            choosen_downhill_stock = {downhill_key: downhill_stocks[downhill_key]}
            print(f"downhill {downhill_stocks}, choosen {choosen_downhill_stock}")
        
            # add downhill stock to change list
            stocks_change[downhill_key] = random.randint(0, downhill_random)

        for stock, val in stocks_filtered.items():
            # val[0] is net_bought
            stocks_change[stock] = val[0] * max_multiplier * stocks[stock].get("amount", 0) / market_cap

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


