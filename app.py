import base64
from datetime import datetime, date
import os
import textwrap
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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

# CSS GENERAL DEL SISTEMA Y CORRECCIÓN DE BORDES Y BOTONES
st.markdown(
    """
    <style>
    /* Estructura general */
    html, body, .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important;
        border-right: 1px solid #CBD5E1 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    [data-testid="stSidebar"] .stTextInput, 
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: -10px !important;
    }

    /* =========================================================
       ESTILOS PARA INPUTS, SELECTS Y BORDES VERDE OSCURO
       ========================================================= */
       
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #0F382C !important;
        border-width: 1.5px !important;
    }
    
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"] > div:hover {
        border-color: #0F382C !important;
        box-shadow: 0 0 0 1px #0F382C !important;
    }
    
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input {
        color: #0F172A !important;
        fill: #0F172A !important;
    }
    
    span[data-baseweb="tag"] {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
    }
    span[data-baseweb="tag"] * {
        color: #0F172A !important;
    }
    
    div[data-baseweb="popover"] > div, 
    ul[role="listbox"],
    div[data-baseweb="popover"] ul {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    
    li[role="option"] span,
    li[role="option"] div {
        color: #0F172A !important;
    }
    
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #0F382C !important;
    }

    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
        padding: 8px 10px !important;
    }

    /* ========================================================= */

    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stElementToolbar"] { display: none !important; }
    
    .block-container { 
        max-width: 96% !important; 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #0F172A; }

    /* Estilo general para botones por defecto (Fondo Blanco, Borde Verde Oscuro) */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button { 
        background-color: #FFFFFF !important;  
        border: 1.5px solid #0F382C !important;
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
        color: #0F382C !important;    
        fill: #0F382C !important;     
    }

    /* Hover de los botones */
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover { 
        background-color: #0F382C !important; 
        border-color: #0F382C !important; 
    }

    div[data-testid="stButton"] > button:hover div,
    div[data-testid="stButton"] > button:hover span,
    div[data-testid="stButton"] > button:hover p,
    div[data-testid="stButton"] > button:hover label {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* ESTILO ESPECÍFICO PARA LOS 3 BOTONES SUPERIORES (Descargar, Subir, Añadir) */
    .contenedor-btn-custom button {
        background-color: #FFFFFF !important;
        border: 1.5px solid #0F382C !important;
        border-radius: 8px !important;
    }
    .contenedor-btn-custom button div,
    .contenedor-btn-custom button span,
    .contenedor-btn-custom button p {
        color: #0F382C !important;
        font-weight: 700 !important;
    }
    .contenedor-btn-custom button:hover {
        background-color: #0F382C !important;
    }
    .contenedor-btn-custom button:hover div,
    .contenedor-btn-custom button:hover span,
    .contenedor-btn-custom button:hover p {
        color: #FFFFFF !important;
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
        margin-top: 10px !important;
    }

    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
    }
    .tabla-usuarios th {
        background-color: #0F382C;
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
        background-color: #0F382C !important;
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
        border-top: 6px solid #0F382C !important; 
    }

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

    #logout_btn button {
        background-color: #FFFFFF !important;
        border: 1.5px solid #0F382C !important;
        border-radius: 8px !important;
    }
    #logout_btn button p, #logout_btn button span { color: #0F382C !important; font-weight: 700 !important; }
    #logout_btn button:hover { background-color: #0F382C !important; }
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
        color: #0F382C !important; 
        font-weight: 700 !important; 
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
        {"FECHA_REGISTRO": "24/07/2026", "CODIGO INTERNO": "BLC1-48039", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "CECILIA LOO", "DISTRITO": "ATE", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "23/07/2026", "CODIGO INTERNO": "SIN NUMERO", "CLIENTE": "ALICORP", "ESTADO": "EN RUTA", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "LUIS LLOSA", "DISTRITO": "SAN ISIDRO", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "22/07/2026", "CODIGO INTERNO": "BLC2-5014", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "JUAN REYES", "DISTRITO": "MIRAFLORES", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "21/07/2026", "CODIGO INTERNO": "BLC2-5015", "CLIENTE": "GLORIA", "ESTADO": "PENDIENTE", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "MARIA PEREZ", "DISTRITO": "LA MOLINA", "TIPO_SERVICIO": "NEXT-DAY"}
    ])

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
            input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
            input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
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
        if st.button("❓ ¿Necesitas ayuda con tu acceso o contraseña?", use_container_width=True):
            mostrar_modal_soporte()

else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — Portal {st.session_state.rol_actual}</div>
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

    st.markdown("<hr style='margin: 8px 0px 12px 0px; border-color: #CBD5E1;'>", unsafe_allow_html=True)

    # ==========================================
    # VISTA 1: PORTAL OPERARIO
    # ==========================================
    if st.session_state.rol_actual == "🛠️ Operario":
        csv = st.session_state.df_pedidos.to_csv(index=False).encode('utf-8')
        
        col_tit, col_b1, col_b2, col_b3 = st.columns([4.2, 0.6, 0.6, 0.6], vertical_alignment="center")
        
        with col_tit:
            st.markdown("<h3 style='margin:0; padding:0; line-height: 1.0;'>Gestión de Envíos</h3>", unsafe_allow_html=True)
        with col_b1:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            st.download_button("📥", data=csv, file_name="pedidos.csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b2:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("📤", use_container_width=True): modal_upload()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b3:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("➕", use_container_width=True): modal_add_pedido()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)

        # ------------------------------------------
        # FILTROS EN EL SIDEBAR
        # ------------------------------------------
        with st.sidebar:
            st.markdown("<h3 style='color: #0F382C; margin-bottom: 0px;'>🔍 Panel de Filtros</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 12px; color: #64748B; margin-bottom: 4px;'>Filtra los registros de envíos de manera rápida.</p>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 0px 0px 6px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:13px; color:#0F382C; margin-bottom:0px;'>📅 Rango de Fechas (DD/MM/YYYY):</p>", unsafe_allow_html=True)
            txt_fecha_inicio = st.text_input("Fecha Inicial", value="", placeholder="DD/MM/YYYY", key="f_ini")
            txt_fecha_fin = st.text_input("Fecha Final", value="", placeholder="DD/MM/YYYY", key="f_fin")

            components.html("""
                <script>
                const doc = window.parent.document;
                function aplicarMascaraLimpia(input) {
                    if (!input.dataset.masked) {
                        input.dataset.masked = "true";
                        input.setAttribute("maxlength", "10");
                        
                        input.addEventListener("input", function(e) {
                            let val = this.value.replace(/\\D/g, "");
                            if (val.length > 8) val = val.slice(0, 8);
                            
                            let res = "";
                            if (val.length > 0) res += val.substring(0, 2);
                            if (val.length >= 3) res += "/" + val.substring(2, 4);
                            if (val.length >= 5) res += "/" + val.substring(4, 8);

                            if (this.value !== res) {
                                this.value = res;
                                this.dispatchEvent(new Event('input', { bubbles: true }));
                            }
                        });
                    }
                }
                function observarInputs() {
                    doc.querySelectorAll('input').forEach(input => {
                        if (input.getAttribute('placeholder') === 'DD/MM/YYYY') {
                            aplicarMascaraLimpia(input);
                        }
                    });
                }
                setInterval(observarInputs, 300);
                </script>
            """, height=0)

            st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:13px; color:#0F382C; margin-bottom:0px;'>📌 Selección Múltiple:</p>", unsafe_allow_html=True)
            
            clientes_unicos = sorted(st.session_state.df_pedidos["CLIENTE"].astype(str).unique().tolist())
            filtro_cliente = st.multiselect("Cliente", options=clientes_unicos, placeholder="Todos")

            distritos_unicos = sorted(st.session_state.df_pedidos["DISTRITO"].astype(str).unique().tolist())
            filtro_distrito = st.multiselect("Distrito", options=distritos_unicos, placeholder="Todos")

            servicios_unicos = sorted(st.session_state.df_pedidos["TIPO_SERVICIO"].astype(str).unique().tolist())
            filtro_servicio = st.multiselect("Tipo de Servicio", options=servicios_unicos, placeholder="Todos")

            estados_unicos = sorted(st.session_state.df_pedidos["ESTADO"].astype(str).unique().tolist())
            filtro_estado = st.multiselect("Estado", options=estados_unicos, placeholder="Todos")

            sub_estados_unicos = sorted(st.session_state.df_pedidos["SUB_ESTADO"].astype(str).unique().tolist())
            filtro_sub_estado = st.multiselect("Sub Estado", options=sub_estados_unicos, placeholder="Todos")

            st.markdown("<hr style='margin: 6px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:13px; color:#0F382C; margin-bottom:0px;'>🔍 Búsqueda por Texto:</p>", unsafe_allow_html=True)
            filtro_codigo_txt = st.text_input("Código Interno", placeholder="Ej: BLC1-480...", key="b_cod")
            filtro_nombre_txt = st.text_input("Nombre Destinatario", placeholder="Ej: Cecilia Loo...", key="b_nom")

        # APLICAR FILTROS
        df_filtrado = st.session_state.df_pedidos.copy()

        if "FECHA_REGISTRO" in df_filtrado.columns:
            df_filtrado["_fecha_temp"] = pd.to_datetime(df_filtrado["FECHA_REGISTRO"], format="%d/%m/%Y", errors="coerce")
            
            f_ini_parsed = None
            f_fin_parsed = None

            if txt_fecha_inicio.strip():
                try:
                    f_ini_parsed = datetime.strptime(txt_fecha_inicio.strip(), "%d/%m/%Y").date()
                except ValueError:
                    pass

            if txt_fecha_fin.strip():
                try:
                    f_fin_parsed = datetime.strptime(txt_fecha_fin.strip(), "%d/%m/%Y").date()
                except ValueError:
                    pass

            if f_ini_parsed and f_fin_parsed:
                df_filtrado = df_filtrado[(df_filtrado["_fecha_temp"].dt.date >= f_ini_parsed) & (df_filtrado["_fecha_temp"].dt.date <= f_fin_parsed)]
            elif f_ini_parsed and not f_fin_parsed:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date == f_ini_parsed]
            elif not f_ini_parsed and f_fin_parsed:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date <= f_fin_parsed]

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

        columnas_pedidos = df_filtrado.columns.tolist()
        headers_html = "".join([f"<th>{col}</th>" for col in columnas_pedidos])

        filas_pedidos_html = ""
        for _, fila in df_filtrado.iterrows():
            filas_pedidos_html += "<tr>"
            for col in columnas_pedidos:
                filas_pedidos_html += f"<td>{fila[col]}</td>"
            filas_pedidos_html += "</tr>"

        tabla_pedidos_html = textwrap.dedent(f"""
            <div class="tabla-contenedor-logs" style="max-height: 540px; margin-top: 4px !important;">
                <table class="tabla-usuarios">
                    <thead>
                        <tr>
                            {headers_html}
                        </tr>
                    </thead>
                    <tbody>
                        {filas_pedidos_html if not df_filtrado.empty else "<tr><td colspan='100%' style='text-align:center;'>No se encontraron registros en este filtro</td></tr>"}
                    </tbody>
                </table>
            </div>
            """).strip()

        st.markdown(tabla_pedidos_html, unsafe_allow_html=True)

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
                    np = st.text_input("Contraseña Inicial", type="password", placeholder="Clave temporal")
                    nr = st.selectbox("Rol Asignado", ["🛠️ Operario", "🏢 Cliente", "🛵 Repartidor (App)"])

                    btn_crear = st.form_submit_button("Guardar Usuario")

                    if btn_crear:
                        if nu and np:
                            if nu not in st.session_state.usuarios_registrados["USUARIO"].values:
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
                cols_existentes = [c for c in cols_deseadas if c in st.session_state.usuarios_registrados.columns]
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
                    st.session_state.usuarios_registrados["USUARIO"] != st.session_state.usuario_actual
                ]["USUARIO"].tolist()

                if lista_usuarios_gestion:
                    usr_gestion = st.selectbox("Selecciona un usuario para gestionar", lista_usuarios_gestion, key="select_gestion")

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
                                    st.session_state.usuarios_registrados["USUARIO"] == usr_gestion,
                                    "PASS",
                                ] = nueva_pass_admin
                                registrar_log(f"Restableció la contraseña del usuario '{usr_gestion}'")
                                st.rerun()

                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.markdown('<div id="btn_inactivar">', unsafe_allow_html=True)
                        if st.button("🚫 Dar de Baja / Inactivar", use_container_width=True, key="inactivar_btn"):
                            st.session_state.usuarios_registrados.loc[
                                st.session_state.usuarios_registrados["USUARIO"] == usr_gestion,
                                "ESTADO",
                            ] = "Inactivo"
                            registrar_log(f"Inactivó al usuario '{usr_gestion}'")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    with col_e2:
                        st.markdown('<div id="btn_eliminar">', unsafe_allow_html=True)
                        if st.button("❌ Eliminar Cuenta", use_container_width=True, key="eliminar_btn"):
                            st.session_state.usuarios_registrados = (
                                st.session_state.usuarios_registrados[
                                    st.session_state.usuarios_registrados["USUARIO"] != usr_gestion
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
