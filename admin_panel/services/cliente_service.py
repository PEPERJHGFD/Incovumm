import pandas as pd

from models.cliente import Cliente
from models.database import Database
from services.firebase_service import FirebaseService

class ClienteService:
    def __init__(self):
        self.firebase = None
        self.connected = False
        try:
            self.firebase = FirebaseService()
            self.connected = True
        except Exception as exc:
            print(f"Firebase no disponible: {exc}")
            self.firebase = None
            self.connected = False
        self.clientes = self._cargar_datos()

    def _cargar_datos(self):
        if self.connected and self.firebase is not None:
            raw = self.firebase.listar_clientes()
            df = pd.DataFrame(raw) if raw else pd.DataFrame(columns=["ID", "Nombre", "Correo", "Telefono", "Activo"])
            if "Activo" not in df.columns:
                df["Activo"] = True
            return df

        raw = Database.read()
        df = pd.DataFrame(raw) if raw else pd.DataFrame(columns=["ID", "Nombre", "Correo", "Telefono", "Activo"])
        if "Activo" not in df.columns:
            df["Activo"] = True
        return df

    def _persistir(self):
        if self.connected and self.firebase is not None:
            return
        Database.write(self.clientes.to_dict(orient="records"))

    def obtener_clientes(self):
        if self.connected and self.firebase is not None:
            df = pd.DataFrame(self.firebase.listar_clientes())
            if "Activo" not in df.columns:
                df["Activo"] = True
            return df
        return self.clientes.copy()

    def obtener_cliente(self, cliente_id: int):
        if self.connected and self.firebase is not None:
            data = self.firebase.obtener_cliente(cliente_id)
            return Cliente.from_dict(data) if data else None
        encontrado = self.clientes.loc[self.clientes["ID"] == cliente_id]
        if encontrado.empty:
            return None
        return Cliente.from_dict(encontrado.iloc[0].to_dict())

    def agregar(self, nombre: str, correo: str, telefono: str):
        if self.connected and self.firebase is not None:
            cliente = Cliente(0, nombre, correo, telefono, activo=True)
            return self.firebase.agregar_cliente(cliente)

        if self.clientes.empty:
            nuevo_id = 1
        else:
            nuevo_id = int(self.clientes["ID"].max()) + 1
        nuevo = Cliente(nuevo_id, nombre, correo, telefono, activo=True)
        self.clientes = pd.concat([
            self.clientes,
            pd.DataFrame([nuevo.to_dict()])
        ], ignore_index=True)
        self._persistir()
        return nuevo

    def actualizar(self, cliente_id: int, nombre: str, correo: str, telefono: str):
        if self.connected and self.firebase is not None:
            return self.firebase.actualizar_cliente(cliente_id, nombre, correo, telefono)
        index = self.clientes.index[self.clientes["ID"] == cliente_id]
        if index.empty:
            return None
        idx = index[0]
        self.clientes.at[idx, "Nombre"] = nombre
        self.clientes.at[idx, "Correo"] = correo
        self.clientes.at[idx, "Telefono"] = telefono
        self._persistir()
        return Cliente.from_dict(self.clientes.loc[idx].to_dict())

    def eliminar(self, cliente_id: int):
        if self.connected and self.firebase is not None:
            return self.firebase.eliminar_cliente(cliente_id)
        self.clientes = self.clientes.loc[self.clientes["ID"] != cliente_id].reset_index(drop=True)
        self._persistir()

    def toggle_activo(self, cliente_id: int):
        if self.connected and self.firebase is not None:
            return self.firebase.toggle_activo(cliente_id)
        index = self.clientes.index[self.clientes["ID"] == cliente_id]
        if index.empty:
            return None
        idx = index[0]
        self.clientes.at[idx, "Activo"] = not bool(self.clientes.at[idx, "Activo"])
        self._persistir()
        return Cliente.from_dict(self.clientes.loc[idx].to_dict())
