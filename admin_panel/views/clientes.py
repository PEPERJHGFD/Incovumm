import streamlit as st
import pandas as pd

from controllers.cliente_controller import ClienteController

controller = ClienteController()


def clientes():
    st.title("Administración de Clientes")
    st.markdown("Use el formulario para agregar clientes y revise la lista actualizada.")

    with st.expander("Nuevo Cliente", expanded=True):
        nombre = st.text_input("Nombre", key="nombre")
        correo = st.text_input("Correo", key="correo")
        telefono = st.text_input("Teléfono", key="telefono")

        if st.button("Guardar cliente"):
            if nombre and correo and telefono:
                controller.guardar(nombre, correo, telefono)
                st.success("Cliente agregado correctamente.")
            else:
                st.warning("Complete todos los campos antes de guardar.")

    st.markdown("---")
    clientes_df = controller.listar()
    if not clientes_df.empty:
        st.dataframe(clientes_df)
    else:
        st.info("No hay clientes registrados aún.")
