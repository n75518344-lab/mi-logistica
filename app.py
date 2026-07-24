import base64
from datetime import datetime
import os
import textwrap
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express - Admin",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# REVISAR SESIÓN
query_params = st.query_params

if "usuario_actual" not in st.session_state:
    if "saved_user" in query_params:
        st.session_state.usuario_actual = query_params["saved_user"]
        st.session_state.rol_actual = query_params.get(
            "saved_rol", "👨‍💼 Portal Administrador"
        )
    else:
        st.session_state.usuario_actual = None
        st.session_state.rol_actual = None

# CSS GENERAL DEL SISTEMA (CORRECCIÓN INFALIBLE DE BOTONES)
st.markdown(
    """
    <style>
    /* OCULTAR SCROLLBAR GLOBAL DE LA VENTANA */
    html, body, .stApp { 
        overflow: hidden !important; 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* OCULTAR SIDEBAR Y CABECERA DE STREAMLIT */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { 
        display: none !important; 
    }
    
    .block-container { 
        max-width: 88% !important; 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A; 
    }

    /* ==========================================================
       CORRECCIÓN ABSOLUTA DE VISIBILIDAD DE TEXTO E ICONOS EN BOTONES
       Afecta al botón, al texto (<p>) y a los iconos (<span>)
       ========================================================== */
    div[data-testid="stButton"] > button { 
        background-color: #1E293B !important;  /* Fondo oscuro consistente con tu imagen */
        border: 1px solid #334155 !important;
        border-radius: 8px !important; 
        font-weight: 600 !important; 
        transition: all 0.2s ease;
    }
    
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button span {
        color: #FFFFFF !important;    /* Texto e Iconos en BLANCO NÍTIDO */
        fill: #FFFFFF !important;     /* Asegura que los iconos SVG también sean blancos */
    }

    div[data-testid="stButton"] > button:hover { 
        background-color: #0F382C !important; /* Color verde corporativo al pasar el mouse */
        border-color: #0F382C !important; 
    }
    div[data-testid="stButton"] > button:hover p,
    div[data-testid="stButton"] > button:hover span {
        color: #FFFFFF !important; /* Mantiene el texto blanco al hacer hover */
    }

    /* CONTENEDORES CON SCROLL INTELIGENTE PARA TABLAS */
    .tabla-contenedor, .tabla-contenedor-logs, .tabla-contenedor-pedidos {
        max-height: 450px;
        height: fit-content;
        overflow-y: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px !important;
    }

    .tabla-contenedor-logs {
        max-height: 500px;
        margin-top: 15px !important;
    }

    /* BARRA DE SCROLL MODERNA Y FINITA PARA TABLAS */
    .tabla-contenedor::-webkit-scrollbar,
    .tabla-contenedor-logs::-webkit-scrollbar,
    .tabla-contenedor-pedidos::-webkit-scrollbar {
        width: 6px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-track,
    .tabla-contenedor-logs::-webkit-scrollbar-track,
    .tabla-contenedor-pedidos::-webkit-scrollbar-track {
        background: transparent !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb,
    .tabla-contenedor-logs::-webkit-scrollbar-thumb,
    .tabla-contenedor-pedidos::-webkit-scrollbar-thumb {
        background-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb:hover,
    .tabla-contenedor-logs::-webkit-scrollbar-thumb:hover,
    .tabla-contenedor-pedidos::-webkit-scrollbar-thumb:hover {
        background-color: #94A3B8 !important;
    }

    /* ESTILOS DE TABLA */
    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 14px;
        text-align: left;
    }
    .tabla-usuarios th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 12px 14px;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 700;
    }
    .tabla-usuarios td {
        padding: 10px 14px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
    }
    .tabla-usuarios tr:last-child td {
        border-bottom: none;
    }
    .tabla-usuarios tr:hover {
        background-color: #F1F5F9;
    }

    /* LIMITAR ALTURA Y SCROLLBAR PARA MENÚS DESPLEGABLES (SELECTBOX) */
    ul[role="listbox"] {
        max-height: 200px !important;
        overflow-y: auto !important;
    }

    ul[role="listbox"]::-webkit-scrollbar {
        width: 6px !important;
    }

    ul[role="listbox"]::-webkit-scrollbar-track {
        background: transparent !important;
    }

    ul[role="listbox"]::-webkit-scrollbar-thumb {
        background-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }

    ul[role="listbox"]::-webkit-scrollbar-thumb:hover {
        background-color: #94A3B8 !important;
    }

    /* MODAL Y TEXTO BLANCO */
    div[role="dialog"] *, [data-testid="stDialog"] *, [data-testid="stModal"] * {
        color: #FFFFFF !important;
    }

    div[role="dialog"] button, [data-testid="stDialog"] button, [data-testid="stModal"] button {
        background-color: #0F382C !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
    }
    div[role="dialog"] button *, [data-testid="stDialog"] button *, [data-testid="stModal"] button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    div[role="dialog"] button:hover, [data-testid="stDialog"] button:hover, [data-testid="stModal"] button:hover {
        background-color: #15803D !important;
    }

    /* FORMULARIO DE LOGIN */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 14px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 28px !important; 
        border-top: 6px solid #0F382C !important; 
    }

    /* INPUTS */
    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    .stTextInput input::placeholder { color: #94A3B8 !important; }

    /* CONTRASEÑA */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
    }
    div[data-baseweb="input"] input {
        background-color: #FFFFFF !important;
        border: none !important;
    }
    button[aria-label="Show password"], button[aria-label="Hide password"] {
        background-color: #FFFFFF !important;
        border: none !important;
    }
    button[aria-label="Show password"] svg, button[aria-label="Hide password"] svg {
        fill: #0F382C !important;
    }

    /* EXPANDER */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] details summary {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }
    [data-testid="stExpander"] details summary * {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* BOTÓN SUBMIT */
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        border-radius: 8px !important; 
        border: none !important; 
        padding: 12px 20px !important; 
        width: 100% !important;
        min-height: 48px !important;
    }
    div[data-testid="stFormSubmitButton"] > button p, 
    div[data-testid="stFormSubmitButton"] > button span { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }

    /* SELECTBOX ESTILOS GENERALES */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
        background-color: transparent !important;
    }
    li[role="option"], div[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }

    /* BOTONES ESPECIALES */
    #logout_btn button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #logout_btn button p, #logout_btn button span { color: #991B1B !important; font-weight: 700 !important; }

    #btn_inactivar button {
        background-color: #FEF3C7 !important;
        border: 1px solid #FCD34D !important;
    }
    #btn_inactivar button p, #btn_inactivar button span { color: #92400E !important; font-weight: 700 !important; }

    #btn_eliminar button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #btn_eliminar button p, #btn_eliminar button span { color: #991B1B !important; font-weight: 700 !important; }

    /* PESTAÑAS MINIMALISTAS */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        gap: 28px !important; 
        border-bottom: 2px solid #CBD5E1 !important; 
        margin-top: 5px !important; 
        padding-bottom: 0px !important;
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: transparent !important; 
        border: none !important;
        border-bottom: 3px solid transparent !important;
        padding: 8px 4px 10px 4px !important; 
        border-radius: 0px !important;
        margin-bottom: -2px !important;
    }
    .stTabs [data-baseweb="tab"] p { 
        color: #64748B !important; 
        font-weight: 500 !important; 
        font-size: 15px !important;
    }
    .stTabs [aria-selected="true"] { 
        background-color: transparent !important; 
        border-bottom: 3px solid #0F382C !important; 
    }
    .stTabs [aria-selected="true"] p { 
        color: #0F382C !important; 
        font-weight: 700 !important; 
    }
    </style>
""",
    unsafe_allow_html=True,
)

# DATOS EN SESIÓN
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = pd.DataFrame([
        {
            "USUARIO": "admin",
            "PASS": "admin123",
            "ROL": "👨‍💼 Portal Administrador",
            "ESTADO": "Activo",
            "ÚLTIMA CONEXIÓN": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "USUARIO": "operador1",
            "PASS": "123",
            "ROL": "🛠️ Operario",
            "ESTADO": "Activo",
            "ÚLTIMA CONEXIÓN": "Nunca",
        },
        {
            "USUARIO": "juan_repartidor",
            "PASS": "123",
            "ROL": "🛵 Repartidor (App)",
            "ESTADO": "Activo",
            "ÚLTIMA CONEXIÓN": "Nunca",
        },
        {
            "USUARIO": "cliente_global",
            "PASS": "123",
            "ROL": "🏢 Cliente",
            "EST
