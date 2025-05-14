#Heber
from model import GreenhouseModel
from view    import MainView

class GreenhouseController:
    def __init__(self):
        self.model = GreenhouseModel()
        self.view = MainView(self)

    def login(self, u, p):
        return u == "admin" and p == "1234"

    def add_greenhouse(self, data):
        keys = ["nombre","superficie","produccion","cultivo","fecha","responsable"]
        self.model.add_greenhouse(dict(zip(keys, data)))

    def get_greenhouses(self):
        return self.model.get_all()

    def delete_greenhouse(self, idx):
        self.model.delete(idx)

if __name__ == '__main__':
    ctrl = GreenhouseController()
    ctrl.view.mainloop()
