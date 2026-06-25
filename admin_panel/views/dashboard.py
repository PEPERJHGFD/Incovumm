import streamlit as st


def dashboard():
    st.title("Panel Administrativo")
    st.markdown("Bienvenido al panel administrativo tipo Django Admin simulado con Streamlit.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", "250")
    c2.metric("Usuarios", "15")
    c3.metric("Ventas", "$50,000")

    st.markdown("---")
    st.subheader("Resumen rápido")
    st.write(
        "Este panel usa una arquitectura MVC simplificada: \n" 
        "- Modelos en `models/`\n" 
        "- Servicios en `services/`\n" 
        "- Controladores en `controllers/`\n" 
        "- Vistas en `views/`"
    )
