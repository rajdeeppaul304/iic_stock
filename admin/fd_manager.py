import json

class FD:
    def __init__(self, file, interest) -> None:
        self.file = file
        self.interest = interest


    def increase_interest(self):
        with open(self.file, "r") as file:
            fds = json.load(file)

        for user, amount in fds.items():
            fds[user] += amount * self.interest


        with open(self.file, "w") as file:
            json.dump(fds, file)
