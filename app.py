import base64
from datetime import datetime, date, timedelta
import os
import textwrap
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express - Admin",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
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

# CSS GENERAL DEL SISTEMA Y CORRECCIÓN TOTAL DE MENÚS DESPLEGABLES (FONDO BLANCO Y TEXTO OSCURO)
st.markdown(
    """
    <style>
    /* Estructura general */
    html, body, .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* Sidebar - Estructura limpia y ordenada sin superposiciones */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important;
        border-right: 1px solid #CBD5E1 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
        padding-top: 1rem !important;
    }
    
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] div.stVerticalBlock {
        gap: 0.6rem !important;
    }
    
    [data-testid="stSidebar"] .stTextInput, 
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 4px !important;
    }
    
    [data-testid="stSidebar"] label {
        margin-bottom: 2px !important;
        padding-bottom: 0px !important;
    }

    /* =========================================================
        ESTILOS ABSOLUTOS PARA SELECTS, MULTISELECTS Y MENÚS FLOTANTES
        ========================================================= */
       
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #0E2F27 !important;
        border-width: 2px !important;
    }
    
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"] > div:hover {
        border-color: #0E2F27 !important;
        box-shadow: 0 0 0 1px #0E2F27 !important;
    }
    
    /* Forzar color oscuro y legible en textos y elementos internos del select */
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {
        color: #0F172A !important;
        fill: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    
    span[data-baseweb="tag"] {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
    }
    span[data-baseweb="tag"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    
    /* CONTENEDOR FLOTANTE / POPOVER / MENÚS DESPLEGABLES (FORZAR FONDO BLANCO) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div, 
    ul[role="listbox"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"],
    div.baseui-menu,
    [data-testid="stMultiSelect"] [data-baseweb="popover"] div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    /* Opciones individuales de la lista desplegable (Select y Multiselect) */
    li[role="option"], 
    div[role="option"],
    [role="listbox"] div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }
    
    li[role="option"] *,
    li[role="option"] span,
    li[role="option"] div,
    div[role="option"] *,
    [role="listbox"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"]:hover {
        background-color: #E2E8F0 !important;
    }
    
    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"] * {
        color: #0E2F27 !important;
        -webkit-text-fill-color: #0E2F27 !important;
    }

    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 2px solid #0E2F27 !important; 
        border-radius: 8px !important; 
        padding: 6px 10px !important;
    }

    /* ========================================================= */

    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stElementToolbar"] { display: none !important; }
    
    .block-container { 
        max-width: 100% !important; 
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #0F172A; }

    /* =========================================================
        CALENDARIO DEL SELECTOR DE FECHA (st.date_input) - forzar tema claro
        ========================================================= */
    div[data-baseweb="popover"], div[data-baseweb="calendar"] {
        background-color: #FFFFFF !important;
    }
    div[data-baseweb="calendar"] *,
    div[data-baseweb="popover"] * {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        fill: #0F172A !important;
    }
    div[data-baseweb="calendar"] button:hover {
        background-color: #EAF3EF !important;
    }
    div[data-baseweb="calendar"] [aria-selected="true"] {
        background-color: #0E2F27 !important;
    }
    div[data-baseweb="calendar"] [aria-selected="true"] * {
        background-color: #0E2F27 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="calendar"] [aria-disabled="true"],
    div[data-baseweb="calendar"] [aria-disabled="true"] * {
        color: #CBD5E1 !important;
    }

    /* Estilo general para botones por defecto (Fondo Blanco, Borde Verde Oscuro 2px) */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button { 
        background-color: #FFFFFF !important;  
        border: 2px solid #0E2F27 !important;
        border-radius: 8px !important; 
        font-weight: 600 !important; 
    }
    
    div[data-testid="stButton"] > button div,
    div[data-testid="stButton"] > button span,
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button label,
    div[data-testid="stButton"] > button svg,
    div[data-testid="stButton"] > button svg path,
    div[data-testid="stDownloadButton"] > button div,
    div[data-testid="stDownloadButton"] > button span,
    div[data-testid="stDownloadButton"] > button p,
    div[data-testid="stDownloadButton"] > button label,
    div[data-testid="stDownloadButton"] > button svg,
    div[data-testid="stDownloadButton"] > button svg path {
        color: #0E2F27 !important;    
        fill: #0E2F27 !important;     
    }

    /* Hover de los botones */
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover { 
        background-color: #0E2F27 !important; 
        border-color: #0E2F27 !important; 
    }

    div[data-testid="stButton"] > button:hover div,
    div[data-testid="stButton"] > button:hover span,
    div[data-testid="stButton"] > button:hover p,
    div[data-testid="stButton"] > button:hover label,
    div[data-testid="stButton"] > button:hover svg,
    div[data-testid="stButton"] > button:hover svg path,
    div[data-testid="stDownloadButton"] > button:hover div,
    div[data-testid="stDownloadButton"] > button:hover span,
    div[data-testid="stDownloadButton"] > button:hover p,
    div[data-testid="stDownloadButton"] > button:hover label,
    div[data-testid="stDownloadButton"] > button:hover svg,
    div[data-testid="stDownloadButton"] > button:hover svg path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* ESTILO ESPECÍFICO PARA LOS 3 BOTONES SUPERIORES (Borde 2px) */
    .contenedor-btn-custom button {
        background-color: #FFFFFF !important;
        border: 2px solid #0E2F27 !important;
        border-radius: 8px !important;
    }
    .contenedor-btn-custom button div,
    .contenedor-btn-custom button span,
    .contenedor-btn-custom button p {
        color: #0E2F27 !important;
        font-weight: 700 !important;
    }
    .contenedor-btn-custom button svg,
    .contenedor-btn-custom button svg path {
        fill: #0E2F27 !important;
    }
    .contenedor-btn-custom button:hover {
        background-color: #0E2F27 !important;
    }
    .contenedor-btn-custom button:hover div,
    .contenedor-btn-custom button:hover span,
    .contenedor-btn-custom button:hover p {
        color: #FFFFFF !important;
    }
    .contenedor-btn-custom button:hover svg,
    .contenedor-btn-custom button:hover svg path {
        fill: #FFFFFF !important;
    }

    .tabla-contenedor, .tabla-contenedor-logs {
        max-height: 550px;
        height: fit-content;
        overflow-y: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px !important;
    }

    .tabla-contenedor-logs {
        max-height: 550px;
        margin-top: 0px !important;
    }

    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
    }
    .tabla-usuarios th {
        background-color: #0E2F27;
        color: #FFFFFF !important;
        padding: 10px 12px;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 700;
    }
    .tabla-usuarios td {
        padding: 9px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
    }
    .tabla-usuarios tr:hover {
        background-color: #F1F5F9;
    }

    div[role="dialog"] *, [data-testid="stDialog"] *, [data-testid="stModal"] * {
        color: #FFFFFF !important;
    }
    div[role="dialog"] button, [data-testid="stDialog"] button {
        background-color: #0E2F27 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
    }

    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 14px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 28px !important; 
        border-top: 6px solid #0E2F27 !important; 
    }

    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0E2F27 !important; 
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

    #logout_btn button {
        background-color: #FFFFFF !important;
        border: 2px solid #0E2F27 !important;
        border-radius: 8px !important;
    }
    #logout_btn button p, #logout_btn button span { color: #0E2F27 !important; font-weight: 700 !important; }
    #logout_btn button:hover { background-color: #0E2F27 !important; }
    #logout_btn button:hover p, #logout_btn button:hover span { color: #FFFFFF !important; }

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

    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        gap: 28px !important; 
        border-bottom: 2px solid #CBD5E1 !important; 
        margin-top: 5px !important; 
    }
    .stTabs [data-baseweb="tab"] p { 
        color: #64748B !important; 
        font-weight: 500 !important; 
        font-size: 15px !important;
    }
    .stTabs [aria-selected="true"] p { 
        color: #0E2F27 !important; 
        font-weight: 700 !important; 
    }

    /* =========================================================
        PAGINACIÓN ESTILO GMAIL (1–50 de 62  ‹  ›)
        ========================================================= */
    .st-key-gmail_paginacion {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
    }
    .st-key-gmail_paginacion div[data-testid="column"] {
        display: flex !important;
        align-items: center !important;
        width: auto !important;
        flex: 0 0 auto !important;
    }
    .gmail-pag-texto {
        color: #5F6368;
        font-size: 13px;
        white-space: nowrap;
        padding-right: 4px;
        font-weight: 500;
    }
    .st-key-gmail_paginacion div[data-testid="stButton"] > button {
        background-color: transparent !important;
        border: none !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        min-height: 30px !important;
        padding: 0 !important;
        margin: 0 2px !important;
        color: #5F6368 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }
    .st-key-gmail_paginacion div[data-testid="stButton"] > button p {
        color: #5F6368 !important;
        font-size: 18px !important;
    }
    .st-key-gmail_paginacion div[data-testid="stButton"] > button:hover:not(:disabled) {
        background-color: #E9EEEC !important;
        border: none !important;
    }
    .st-key-gmail_paginacion div[data-testid="stButton"] > button:hover:not(:disabled) p {
        color: #0E2F27 !important;
    }
    .st-key-gmail_paginacion div[data-testid="stButton"] > button:disabled {
        opacity: 0.35 !important;
        cursor: default !important;
    }

    /* =========================================================
        LISTA INTERACTIVA DE PEDIDOS (fila clickeable con detalle tipo Airtable)
        ========================================================= */
    .st-key-tabla_pedidos_scroll {
        overflow-x: auto !important;
        padding-bottom: 8px !important;
    }
    .st-key-tabla_pedidos_header,
    div[class*="st-key-tabla_pedidos_fila_"] {
        width: 100% !important;
        min-width: 1150px !important;
    }
    .st-key-tabla_pedidos_header {
        background-color: #0E2F27 !important;
        border-radius: 8px 8px 0 0 !important;
    }
    div[class*="st-key-tabla_pedidos_fila_"] {
        border-bottom: 1px solid #E2E8F0 !important;
    }
    div[class*="st-key-tabla_pedidos_fila_"]:hover {
        background-color: #F8FAFC !important;
    }
    div[class*="st-key-tabla_pedidos_fila_"] div[data-testid="stButton"] > button {
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        padding: 0 !important;
        min-height: 30px !important;
        height: 30px !important;
        box-shadow: none !important;
    }
    div[class*="st-key-tabla_pedidos_fila_"] div[data-testid="stButton"] > button:hover {
        color: #0E2F27 !important;
        background-color: transparent !important;
    }

    .st-key-detalle_pedido_nav div[data-testid="stButton"] > button {
        background-color: transparent !important;
        border: none !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        min-height: 30px !important;
        padding: 0 !important;
        color: #5F6368 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }
    .st-key-detalle_pedido_nav div[data-testid="stButton"] > button:hover:not(:disabled) {
        background-color: #E9EEEC !important;
        color: #0E2F27 !important;
    }
    .st-key-detalle_pedido_nav div[data-testid="stButton"] > button:disabled {
        opacity: 0.35 !important;
    }

    .st-key-detalle_pedido_panel {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.06) !important;
        padding: 14px 18px 18px 18px !important;
        max-height: 620px !important;
        overflow-y: auto !important;
    }
    .detalle-pedido-titulo {
        color: #0F172A;
        font-size: 15px;
        font-weight: 700;
        padding-top: 4px;
    }
    div[class*="st-key-tabla_pedidos_fila_"].fila-pedido-activa {
        background-color: #EAF3EF !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# INICIALIZACIÓN DE DATOS (Mocks)
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
            "ESTADO": "Activo",
            "ÚLTIMA CONEXIÓN": "Nunca",
        },
    ])

if "df_pedidos" not in st.session_state:
    st.session_state.df_pedidos = pd.DataFrame([
        {"FECHA_REGISTRO": "24/07/2026", "CODIGO INTERNO": "BLC1-48039", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "CECILIA LOO", "DISTRITO": "ATE", "TIPO_SERVICIO": "SAME-DAY", "DIRECCION": "AV. LA MAR 576", "DEPARTAMENTO": "LIMA", "PROVINCIA": "LIMA", "DOCUMENTO": "TRAMONTINA", "TELEFONO": "999999999", "DESCRIPCION": "CAJAS", "PESO": "1.00", "PLACA": "ABR120", "EVIDENCIA_1": "", "EVIDENCIA_2": "", "EVIDENCIA_3": "", "EVIDENCIA_4": ""},
        {"FECHA_REGISTRO": "23/07/2026", "CODIGO INTERNO": "SIN NUMERO", "CLIENTE": "ALICORP", "ESTADO": "EN RUTA", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "LUIS LLOSA", "DISTRITO": "SAN ISIDRO", "TIPO_SERVICIO": "SAME-DAY", "DIRECCION": "CALLE LAS BEGONIAS 441", "DEPARTAMENTO": "LIMA", "PROVINCIA": "LIMA", "DOCUMENTO": "ALICORP SAA", "TELEFONO": "988888888", "DESCRIPCION": "PAQUETES", "PESO": "3.50", "PLACA": "ABR120", "EVIDENCIA_1": "", "EVIDENCIA_2": "", "EVIDENCIA_3": "", "EVIDENCIA_4": ""},
        {"FECHA_REGISTRO": "22/07/2026", "CODIGO INTERNO": "BLC2-5014", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "JUAN REYES", "DISTRITO": "MIRAFLORES", "TIPO_SERVICIO": "SAME-DAY", "DIRECCION": "AV. LARCO 1301", "DEPARTAMENTO": "LIMA", "PROVINCIA": "LIMA", "DOCUMENTO": "TRAMONTINA", "TELEFONO": "977777777", "DESCRIPCION": "CAJAS", "PESO": "2.10", "PLACA": "ABR120", "EVIDENCIA_1": "", "EVIDENCIA_2": "", "EVIDENCIA_3": "", "EVIDENCIA_4": ""},
        {"FECHA_REGISTRO": "21/07/2026", "CODIGO INTERNO": "BLC2-5015", "CLIENTE": "GLORIA", "ESTADO": "PENDIENTE", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "MARIA PEREZ", "DISTRITO": "LA MOLINA", "TIPO_SERVICIO": "NEXT-DAY", "DIRECCION": "AV. LA MOLINA 1225", "DEPARTAMENTO": "LIMA", "PROVINCIA": "LIMA", "DOCUMENTO": "GLORIA SA", "TELEFONO": "966666666", "DESCRIPCION": "PRODUCTOS LÁCTEOS", "PESO": "5.00", "PLACA": "ABR120", "EVIDENCIA_1": "", "EVIDENCIA_2": "", "EVIDENCIA_3": "", "EVIDENCIA_4": ""},
    ])

# Compatibilidad hacia adelante: si el DataFrame venía sin estas columnas (subida masiva antigua, etc.)
_columnas_detalle_pedido = ["DIRECCION", "DEPARTAMENTO", "PROVINCIA", "DOCUMENTO", "TELEFONO", "DESCRIPCION", "PESO", "PLACA", "EVIDENCIA_1", "EVIDENCIA_2", "EVIDENCIA_3", "EVIDENCIA_4"]
for _col in _columnas_detalle_pedido:
    if _col not in st.session_state.df_pedidos.columns:
        st.session_state.df_pedidos[_col] = ""

if "detalle_pedido_idx" not in st.session_state:
    st.session_state.detalle_pedido_idx = None
if "mostrar_dashboard_pedidos" not in st.session_state:
    st.session_state.mostrar_dashboard_pedidos = False
if "detalle_panel_expandido" not in st.session_state:
    st.session_state.detalle_panel_expandido = False

# POLÍTICA DE ELIMINACIÓN AUTOMÁTICA (MANTENER MÁXIMO 90 DÍAS)
if not st.session_state.df_pedidos.empty and "FECHA_REGISTRO" in st.session_state.df_pedidos.columns:
    st.session_state.df_pedidos["_fecha_dt"] = pd.to_datetime(
        st.session_state.df_pedidos["FECHA_REGISTRO"], format="%d/%m/%Y", errors="coerce"
    )
    limite_90_dias = datetime.now() - timedelta(days=90)
    st.session_state.df_pedidos = st.session_state.df_pedidos[
        st.session_state.df_pedidos["_fecha_dt"] >= limite_90_dias
    ].drop(columns=["_fecha_dt"])

if "historial_acciones" not in st.session_state:
    st.session_state.historial_acciones = pd.DataFrame([
        {
            "FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "USUARIO": "admin",
            "ACCIÓN": "Inicio de sistema",
        }
    ])

def registrar_log(accion):
    nuevo_log = pd.DataFrame([{
        "FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "USUARIO": st.session_state.usuario_actual,
        "ACCIÓN": accion,
    }])
    st.session_state.historial_acciones = pd.concat(
        [nuevo_log, st.session_state.historial_acciones], ignore_index=True
    )

@st.cache_data(show_spinner=False)
def obtener_imagen_github(nombre_archivo="alfa_warehouse.jpg"):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

# LOGO OFICIAL ALFA EXPRESS (reemplaza el emoji 🌲 en todo el sistema)
LOGO_ICON_B64 = obtener_imagen_github("alfa_logo_icon.png")
if LOGO_ICON_B64:
    LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_ICON_B64}" style="height:1em; vertical-align:-0.15em; margin-right:8px;">'
else:
    LOGO_HTML = "🌲"  # Respaldo si aún no se sube el archivo alfa_logo_icon.png

@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
    st.markdown(
        """
    <div style="color: #FFFFFF !important; line-height: 1.6;">
        <p style="color: #FFFFFF !important; font-size: 15px; margin-bottom: 15px;">
            Por motivos de seguridad corporativa, la asignación y restablecimiento de contraseñas es gestionada de manera directa por el área de Administración.
        </p>
        <p style="color: #FFFFFF !important; font-weight: bold; font-size: 15px; margin-bottom: 10px;">
            Canales de atención:
        </p>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">💬 <b>WhatsApp Soporte:</b> +51 987 654 321</div>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo Institucional:</b> <a href="mailto:soporte@alfacargo.pe" style="color: #4ADE80 !important; text-decoration: underline;">soporte@alfacargo.pe</a></div>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 20px;">🕒 <b>Horario de Atención:</b> Lun a Vie de 8:00 am a 6:00 pm</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Entendido", use_container_width=True):
        st.rerun()

@st.dialog("➕ Añadir Registro de Pedido")
def modal_add_pedido():
    with st.form("add_p"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código Interno")
        cli = c2.text_input("Cliente")
        nom = st.text_input("Nombre Destinatario")
        est = st.selectbox("Estado", ["ENTREGADO", "EN RUTA", "PENDIENTE"])

        with st.expander("📋 Detalles adicionales del pedido"):
            c3, c4 = st.columns(2)
            direccion = c3.text_input("Dirección")
            documento = c4.text_input("Documento / Empresa")
            c5, c6 = st.columns(2)
            departamento = c5.text_input("Departamento", value="LIMA")
            provincia = c6.text_input("Provincia", value="LIMA")
            c7, c8 = st.columns(2)
            telefono = c7.text_input("Teléfono")
            placa = c8.text_input("Placa del vehículo")
            c9, c10 = st.columns(2)
            descripcion = c9.text_input("Descripción de la carga")
            peso = c10.text_input("Peso (kg)")
            evidencia_files = st.file_uploader(
                "Evidencia de entrega (hasta 4 fotos subidas por el repartidor desde su celular)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
            )

        if st.form_submit_button("Guardar Pedido", use_container_width=True):
            evidencias_b64 = ["", "", "", ""]
            if evidencia_files:
                for i, archivo in enumerate(evidencia_files[:4]):
                    evidencias_b64[i] = "data:image/png;base64," + base64.b64encode(archivo.read()).decode("utf-8")

            nuevo = pd.DataFrame([{
                "FECHA_REGISTRO": datetime.now().strftime("%d/%m/%Y"),
                "CODIGO INTERNO": cod,
                "CLIENTE": cli,
                "ESTADO": est,
                "SUB_ESTADO": "REGISTRADO",
                "NOMBRE": nom,
                "DISTRITO": "LIMA",
                "TIPO_SERVICIO": "SAME-DAY",
                "DIRECCION": direccion,
                "DEPARTAMENTO": departamento,
                "PROVINCIA": provincia,
                "DOCUMENTO": documento,
                "TELEFONO": telefono,
                "DESCRIPCION": descripcion,
                "PESO": peso,
                "PLACA": placa,
                "EVIDENCIA_1": evidencias_b64[0],
                "EVIDENCIA_2": evidencias_b64[1],
                "EVIDENCIA_3": evidencias_b64[2],
                "EVIDENCIA_4": evidencias_b64[3],
            }])
            st.session_state.df_pedidos = pd.concat([st.session_state.df_pedidos, nuevo], ignore_index=True)
            registrar_log(f"Añadió pedido {cod}")
            st.rerun()

def mostrar_detalle_pedido():
    df = st.session_state.df_pedidos
    indices = st.session_state.get("detalle_pedido_lista_indices") or df.index.tolist()
    indices = [i for i in indices if i in df.index]

    if st.session_state.detalle_pedido_idx not in indices:
        st.session_state.detalle_pedido_idx = None
        st.rerun()
        return

    idx_actual = st.session_state.detalle_pedido_idx
    pos = indices.index(idx_actual)
    fila = df.loc[idx_actual]
    expandido = st.session_state.get("detalle_panel_expandido", False)

    with st.container(key="detalle_pedido_panel"):
        with st.container(key="detalle_pedido_nav"):
            c_title, c_prev, c_next, c_expand, c_close = st.columns([3.2, 0.6, 0.6, 0.6, 0.6])
            with c_title:
                st.markdown("<div class='detalle-pedido-titulo'>Pedidos filtro</div>", unsafe_allow_html=True)
            with c_prev:
                if st.button("‹", key="detalle_prev", disabled=(pos <= 0)):
                    st.session_state.detalle_pedido_idx = indices[pos - 1]
                    st.rerun()
            with c_next:
                if st.button("›", key="detalle_next", disabled=(pos >= len(indices) - 1)):
                    st.session_state.detalle_pedido_idx = indices[pos + 1]
                    st.rerun()
            with c_expand:
                if st.button("⤢", key="detalle_expand"):
                    st.session_state.detalle_panel_expandido = not expandido
                    st.rerun()
            with c_close:
                if st.button("✕", key="detalle_close"):
                    st.session_state.detalle_pedido_idx = None
                    st.session_state.detalle_panel_expandido = False
                    st.rerun()

        campos_detalle = [
            ("NOMBRE", "NOMBRE"), ("DIRECCION", "DIRECCION"), ("DEPARTAMENTO", "DEPARTAMENTO"),
            ("PROVINCIA", "PROVINCIA"), ("DISTRITO", "DISTRITO"), ("DOCUMENTO", "DOCUMENTO"),
            ("TELEFONO", "TELEFONO"), ("DESCRIPCION", "DESCRIPCION"), ("PESO", "PESO"),
            ("TIPO_SERVICIO", "TIPO_SERVICIO"), ("PLACA", "PLACA"),
        ]
        filas_detalle_html = ""
        for etiqueta, columna in campos_detalle:
            valor = fila[columna] if columna in fila.index and str(fila[columna]).strip() else "—"
            filas_detalle_html += f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid #E2E8F0;">
                <span style="color:#64748B; font-size:12px; font-weight:700; letter-spacing:0.3px;">{etiqueta}</span>
                <span style="color:#0F172A; font-size:14px; text-align:right;">{valor}</span>
            </div>"""
        st.markdown(filas_detalle_html, unsafe_allow_html=True)

        st.markdown("<p style='color:#64748B; font-size:12px; font-weight:700; margin-top:16px; margin-bottom:6px;'>EVIDENCIAS (hasta 4 fotos del repartidor)</p>", unsafe_allow_html=True)
        evidencias = [fila.get(f"EVIDENCIA_{n}", "") for n in range(1, 5)]
        evidencias_con_foto = [e for e in evidencias if isinstance(e, str) and e.strip()]
        if evidencias_con_foto:
            col_ev1, col_ev2 = st.columns(2)
            for i, foto in enumerate(evidencias_con_foto):
                (col_ev1 if i % 2 == 0 else col_ev2).image(foto, use_container_width=True)
        else:
            st.markdown(
                "<p style='color:#94A3B8; font-size:13px;'>Aún no hay evidencia subida por el repartidor desde su celular para este pedido.</p>",
                unsafe_allow_html=True,
            )


@st.dialog("📤 Subir Data Masiva")
def modal_upload():
    uploaded_file = st.file_uploader("Selecciona archivo Excel o CSV", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_nuevo = pd.read_csv(uploaded_file)
            else:
                df_nuevo = pd.read_excel(uploaded_file)
            
            if st.button("Procesar y Cargar"):
                columnas_requeridas = ["FECHA_REGISTRO", "CODIGO INTERNO", "CLIENTE", "ESTADO", "SUB_ESTADO", "NOMBRE", "DISTRITO", "TIPO_SERVICIO"]
                
                # Normalizar nombres de columnas a mayúsculas por si acaso
                df_nuevo.columns = [str(c).strip().upper() for c in df_nuevo.columns]
                
                faltantes = [col for col in columnas_requeridas if col not in df_nuevo.columns]
                if faltantes:
                    st.error(f"El archivo no cuenta con las columnas obligatorias requeridas: {', '.join(faltantes)}")
                else:
                    df_a_cargar = df_nuevo[columnas_requeridas].copy()
                    for _col in _columnas_detalle_pedido:
                        df_a_cargar[_col] = df_nuevo[_col] if _col in df_nuevo.columns else ""
                    st.session_state.df_pedidos = pd.concat([st.session_state.df_pedidos, df_a_cargar], ignore_index=True)
                    registrar_log("Subida y carga exitosa de archivo masivo")
                    st.success("¡Datos cargados correctamente!")
                    st.rerun()
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo: {e}")

def _grafico_barras_html(serie, color="#0E2F27", alto_px=200):
    if serie.empty or serie.sum() == 0:
        return "<p style='color:#94A3B8; font-size:13px;'>Sin datos para graficar.</p>"

    valor_max = float(serie.max())
    pasos = 5
    paso = max(1, -(-int(valor_max) // pasos))  # redondeo hacia arriba
    max_eje = paso * pasos

    lineas_y_html = "".join(
        f"<div style='position:absolute; left:0; right:0; top:{100 - (i/pasos)*100:.2f}%; border-top:1px solid #EEF2F6;'></div>"
        for i in range(pasos + 1)
    )
    etiquetas_y_html = "".join(
        f"<div style='position:absolute; left:0; top:{100 - (i/pasos)*100:.2f}%; transform:translateY(-50%); font-size:10px; color:#94A3B8;'>{paso * i}</div>"
        for i in range(pasos + 1)
    )
    barras_html = "".join(
        f"<div style='flex:1; height:100%; display:flex; align-items:flex-end; justify-content:center;'>"
        f"<div title='{etiqueta}: {int(valor)}' style='width:55%; min-height:2px; border-radius:3px 3px 0 0; "
        f"background:{color}; height:{(valor / max_eje) * 100:.2f}%;'></div></div>"
        for etiqueta, valor in serie.items()
    )
    etiquetas_x_html = "".join(
        f"<div style='flex:1; text-align:center; font-size:10px; color:#64748B; white-space:nowrap; "
        f"overflow:hidden; text-overflow:ellipsis; padding-top:6px;'>{etiqueta}</div>"
        for etiqueta in serie.index
    )

    return f"""
    <div style="display:flex; margin-top:8px;">
        <div style="position:relative; width:28px; flex-shrink:0; height:{alto_px}px;">{etiquetas_y_html}</div>
        <div style="flex:1;">
            <div style="position:relative; height:{alto_px}px; border-left:1px solid #CBD5E1; border-bottom:1px solid #CBD5E1;">
                {lineas_y_html}
                <div style="position:absolute; inset:0; display:flex; padding:0 4px;">{barras_html}</div>
            </div>
            <div style="display:flex; padding:0 4px;">{etiquetas_x_html}</div>
        </div>
    </div>
    """

def mostrar_dashboard_pedidos(df, filtrado):
    expandido = st.session_state.get("detalle_panel_expandido", False)

    with st.container(key="detalle_pedido_panel"):
        with st.container(key="detalle_pedido_nav"):
            c_title, c_expand, c_close = st.columns([4.4, 0.6, 0.6])
            with c_title:
                st.markdown("<div class='detalle-pedido-titulo'>📊 Dashboard</div>", unsafe_allow_html=True)
            with c_expand:
                if st.button("⤢", key="dashboard_expand"):
                    st.session_state.detalle_panel_expandido = not expandido
                    st.rerun()
            with c_close:
                if st.button("✕", key="dashboard_close"):
                    st.session_state.mostrar_dashboard_pedidos = False
                    st.session_state.detalle_panel_expandido = False
                    st.rerun()

        if filtrado:
            st.markdown(f"<p style='color:#64748B; font-size:13px; margin-top:2px;'>Basado en los <b>{len(df)}</b> resultados de tu filtro actual.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:#64748B; font-size:13px; margin-top:2px;'>Basado en el total de <b>{len(df)}</b> pedidos (sin filtros aplicados).</p>", unsafe_allow_html=True)

        if df.empty:
            st.markdown("<p style='color:#94A3B8; font-size:13px; padding:20px 0;'>No hay registros para graficar con los filtros actuales.</p>", unsafe_allow_html=True)
            return

        conteo_estado = df["ESTADO"].astype(str).value_counts() if "ESTADO" in df.columns else pd.Series(dtype=int)

        st.markdown("<p style='font-weight:700; font-size:13px; color:#0E2F27; margin:0 0 4px 0;'>Avance de Ruta (por Estado)</p>", unsafe_allow_html=True)
        if not conteo_estado.empty:
            colores_torta = ["#0E2F27", "#4ADE80", "#94A3B8", "#CBD5E1", "#16A34A", "#0F172A"]
            total_torta = int(conteo_estado.sum())
            segmentos_css = []
            leyenda_html = ""
            acumulado_pct = 0.0
            for i, (etiqueta, valor) in enumerate(conteo_estado.items()):
                color = colores_torta[i % len(colores_torta)]
                pct = (valor / total_torta) * 100 if total_torta else 0
                inicio = acumulado_pct
                fin = acumulado_pct + pct
                segmentos_css.append(f"{color} {inicio:.2f}% {fin:.2f}%")
                acumulado_pct = fin
                leyenda_html += (
                    f"<div style='display:flex; align-items:center; gap:6px; font-size:12px; color:#0F172A; margin-bottom:4px;'>"
                    f"<span style='width:10px; height:10px; border-radius:2px; background:{color}; display:inline-block;'></span>"
                    f"{etiqueta} — {valor} ({pct:.0f}%)</div>"
                )
            gradiente = ", ".join(segmentos_css)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:18px; margin-top:6px;">
                <div style="width:120px; height:120px; border-radius:50%; flex-shrink:0;
                            background:conic-gradient({gradiente});
                            display:flex; align-items:center; justify-content:center;">
                    <div style="width:64px; height:64px; border-radius:50%; background:#FFFFFF;
                                display:flex; align-items:center; justify-content:center;
                                font-size:12px; font-weight:700; color:#0E2F27;">{total_torta}</div>
                </div>
                <div>{leyenda_html}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<p style='font-weight:700; font-size:13px; color:#0E2F27; margin:20px 0 4px 0;'>Cantidad de Pedidos</p>", unsafe_allow_html=True)
        if "FECHA_REGISTRO" in df.columns:
            conteo_fecha = df["FECHA_REGISTRO"].astype(str).value_counts()
            fechas_dt = pd.to_datetime(conteo_fecha.index, format="%d/%m/%Y", errors="coerce")
            conteo_fecha = conteo_fecha.iloc[fechas_dt.argsort()]
            st.markdown(_grafico_barras_html(conteo_fecha, color="#0E2F27"), unsafe_allow_html=True)



if st.session_state.usuario_actual is None:
    # Fondo verde minimalista (gradiente + resplandor, sin logo ni íconos de logística)
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 50% 32%, rgba(74, 222, 128, 0.22) 0%, rgba(74, 222, 128, 0) 45%),
                linear-gradient(160deg, #03110C 0%, #0E2F27 48%, #0B2A22 75%, #04140F 100%) !important;
            background-attachment: fixed !important;
        }

        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.99) !important;
            border-radius: 20px !important;
            padding: 44px 40px 30px 40px !important;
            box-shadow: 0 35px 80px rgba(0, 0, 0, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }

        div.login-ayuda-wrap button {
            background-color: transparent !important;
            color: #DCFCE7 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(220, 252, 231, 0.35) !important;
            box-shadow: none !important;
        }
        div.login-ayuda-wrap button:hover {
            border-color: rgba(220, 252, 231, 0.7) !important;
            color: #FFFFFF !important;
        }
        div.login-ayuda-wrap button p {
            color: inherit !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 7vh;">
        <div style="font-size: 26px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.3px;">{LOGO_HTML} ALFA CARGO EXPRESS</div>
        <div style='color: #A7F3D0; font-size: 13px; font-weight: 600;'>🌐 Central Lima, Perú</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)

    col_izq, col_centro, col_der = st.columns([1, 1.05, 1])
    with col_centro:
        with st.form("login_form"):
            st.markdown(
                '<h3 style="text-align: center; color: #0E2F27; font-weight:800;'
                ' margin-bottom: 24px;">Bienvenido</h3>',
                unsafe_allow_html=True,
            )
            input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
            input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
            remember = st.checkbox("Recordar inicio de sesión", value=True)
            submit_btn = st.form_submit_button("Ingresar al Portal", use_container_width=True)

            if submit_btn:
                df_users = st.session_state.usuarios_registrados
                user_match = df_users[
                    (df_users["USUARIO"] == input_user)
                    & (df_users["PASS"] == input_pass)
                ]

                if not user_match.empty:
                    st.session_state.usuario_actual = input_user
                    st.session_state.rol_actual = user_match.iloc[0]["ROL"]
                    st.session_state.usuarios_registrados.loc[
                        st.session_state.usuarios_registrados["USUARIO"] == input_user,
                        "ÚLTIMA CONEXIÓN",
                    ] = datetime.now().strftime("%Y-%m-%d %H:%M")

                    if remember:
                        st.query_params["saved_user"] = input_user
                        st.query_params["saved_rol"] = st.session_state.rol_actual

                    registrar_log("Inicio de sesión exitoso")
                    st.rerun()

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="login-ayuda-wrap">', unsafe_allow_html=True)
        if st.button("❓ ¿Necesitas ayuda con tu acceso o contraseña?", use_container_width=True):
            mostrar_modal_soporte()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0E2F27; margin-bottom: 0px;">{LOGO_HTML} PORTAL {str(st.session_state.usuario_actual).upper()}</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 2px;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong></div>
            """,
            unsafe_allow_html=True,
        )
    with col_nav2:
        st.markdown('<div id="logout_btn">', unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", key="logout"):
            registrar_log("Cierre de sesión")
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.query_params.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 8px 0px 8px 0px; border-color: #CBD5E1;'>", unsafe_allow_html=True)

    # ==========================================
    # VISTA 1: PORTAL OPERARIO
    # ==========================================
    if st.session_state.rol_actual == "🛠️ Operario":
        csv = st.session_state.df_pedidos.to_csv(index=False).encode('utf-8')
        
        st.markdown("<h3 style='margin:0 0 8px 0; padding:0; line-height: 1.2;'>Gestión de Envíos</h3>", unsafe_allow_html=True)
        
        _, col_b1, col_b2, col_b3, col_b4 = st.columns([1.8, 0.9, 0.9, 0.9, 0.9])
        
        with col_b1:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            st.download_button("📥 Descargar", data=csv, file_name="pedidos.csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b2:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("📤 Cargar Data", use_container_width=True): modal_upload()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b3:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("➕ Nuevo Pedido", use_container_width=True): modal_add_pedido()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b4:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("📊 Dashboard", use_container_width=True, key="btn_dashboard_pedidos"):
                st.session_state.mostrar_dashboard_pedidos = True
                st.session_state.detalle_pedido_idx = None
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 2px;'></div>", unsafe_allow_html=True)

        # ------------------------------------------
        # FILTROS EN EL SIDEBAR
        # ------------------------------------------
        with st.sidebar:
            st.markdown(f"<h2 style='color: #0E2F27; margin: 0px 0px 4px 0px; padding: 0px; white-space: nowrap; font-size: 22px; font-weight: 800;'>{LOGO_HTML} ALFA EXPRESS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; color: #64748B; margin-top: 0px; margin-bottom: 14px; line-height: 1.4;'>Filtra los registros de envíos de manera rápida.</p>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 0px 0px 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0E2F27; margin:0 0 6px 0;'>📅 Rango de Fechas:</p>", unsafe_allow_html=True)
            fecha_inicio_sel = st.date_input("Fecha Inicial", value=None, format="DD/MM/YYYY", key="f_ini")
            fecha_fin_sel = st.date_input("Fecha Final", value=None, format="DD/MM/YYYY", key="f_fin")

            st.markdown("<hr style='margin: 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0E2F27; margin:0 0 6px 0;'>🔍 Búsqueda por Texto:</p>", unsafe_allow_html=True)
            filtro_codigo_txt = st.text_input("Código Interno", placeholder="Ej: BLC1-480...", key="b_cod")
            filtro_nombre_txt = st.text_input("Nombre Destinatario", placeholder="Ej: Cecilia Loo...", key="b_nom")

            st.markdown("<hr style='margin: 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0E2F27; margin:0 0 6px 0;'>📌 Selección Múltiple:</p>", unsafe_allow_html=True)
            
            clientes_unicos = sorted(st.session_state.df_pedidos["CLIENTE"].astype(str).unique().tolist())
            filtro_cliente = st.multiselect("Cliente", options=clientes_unicos, placeholder="Todos")

            distritos_unicos = sorted(st.session_state.df_pedidos["DISTRITO"].astype(str).unique().tolist())
            filtro_distrito = st.multiselect("Distrito", options=distritos_unicos, placeholder="Todos")

            TIPOS_SERVICIO_VALIDOS = ["NEXT-DAY", "SAME-DAY", "LOGISTICA INVERSA"]
            servicios_unicos = sorted(set(TIPOS_SERVICIO_VALIDOS) | set(st.session_state.df_pedidos["TIPO_SERVICIO"].astype(str).unique().tolist()))
            filtro_servicio = st.multiselect("Tipo de Servicio", options=servicios_unicos, placeholder="Todos")

            estados_unicos = sorted(st.session_state.df_pedidos["ESTADO"].astype(str).unique().tolist())
            filtro_estado = st.multiselect("Estado", options=estados_unicos, placeholder="Todos")

            sub_estados_unicos = sorted(st.session_state.df_pedidos["SUB_ESTADO"].astype(str).unique().tolist())
            filtro_sub_estado = st.multiselect("Sub Estado", options=sub_estados_unicos, placeholder="Todos")

        # APLICAR FILTROS
        df_filtrado = st.session_state.df_pedidos.copy()

        if "FECHA_REGISTRO" in df_filtrado.columns:
            df_filtrado["_fecha_temp"] = pd.to_datetime(df_filtrado["FECHA_REGISTRO"], format="%d/%m/%Y", errors="coerce")

            if fecha_inicio_sel and fecha_fin_sel:
                df_filtrado = df_filtrado[(df_filtrado["_fecha_temp"].dt.date >= fecha_inicio_sel) & (df_filtrado["_fecha_temp"].dt.date <= fecha_fin_sel)]
            elif fecha_inicio_sel and not fecha_fin_sel:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date == fecha_inicio_sel]
            elif not fecha_inicio_sel and fecha_fin_sel:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date <= fecha_fin_sel]

            df_filtrado = df_filtrado.drop(columns=["_fecha_temp"])

        if filtro_cliente: df_filtrado = df_filtrado[df_filtrado["CLIENTE"].astype(str).isin(filtro_cliente)]
        if filtro_distrito: df_filtrado = df_filtrado[df_filtrado["DISTRITO"].astype(str).isin(filtro_distrito)]
        if filtro_servicio: df_filtrado = df_filtrado[df_filtrado["TIPO_SERVICIO"].astype(str).isin(filtro_servicio)]
        if filtro_estado: df_filtrado = df_filtrado[df_filtrado["ESTADO"].astype(str).isin(filtro_estado)]
        if filtro_sub_estado: df_filtrado = df_filtrado[df_filtrado["SUB_ESTADO"].astype(str).isin(filtro_sub_estado)]

        if filtro_codigo_txt: df_filtrado = df_filtrado[df_filtrado["CODIGO INTERNO"].astype(str).str.contains(filtro_codigo_txt, case=False, na=False)]
        if filtro_nombre_txt: df_filtrado = df_filtrado[df_filtrado["NOMBRE"].astype(str).str.contains(filtro_nombre_txt, case=False, na=False)]

        if "FECHA_REGISTRO" in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by="FECHA_REGISTRO", ascending=False)

        total_sin_filtrar = len(st.session_state.df_pedidos)
        hay_filtros_activos = any([
            fecha_inicio_sel, fecha_fin_sel,
            filtro_cliente, filtro_distrito, filtro_servicio, filtro_estado, filtro_sub_estado,
            filtro_codigo_txt.strip(), filtro_nombre_txt.strip(),
        ])

        # ==========================================
        # LÓGICA DE PAGINACIÓN (BLOQUES DE 50) - ESTILO GMAIL
        # ==========================================
        TAMANO_PAGINA = 50
        total_registros = len(df_filtrado)
        total_paginas = max(1, (total_registros + TAMANO_PAGINA - 1) // TAMANO_PAGINA)

        if "pagina_actual_pedidos" not in st.session_state:
            st.session_state.pagina_actual_pedidos = 1

        # Si los filtros reducen el total de páginas, no dejar la página fuera de rango
        if st.session_state.pagina_actual_pedidos > total_paginas:
            st.session_state.pagina_actual_pedidos = total_paginas
        if st.session_state.pagina_actual_pedidos < 1:
            st.session_state.pagina_actual_pedidos = 1

        pagina_actual = st.session_state.pagina_actual_pedidos
        inicio_idx = (pagina_actual - 1) * TAMANO_PAGINA
        fin_idx = min(inicio_idx + TAMANO_PAGINA, total_registros)
        rango_texto = f"{inicio_idx + 1}\u2013{fin_idx} de {total_registros}" if total_registros > 0 else "0 de 0"

        col_pag1, col_pag2 = st.columns([3, 1])
        with col_pag1:
            if hay_filtros_activos:
                texto_resultados = f"🔍 Se encontr{'ó' if total_registros == 1 else 'aron'} <b>{total_registros}</b> resultado{'s' if total_registros != 1 else ''} para tu filtro (de {total_sin_filtrar} en total)."
            else:
                texto_resultados = f"Mostrando bloques de 50 registros. Total: <b>{total_registros}</b>."
            st.markdown(f"<p style='color: #475569; font-size: 14px; margin-top: 8px;'>{texto_resultados}</p>", unsafe_allow_html=True)
        with col_pag2:
            with st.container(key="gmail_paginacion"):
                c_txt, c_prev, c_next = st.columns([2.4, 0.8, 0.8])
                with c_txt:
                    st.markdown(f"<div class='gmail-pag-texto'>{rango_texto}</div>", unsafe_allow_html=True)
                with c_prev:
                    if st.button("‹", key="pag_prev", disabled=(pagina_actual <= 1)):
                        st.session_state.pagina_actual_pedidos -= 1
                        st.rerun()
                with c_next:
                    if st.button("›", key="pag_next", disabled=(pagina_actual >= total_paginas)):
                        st.session_state.pagina_actual_pedidos += 1
                        st.rerun()

        # Cortar el DataFrame según la página seleccionada
        df_paginado = df_filtrado.iloc[inicio_idx:fin_idx]
        st.session_state.detalle_pedido_lista_indices = df_filtrado.index.tolist()

        columnas_pedidos_tabla = ["FECHA_REGISTRO", "CODIGO INTERNO", "CLIENTE", "ESTADO", "SUB_ESTADO", "NOMBRE", "DISTRITO", "TIPO_SERVICIO"]
        anchos_columnas_px = [130, 150, 130, 120, 150, 150, 120, 130]  # ancho MÍNIMO por columna (en píxeles); puede crecer si hay espacio

        def _fila_pedido_html(valores, es_encabezado):
            color = "#FFFFFF" if es_encabezado else "#0F172A"
            peso_fuente = "700" if es_encabezado else "400"
            tam_fuente = "12px" if es_encabezado else "13px"
            transform = "text-transform:uppercase;" if es_encabezado else ""
            celdas = "".join(
                f"<div style='flex:1 0 {ancho}px; padding:9px 8px; white-space:nowrap; overflow:hidden; "
                f"text-overflow:ellipsis; color:{color}; font-size:{tam_fuente}; font-weight:{peso_fuente}; {transform}'>{valor}</div>"
                for valor, ancho in zip(valores, anchos_columnas_px)
            )
            return f"<div style='display:flex; align-items:center;'>{celdas}</div>"

        detalle_abierto = st.session_state.detalle_pedido_idx is not None
        dashboard_abierto = st.session_state.mostrar_dashboard_pedidos
        panel_abierto = detalle_abierto or dashboard_abierto
        panel_expandido = st.session_state.get("detalle_panel_expandido", False)

        if panel_abierto and panel_expandido:
            col_tabla, col_detalle = None, st.container()
        elif panel_abierto:
            col_tabla, col_detalle = st.columns([1.6, 1], gap="medium")
        else:
            col_tabla, col_detalle = st.container(), None

        if col_tabla is not None:
            with col_tabla:
                with st.container(key="tabla_pedidos_scroll"):
                    with st.container(key="tabla_pedidos_header"):
                        c_txt, c_btn = st.columns([0.94, 0.06])
                        c_txt.markdown(_fila_pedido_html(columnas_pedidos_tabla, es_encabezado=True), unsafe_allow_html=True)
                        c_btn.markdown("&nbsp;", unsafe_allow_html=True)

                    if df_paginado.empty:
                        st.markdown("<p style='color:#94A3B8; font-size:13px; padding:16px 8px;'>No se encontraron pedidos con los filtros aplicados.</p>", unsafe_allow_html=True)
                    else:
                        for idx_real, fila in df_paginado.iterrows():
                            es_fila_activa = detalle_abierto and idx_real == st.session_state.detalle_pedido_idx
                            if es_fila_activa:
                                st.markdown(f"<style>.st-key-tabla_pedidos_fila_{idx_real} {{ background-color: #EAF3EF !important; }}</style>", unsafe_allow_html=True)
                            with st.container(key=f"tabla_pedidos_fila_{idx_real}"):
                                c_txt, c_btn = st.columns([0.94, 0.06])
                                valores_fila = [fila[col] if col in fila.index else "" for col in columnas_pedidos_tabla]
                                c_txt.markdown(_fila_pedido_html(valores_fila, es_encabezado=False), unsafe_allow_html=True)
                                with c_btn:
                                    if st.button("›", key=f"ver_pedido_{idx_real}"):
                                        st.session_state.detalle_pedido_idx = idx_real
                                        st.session_state.mostrar_dashboard_pedidos = False
                                        st.rerun()

        if col_detalle is not None:
            with col_detalle:
                if dashboard_abierto:
                    mostrar_dashboard_pedidos(df_filtrado, hay_filtros_activos)
                else:
                    mostrar_detalle_pedido()



    # ==========================================
    # VISTA 2: PORTAL ADMINISTRADOR
    # ==========================================
    elif st.session_state.rol_actual == "👨‍💼 Portal Administrador":
        tab_users, tab_logs = st.tabs(["👥 Gestión de Usuarios y Roles", "📋 Auditoría y Registros (Logs)"])

        with tab_users:
            st.markdown("<h3 style='margin-top: 0px; margin-bottom: 12px;'>Panel de Control de Accesos</h3>", unsafe_allow_html=True)
            
            with st.form("form_crear_usuario"):
                st.markdown("<b>Registrar Nuevo Usuario / Personalizar Rol</b>", unsafe_allow_html=True)
                col_u1, col_u2, col_u3 = st.columns(3)
                nuevo_usuario = col_u1.text_input("Nombre de Usuario")
                nuevo_pass = col_u2.text_input("Contraseña Temporal", type="password")
                
                # --- LÍNEA CORREGIDA ---
                nr = st.selectbox("Rol Asignado", options=["👨‍💼 Portal Administrador", "🛠️ Operario", "🛵 Repartidor (App)", "🏢 Cliente"])
                
                if st.form_submit_button("Crear / Actualizar Usuario", use_container_width=True):
                    if nuevo_usuario.strip() and nuevo_pass.strip():
                        df_u = st.session_state.usuarios_registrados
                        if nuevo_usuario in df_u["USUARIO"].values:
                            st.session_state.usuarios_registrados.loc[df_u["USUARIO"] == nuevo_usuario, "PASS"] = nuevo_pass
                            st.session_state.usuarios_registrados.loc[df_u["USUARIO"] == nuevo_usuario, "ROL"] = nr
                            registrar_log(f"Actualizó credenciales/rol para: {nuevo_usuario}")
                            st.success(f"¡Usuario '{nuevo_usuario}' actualizado correctamente!")
                        else:
                            nuevo_reg = pd.DataFrame([{
                                "USUARIO": nuevo_usuario,
                                "PASS": nuevo_pass,
                                "ROL": nr,
                                "ESTADO": "Activo",
                                "ÚLTIMA CONEXIÓN": "Nunca"
                            }])
                            st.session_state.usuarios_registrados = pd.concat([df_u, nuevo_reg], ignore_index=True)
                            registrar_log(f"Creó nuevo usuario: {nuevo_usuario}")
                            st.success(f"¡Usuario '{nuevo_usuario}' creado exitosamente!")
                        st.rerun()
                    else:
                        st.error("Por favor completa el usuario y la contraseña.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<b>Usuarios Registrados en el Sistema</b>", unsafe_allow_html=True)
            
            df_usuarios_view = st.session_state.usuarios_registrados.copy()
            
            filas_u_html = ""
            for _, fila in df_usuarios_view.iterrows():
                filas_u_html += f"<tr><td>{fila['USUARIO']}</td><td>{fila['ROL']}</td><td>{fila['ESTADO']}</td><td>{fila['ÚLTIMA CONEXIÓN']}</td></tr>"

            tabla_u_html = f"""
                <div class="tabla-contenedor">
                    <table class="tabla-usuarios">
                        <thead>
                            <tr><th>USUARIO</th><th>ROL</th><th>ESTADO</th><th>ÚLTIMA CONEXIÓN</th></tr>
                        </thead>
                        <tbody>
                            {filas_u_html}
                        </tbody>
                    </table>
                </div>
            """
            st.markdown(tabla_u_html, unsafe_allow_html=True)

        with tab_logs:
            st.markdown("<h3 style='margin-top: 0px; margin-bottom: 12px;'>Registro de Auditoría y Acciones</h3>", unsafe_allow_html=True)
            
            df_logs = st.session_state.historial_acciones.copy()
            filas_l_html = ""
            for _, fila in df_logs.iterrows():
                filas_l_html += f"<tr><td>{fila['FECHA Y HORA']}</td><td>{fila['USUARIO']}</td><td>{fila['ACCIÓN']}</td></tr>"

            tabla_l_html = f"""
                <div class="tabla-contenedor-logs">
                    <table class="tabla-usuarios">
                        <thead>
                            <tr><th>FECHA Y HORA</th><th>USUARIO</th><th>ACCIÓN</th></tr>
                        </thead>
                        <tbody>
                            {filas_l_html}
                        </tbody>
                    </table>
                </div>
            """
            st.markdown(tabla_l_html, unsafe_allow_html=True)
