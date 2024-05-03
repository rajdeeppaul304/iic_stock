from ipo_manager import Ipo
from database_manager import Database

database = Database("database.json", "stocks.json")
ipo = Ipo("requested_lots.json", database)

ipo.request_ipo("testing123", "1019", 10)

ipo.distribute_lots()
