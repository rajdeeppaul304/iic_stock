from ipo import Ipo, FD
from database_manager import Database

database = Database("database.json", "stocks.json")
ipo = Ipo("requested_lots.json", database)
fd_manager = FD("fds.json")

print(fd_manager.sell_fd("dhruvdubey32@gmail.com", database, 1, 0))

