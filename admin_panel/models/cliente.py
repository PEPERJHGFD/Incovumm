class Cliente:
    def __init__(self, id: int, nombre: str, correo: str, telefono: str, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.activo = activo

    def to_dict(self):
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Correo": self.correo,
            "Telefono": self.telefono,
            "Activo": self.activo,
        }

    @staticmethod
    def from_dict(data: dict):
        return Cliente(
            id=data.get("ID"),
            nombre=data.get("Nombre", ""),
            correo=data.get("Correo", ""),
            telefono=data.get("Telefono", ""),
            activo=data.get("Activo", True),
        )
