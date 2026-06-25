import streamlit as st
from config import MENU_OPTIONS


def menu():
    st.sidebar.title("Navegación")
    return st.sidebar.radio("Menú", MENU_OPTIONS)
