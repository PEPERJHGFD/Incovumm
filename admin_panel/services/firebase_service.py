import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

from models.cliente import Cliente
from config import FIREBASE_CREDENTIALS_PATH, FIREBASE_COLLECTION


class FirebaseService:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        credential_path = base_dir / FIREBASE_CREDENTIALS_PATH
        if not credential_path.exists():
            raise FileNotFoundError(f"Firebase credentials not found at {credential_path}")

        if not firebase_admin._apps:
            cred = credentials.Certificate(str(credential_path))
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.collection = self.db.collection(FIREBASE_COLLECTION)

        if not self._test_connection():
            raise ConnectionError("No se pudo conectar a Firestore con las credenciales proporcionadas.")

    def _test_connection(self):
        try:
            list(self.collection.limit(1).stream())
            return True
        except Exception:
            return False

    def _normalize_id(self, doc_id):
        try:
            return int(doc_id)
        except (TypeError, ValueError):
            return doc_id

    def listar_clientes(self):
        docs = self.collection.stream()
        clientes = []
        for doc in docs:
            data = doc.to_dict() or {}
            data["ID"] = self._normalize_id(doc.id)
            clientes.append(data)
        return clientes

    def obtener_cliente(self, cliente_id):
        doc = self.collection.document(str(cliente_id)).get()
        if not doc.exists:
            return None
        data = doc.to_dict() or {}
        data["ID"] = self._normalize_id(doc.id)
        return data

    def _next_id(self):
        docs = self.collection.stream()
        max_id = 0
        for doc in docs:
            try:
                current_id = int(doc.id)
                max_id = max(max_id, current_id)
            except (TypeError, ValueError):
                continue
        return max_id + 1

    def agregar_cliente(self, cliente: Cliente):
        cliente.id = self._next_id()
        self.collection.document(str(cliente.id)).set(cliente.to_dict())
        return cliente

    def actualizar_cliente(self, cliente_id, nombre, correo, telefono):
        doc_ref = self.collection.document(str(cliente_id))
        if not doc_ref.get().exists:
            return None
        doc_ref.update({"Nombre": nombre, "Correo": correo, "Telefono": telefono})
        data = doc_ref.get().to_dict() or {}
        data["ID"] = cliente_id
        return data

    def eliminar_cliente(self, cliente_id):
        self.collection.document(str(cliente_id)).delete()

    def toggle_activo(self, cliente_id):
        doc_ref = self.collection.document(str(cliente_id))
        snapshot = doc_ref.get()
        if not snapshot.exists:
            return None
        current = snapshot.to_dict().get("Activo", True)
        doc_ref.update({"Activo": not bool(current)})
        data = doc_ref.get().to_dict() or {}
        data["ID"] = cliente_id
        return data
