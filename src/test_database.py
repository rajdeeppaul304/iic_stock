from database_manager import Database

manager = Database("database.json", "stocks.json")
manager.reset("dhruvdubey32@gmail.com")

while 1:
    input()
    manager.buy_stocks("dhruvdubey32@gmail.com", 1001, 1)
    manager.dump_data()
