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

# CSS GENERAL DEL SISTEMA
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
       ESTILO OSCURO Y ELEGANTE FIJO PARA TODOS LOS BOTONES
       ========================================================== */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button { 
        background-color: #1E293B !important;  
        border: 1px solid #334155 !important;
        border-radius: 8px !important; 
        font-weight: 600 !important; 
    }
    
    div[data-testid="stButton"] > button div,
    div[data-testid="stButton"] > button span,
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button label,
    div[data-testid="stDownloadButton"] > button div,
    div[data-testid="stDownloadButton"] > button span,
    div[data-testid="stDownloadButton"] > button p,
    div[data-testid="stDownloadButton"] > button label {
        color: #FFFFFF !important;    
        fill: #FFFFFF !important;     
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover { 
        background-color: #0F382C !important; 
        border-color: #0F382C !important; 
    }
    div[data-testid="stButton"] > button:hover div,
    div[data-testid="stButton"] > button:hover span,
    div[data-testid="stButton"] > button:hover p,
    div[data-testid="stDownloadButton"] > button:hover div,
    div[data-testid="stDownloadButton"] > button:hover span,
    div[data-testid="stDownloadButton"] > button:hover p {
        color: #FFFFFF !important; 
    }

    /* CONTENEDORES CON SCROLL INTELIGENTE PARA TABLAS */
    .tabla-contenedor, .tabla-contenedor-logs {
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
    .tabla-contenedor-logs::-webkit-scrollbar {
        width: 6px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-track,
    .tabla-contenedor-logs::-webkit-scrollbar-track {
        background: transparent !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb,
    .tabla-contenedor-logs::-webkit-scrollbar-thumb {
        background-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb:hover,
    .tabla-contenedor-logs::-webkit-scrollbar-thumb:hover {
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
            "ESTADO": "Activo",
            "ÚLTIMA CONEXIÓN": "Nunca",
        },
    ])

if "df_pedidos" not in st.session_state:
    st.session_state.df_pedidos = pd.DataFrame([
        {"FECHA_REGISTRO": "24/07/2026", "CODIGO INTERNO": "BLC1-48039", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "CECILIA LOO", "DISTRITO": "ATE", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "23/07/2026", "CODIGO INTERNO": "SIN NUMERO", "CLIENTE": "ALICORP", "ESTADO": "EN RUTA", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "LUIS LLOSA", "DISTRITO": "SAN ISIDRO", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "22/07/2026", "CODIGO INTERNO": "BLC2-5014", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "JUAN REYES", "DISTRITO": "MIRAFLORES", "TIPO_SERVICIO": "SAME-DAY"}
    ])

if (
    "ÚLTIMA CONEXIÓN"
    not in st.session_state.usuarios_registrados.columns
):
    st.session_state.usuarios_registrados["ÚLTIMA CONEXIÓN"] = "Nunca"

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


def obtener_imagen_github(nombre_archivo="alfa_warehouse.jpg"):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


# MODAL DE SOPORTE
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
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo Institucional:</b> <a href="mailto:soporte@alfacargo.pe" style="color: #38BDF8 !important; text-decoration: underline;">soporte@alfacargo.pe</a></div>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 20px;">🕒 <b>Horario de Atención:</b> Lun a Vie de 8:00 am a 6:00 pm</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("Entendido", use_container_width=True):
        st.rerun()

# MODALES PARA OPERARIO
@st.dialog("➕ Añadir Registro de Pedido")
def modal_add_pedido():
    with st.form("add_p"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código Interno")
        cli = c2.text_input("Cliente")
        nom = st.text_input("Nombre Destinatario")
        est = st.selectbox("Estado", ["ENTREGADO", "EN RUTA", "PENDIENTE"])
        if st.form_submit_button("Guardar Pedido", use_container_width=True):
            nuevo = pd.DataFrame([{"FECHA_REGISTRO": datetime.now().strftime("%d/%m/%Y"), "CODIGO INTERNO": cod, "CLIENTE": cli, "ESTADO": est, "SUB_ESTADO": "REGISTRADO", "NOMBRE": nom, "DISTRITO": "LIMA", "TIPO_SERVICIO": "SAME-DAY"}])
            st.session_state.df_pedidos = pd.concat([st.session_state.df_pedidos, nuevo], ignore_index=True)
            registrar_log(f"Añadió pedido {cod}")
            st.rerun()

@st.dialog("📤 Subir Data Masiva")
def modal_upload():
    file = st.file_uploader("Selecciona archivo Excel o CSV", type=["xlsx", "csv"])
    if file and st.button("Procesar y Cargar"):
        registrar_log("Subida de archivo masivo")
        st.rerun()


# LOGIN
if st.session_state.usuario_actual is None:
    st.markdown(
        """
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 28px; font-weight: 900; color: #0F382C;">🌲 ALFA CARGO EXPRESS</div>
        <div style='color: #64748B; font-size: 14px; font-weight: 600;'>🌐 Central Lima, Perú</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.2, 1.0], gap="large")

    with col_left:
        st.markdown(
            '<div style="color: #0F172A; font-size: 22px; font-weight: 700;'
            ' margin-bottom: 15px;">Módulo de Administración del Sistema</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Control de Accesos y Roles</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Gestión de Claves Directa</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Auditoría y Registros (Logs)</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Seguridad Operativa</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        img_b64 = obtener_imagen_github("alfa_warehouse.jpg")
        if img_b64:
            st.markdown(
                f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%;'
                ' max-height: 260px; object-fit: contain; border-radius: 12px;" />',
                unsafe_allow_html=True,
            )

    with col_right:
        with st.form("login_form"):
            st.markdown(
                '<h3 style="text-align: center; color: #0F382C; font-weight:800;'
                ' margin-bottom: 20px;">Bienvenido</h3>',
                unsafe_allow_html=True,
            )
            input_user = st.text_input(
                "Usuario", placeholder="Ingresa tu usuario", key="u_login"
            )
            input_pass = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingresa tu contraseña",
                key="p_login",
            )

            remember = st.checkbox("Recordar inicio de sesión", value=True)

            submit_btn = st.form_submit_button("Ingresar al Portal")

            if submit_btn:
                df_users = st.session_state.usuarios_registrados
                user_match = df_users[
                    (df_users["USUARIO"] == input_user)
                    & (df_users["PASS"] == input_pass)
                ]

                if not user_match.empty:
                    st.session_state.usuario_actual = input_user
                    st.session_state.rol_actual = user_match.iloc[0]["ROL"]

                    if (
                        "ÚLTIMA CONEXIÓN"
                        in st.session_state.usuarios_registrados.columns
                    ):
                        st.session_state.usuarios_registrados.loc[
                            st.session_state.usuarios_registrados["USUARIO"] == input_user,
                            "ÚLTIMA CONEXIÓN",
                        ] = datetime.now().strftime("%Y-%m-%d %H:%M")

                    if remember:
                        st.query_params["saved_user"] = input_user
                        st.query_params["saved_rol"] = st.session_state.rol_actual

                    registrar_log("Inicio de sesión exitoso")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "❓ ¿Necesitas ayuda con tu acceso o contraseña?",
            use_container_width=True,
        ):
            mostrar_modal_soporte()

# DASHBOARD
else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — Portal {st.session_state.rol_actual}</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 5px;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong></div>
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

    st.divider()

    # ==========================================
    # VISTA 1: PORTAL OPERARIO
    # ==========================================
    if st.session_state.rol_actual == "🛠️ Operario":
        col_tit, col_btns = st.columns([3, 2])
        
        with col_tit:
            st.markdown("<h3 style='margin:0;'>DASHBOARD > Detalle de pedidos</h3>", unsafe_allow_html=True)
        
        with col_btns:
            b1, b2, b3 = st.columns(3)
            csv = st.session_state.df_pedidos.to_csv(index=False).encode('utf-8')
            b1.download_button("📥 Descargar", data=csv, file_name="pedidos.csv")
            if b2.button("📤 Subir"): modal_upload()
            if b3.button("➕ Nuevo"): modal_add_pedido()

        st.markdown("<br>", unsafe_allow_html=True)

        # TABLA INTERACTIVA NATIVA CON FUNCIONALIDADES NATIVAS COMPLETAS
        st.dataframe(
            st.session_state.df_pedidos,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    # ==========================================
    # VISTA 2: PORTAL ADMINISTRADOR
    # ==========================================
    else:
        tab1, tab2 = st.tabs(["Usuarios y Claves", "Auditoría (Logs)"])

        with tab1:
            col_a, col_b = st.columns([1, 1.3], gap="large")

            with col_a:
                st.subheader("➕ Crear Nuevo Usuario")
                with st.form("form_crear"):
                    nu = st.text_input("Nombre de Usuario", placeholder="Ej: operador_lima")
                    np = st.text_input(
                        "Contraseña Inicial", type="password", placeholder="Clave temporal"
                    )

                    nr = st.selectbox(
                        "Rol Asignado",
                        ["🛠️ Operario", "🏢 Cliente", "🛵 Repartidor (App)"],
                    )

                    btn_crear = st.form_submit_button("Guardar Usuario")

                    if btn_crear:
                        if nu and np:
                            if (
                                nu
                                in st.session_state.usuarios_registrados["USUARIO"].values
                            ):
                                pass
                            else:
                                nueva_f = pd.DataFrame([{
                                    "USUARIO": nu,
                                    "PASS": np,
                                    "ROL": nr,
                                    "ESTADO": "Activo",
                                    "ÚLTIMA CONEXIÓN": "Nunca",
                                }])
                                st.session_state.usuarios_registrados = pd.concat(
                                    [st.session_state.usuarios_registrados, nueva_f],
                                    ignore_index=True,
                                )
                                registrar_log(f"Creó al usuario '{nu}' con rol '{nr}'")
                                st.rerun()

            with col_b:
                st.subheader("📋 Usuarios Registrados")

                cols_deseadas = ["USUARIO", "ROL", "ESTADO", "ÚLTIMA CONEXIÓN"]
                cols_existentes = [
                    c
                    for c in cols_deseadas
                    if c in st.session_state.usuarios_registrados.columns
                ]

                df_vista = st.session_state.usuarios_registrados[cols_existentes]

                filas_html = ""
                for _, fila in df_vista.iterrows():
                    color_estado = "#16A34A" if fila["ESTADO"] == "Activo" else "#DC2626"
                    ultima_conexion = fila.get("ÚLTIMA CONEXIÓN", "Nunca")
                    filas_html += f"<tr><td><b>{fila['USUARIO']}</b></td><td>{fila['ROL']}</td><td><span style='color: {color_estado}; font-weight:700;'>{fila['ESTADO']}</span></td><td>{ultima_conexion}</td></tr>"

                tabla_html = textwrap.dedent(f"""
                    <div class="tabla-contenedor">
                        <table class="tabla-usuarios">
                            <thead>
                                <tr>
                                    <th>USUARIO</th>
                                    <th>ROL</th>
                                    <th>ESTADO</th>
                                    <th>ÚLTIMA CONEXIÓN</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filas_html}
                            </tbody>
                        </table>
                    </div>
                    """).strip()

                st.markdown(tabla_html, unsafe_allow_html=True)

                st.subheader("⚙️ Gestión de Claves y Accesos")

                lista_usuarios_gestion = st.session_state.usuarios_registrados[
                    st.session_state.usuarios_registrados["USUARIO"]
                    != st.session_state.usuario_actual
                ]["USUARIO"].tolist()

                if lista_usuarios_gestion:
                    usr_gestion = st.selectbox(
                        "Selecciona un usuario para gestionar",
                        lista_usuarios_gestion,
                        key="select_gestion",
                    )

                    with st.expander("🔑 Restablecer Contraseña Directamente"):
                        nueva_pass_admin = st.text_input(
                            f"Nueva Contraseña para {usr_gestion}",
                            type="password",
                            placeholder="Escribe la nueva clave",
                            key="n_p_admin",
                        )
                        if st.button("🔄 Actualizar Clave Now", use_container_width=True):
                            if nueva_pass_admin:
                                st.session_state.usuarios_registrados.loc[
                                    st.session_state.usuarios_registrados["USUARIO"]
                                    == usr_gestion,
                                    "PASS",
                                ] = nueva_pass_admin
                                registrar_log(
                                    f"Restableció la contraseña del usuario '{usr_gestion}'"
                                )
                                st.rerun()

                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown('<div id="btn_inactivar">', unsafe_allow_html=True)
                        if st.button(
                            "🚫 Dar de Baja / Inactivar",
                            use_container_width=True,
                            key="inactivar_btn",
                        ):
                            st.session_state.usuarios_registrados.loc[
                                st.session_state.usuarios_registrados["USUARIO"]
                                == usr_gestion,
                                "ESTADO",
                            ] = "Inactivo"
                            registrar_log(f"Inactivó al usuario '{usr_gestion}'")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    with col_e2:
                        st.markdown('<div id="btn_eliminar">', unsafe_allow_html=True)
                        if st.button(
                            "❌ Eliminar Cuenta",
                            use_container_width=True,
                            key="eliminar_btn",
                        ):
                            st.session_state.usuarios_registrados = (
                                st.session_state.usuarios_registrados[
                                    st.session_state.usuarios_registrados["USUARIO"]
                                    != usr_gestion
                                ]
                            )
                            registrar_log(f"Eliminó al usuario '{usr_gestion}'")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("ℹ️ No hay otros usuarios registrados para gestionar.")

        with tab2:
            st.subheader("📜 Historial de Seguridad y Movimientos")

            df_logs = st.session_state.historial_acciones
            filas_logs = ""
            for _, fila in df_logs.iterrows():
                filas_logs += f"<tr><td>{fila['FECHA Y HORA']}</td><td><b>{fila['USUARIO']}</b></td><td>{fila['ACCIÓN']}</td></tr>"

            tabla_logs_html = textwrap.dedent(f"""
                <div class="tabla-contenedor-logs">
                    <table class="tabla-usuarios">
                        <thead>
                            <tr>
                                <th>FECHA Y HORA</th>
                                <th>USUARIO</th>
                                <th>ACCIÓN</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_logs}
                        </tbody>
                    </table>
                </div>
                """).strip()

            st.markdown(tabla_logs_html, unsafe_allow_html=True)
