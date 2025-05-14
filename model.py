# model.py
class GreenhouseModel:
    def __init__(self):
        self.greenhouses = []

    def add_greenhouse(self, data):
        self.greenhouses.append(data)
        return len(self.greenhouses) - 1  # Return the index of the new greenhouse

    def get_all(self, filter_active=False, search_term=None):
        """Get all greenhouses, optionally filtered"""
        result = self.greenhouses
        
        if search_term:
            search_term = search_term.lower()
            result = [gh for gh in result if search_term in gh['nombre'].lower() or 
                      search_term in gh['cultivo'].lower() or 
                      search_term in gh['responsable'].lower()]
        
        # En una implementación real, habría un campo 'activo'
        # para filtrar, pero lo omitimos por simplicidad
        
        return result

    def get(self, index):
        return self.greenhouses[index] if 0 <= index < len(self.greenhouses) else None

    def update(self, index, data):
        if 0 <= index < len(self.greenhouses):
            self.greenhouses[index] = data
            return True
        return False

    def delete(self, index):
        if 0 <= index < len(self.greenhouses):
            del self.greenhouses[index]
            return True
        return False