from os import path
import json

class Database():
    def __init__(self, file:str) -> None:
        self.file = file
        if not path.exists(file):
            open(file, "w").close()

    # whats hashing?
    def add_user(self, name:str, email:str, password:str, intial_balance:float):
        pass

    def append(self, data):
        with open(self.file, "a") as database:
            pass



