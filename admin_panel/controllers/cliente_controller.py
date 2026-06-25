from services.cliente_service import ClienteService

class ClienteController:
    def __init__(self):
        self.service = ClienteService()

    def listar(self):
        return self.service.obtener_clientes()

    def guardar(self, nombre, correo, telefono):
        return self.service.agregar(nombre, correo, telefono)

    def obtener(self, cliente_id):
        return self.service.obtener_cliente(cliente_id)

    def actualizar(self, cliente_id, nombre, correo, telefono):
        return self.service.actualizar(cliente_id, nombre, correo, telefono)

    def eliminar(self, cliente_id):
        return self.service.eliminar(cliente_id)

    def toggle_activo(self, cliente_id):
        return self.service.toggle_activo(cliente_id)

    def is_connected(self):
        return getattr(self.service, "connected", False)

    def obtener(self, cliente_id):
        return self.service.obtener_cliente(cliente_id)

    def actualizar(self, cliente_id, nombre, correo, telefono):
        return self.service.actualizar(cliente_id, nombre, correo, telefono)

    def eliminar(self, cliente_id):
        return self.service.eliminar(cliente_id)

    def toggle_activo(self, cliente_id):
        return self.service.toggle_activo(cliente_id)
