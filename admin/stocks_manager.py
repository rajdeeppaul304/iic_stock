import json

class Stocks:
    def __init__(self, file) -> None:
        self.file = file

    def update_price(self):
        pass

    def on_match_increment(self):
        with open(self.file, "r") as file:
            stocks = json.load(file)

        for stock_id, data in stocks.items():
            if data.get("net_bought"):
                data["net_bought_prev"] = data["net_bought"]
                data["net_bought"] = 0

            else:
                data["net_bought"] = 0
                data["net_bought_prev"] = 0


        with open(self.file, "w") as file:
            json.dump(stocks, file)
