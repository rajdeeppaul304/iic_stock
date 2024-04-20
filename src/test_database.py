from database_manager import Database

manager = Database("database.json", "stocks.json")
manager.reset("dhruvdubey32@gmail.com")

manager.buy_stocks("dhruvdubey32@gmail.com", 1001, 6)
manager.buy_stocks("dhruvdubey32@gmail.com", 1002, 2)
manager.sell_stocks("dhruvdubey32@gmail.com", 1001, 10)

manager.dump_data()
