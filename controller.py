# controller.py
from model import GreenhouseModel
from view import MainView

class GreenhouseController:
    def __init__(self):
        self.model = GreenhouseModel()
        self.view = MainView(self)
        
        # Agregar algunos datos de ejemplo
        self._add_sample_data()

    def _add_sample_data(self):
        # Datos de ejemplo para tener contenido al iniciar
        sample_data = [
            ["Invernadero Norte", "500", "12", "Tomate", "2024-01-15", "Juan Pérez"],
            ["Invernadero Sur", "350", "8", "Pimiento", "2024-02-20", "María García"],
            ["Invernadero Este", "420", "10", "Lechuga", "2024-03-10", "Carlos López"]
        ]
        for data in sample_data:
            self.add_greenhouse(data)

    def login(self, u, p):
        # En un sistema real, validaríamos contra una base de datos
        return u == "admin" and p == "1234"

    def add_greenhouse(self, data):
        keys = ["nombre", "superficie", "produccion", "cultivo", "fecha", "responsable"]
        self.model.add_greenhouse(dict(zip(keys, data)))

    def get_greenhouses(self, filter_active=False, search_term=None):
        return self.model.get_all(filter_active, search_term)

    def delete_greenhouse(self, idx):
        return self.model.delete(idx)

    def update_greenhouse(self, idx, data):
        keys = ["nombre", "superficie", "produccion", "cultivo", "fecha", "responsable"]
        return self.model.update(idx, dict(zip(keys, data)))

    def get_greenhouse(self, idx):
        return self.model.get(idx)
    # Iniciar la aplicación
if __name__ == '__main__':
    app = GreenhouseController()
    app.view.mainloop()
