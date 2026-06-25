import streamlit as st

from controllers.auth_controller import AuthController


def login():
    st.title("Ingreso al Panel")
    st.write("Ingrese sus credenciales para acceder al panel administrativo.")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        auth = AuthController()
        if auth.login(username, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
