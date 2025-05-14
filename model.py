#Heber
import datetime

class GreenhouseModel:
    def __init__(self):
        self.greenhouses = []  

    def add_greenhouse(self, data):
        self.greenhouses.append(data)

    def get_all(self):
        return self.greenhouses

    def delete(self, index):
        if 0 <= index < len(self.greenhouses):
            del self.greenhouses[index]