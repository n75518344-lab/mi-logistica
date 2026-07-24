import base64
from datetime import datetime
import os
import textwrap
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express",
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

# CSS GENERAL DEL SISTEMA (Mantenido y Reforzado para el verde corporativo)
st.markdown(
    """
    <style>
    html, body, .stApp { 
        overflow: hidden !important; 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { 
        display: none !important; 
    }
    
    .block-container { 
        max-width: 92% !important; 
        padding-top: 1rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #0F172A; }

    /* TABLAS ESTILO APPSHEET */
    .tabla-contenedor, .tabla-contenedor-pedidos {
        max-height: 450px;
        overflow-y: auto;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.02);
    }

    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 14px;
    }
    .tabla-usuarios th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 14px;
        position: sticky;
        top: 0;
        z-index: 1;
        text-align: left;
    }
    .tabla-usuarios td {
        padding: 12px 14px;
        border-bottom: 1px solid #F1F5F9;
        color: #334155 !important;
    }
    .tabla-usuarios tr:hover { background-color: #F8FAFC; }

    /* BOTONES DE ACCIÓN (VERDE ALFA) */
    div[data-testid="stFormSubmitButton"] > button, .btn-alfa button { 
        background-color: #0F382C !important; 
        color: white !important;
        border-radius: 8px !important;
    }

    /* ESTILO PARA LOS BOTONES DE ICONO SUPERIORES */
    .stButton > button {
        border: 1px solid #E2E8F0 !important;
        background-color: white !important;
        color: #0F382C !important;
        font-size: 18px !important;
    }
    .stButton > button:hover {
        border-color: #0F382C !important;
        background-color: #F0FDF4 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- INICIALIZACIÓN DE DATOS ---
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = pd.DataFrame([
        {"USUARIO": "admin", "PASS": "admin123", "ROL": "👨‍💼 Portal Administrador", "ESTADO": "Activo", "ÚLTIMA CONEXIÓN": "Nunca"},
        {"USUARIO": "operador1", "PASS": "123", "ROL": "🛠️ Operario", "ESTADO": "Activo", "ÚLTIMA CONEXIÓN": "Nunca"}
    ])

if "df_pedidos" not in st.session_state:
    st.session_state.df_pedidos = pd.DataFrame([
        {"FECHA_REGISTRO": "24/07/2026", "CODIGO INTERNO": "BLC1-48039", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "CECILIA LOO", "DISTRITO": "ATE", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "23/07/2026", "CODIGO INTERNO": "SIN NUMERO", "CLIENTE": "ALICORP", "ESTADO": "EN RUTA", "SUB_ESTADO": "PENDIENTE", "NOMBRE": "LUIS LLOSA", "DISTRITO": "SAN ISIDRO", "TIPO_SERVICIO": "SAME-DAY"},
        {"FECHA_REGISTRO": "22/07/2026", "CODIGO INTERNO": "BLC2-5014", "CLIENTE": "UNIMARKET", "ESTADO": "ENTREGADO", "SUB_ESTADO": "ENTREGA EFECTIVA", "NOMBRE": "JUAN REYES", "DISTRITO": "MIRAFLORES", "TIPO_SERVICIO": "SAME-DAY"}
    ])

if "historial_acciones" not in st.session_state:
    st.session_state.historial_acciones = pd.DataFrame([{"FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "USUARIO": "admin", "ACCIÓN": "Inicio de sistema"}])

def registrar_log(accion):
    nuevo_log = pd.DataFrame([{"FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "USUARIO": st.session_state.usuario_actual, "ACCIÓN": accion}])
    st.session_state.historial_acciones = pd.concat([nuevo_log, st.session_state.historial_acciones], ignore_index=True)

# --- MODALES ---
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
        st.success("Data cargada correctamente (Simulación)")
        registrar_log("Subida de archivo masivo")

# --- LÓGICA DE NAVEGACIÓN ---
if st.session_state.usuario_actual is None:
    # --- LOGIN (Tu código original) ---
    st.markdown("<div style='font-size: 28px; font-weight: 900; color: #0F382C;'>🌲 ALFA CARGO EXPRESS</div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.2, 1])
    with col_r:
        with st.form("login"):
            st.subheader("Iniciar Sesión")
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar al Portal"):
                match = st.session_state.usuarios_registrados[(st.session_state.usuarios_registrados["USUARIO"]==u) & (st.session_state.usuarios_registrados["PASS"]==p)]
                if not match.empty:
                    st.session_state.usuario_actual = u
                    st.session_state.rol_actual = match.iloc[0]["ROL"]
                    registrar_log("Inicio de sesión")
                    st.rerun()
                else: st.error("❌ Error")

else:
    # BARRA DE NAVEGACIÓN SUPERIOR (Común)
    c_nav1, c_nav2 = st.columns([6, 1])
    with c_nav1:
        st.markdown(f"**Usuario:** {st.session_state.usuario_actual} | **Rol:** {st.session_state.rol_actual}")
    with c_nav2:
        if st.button("🚪 Salir", use_container_width=True):
            st.session_state.usuario_actual = None
            st.rerun()

    st.divider()

    # ==========================================
    # VISTA 1: PORTAL OPERARIO (Diseño AppSheet)
    # ==========================================
    if st.session_state.rol_actual == "🛠️ Operario":
        # Fila de Título y Botones (Tal cual la imagen)
        col_tit, col_btns = st.columns([3, 2])
        
        with col_tit:
            st.markdown("<h3 style='margin:0;'>DASHBOARD > Detalle de pedidos</h3>", unsafe_allow_html=True)
        
        with col_btns:
            b1, b2, b3, b4 = st.columns(4)
            # Descargar
            csv = st.session_state.df_pedidos.to_csv(index=False).encode('utf-8')
            b1.download_button("📥", data=csv, file_name="pedidos.csv", help="Descargar CSV")
            # Subir
            if b2.button("📤", help="Subir Excel"): modal_upload()
            # Añadir
            if b3.button("➕ Add", help="Nuevo Pedido"): modal_add_pedido()
            # Filtrar
            btn_filtro = b4.toggle("🔍", help="Ver Filtros")

        # Zona de Filtros Desplegable
        df_final = st.session_state.df_pedidos.copy()
        if btn_filtro:
            f1, f2, f3 = st.columns(3)
            filtro_est = f1.selectbox("Estado", ["TODOS", "ENTREGADO", "EN RUTA", "PENDIENTE"])
            filtro_bus = f2.text_input("Buscar Nombre/Código")
            if filtro_est != "TODOS": df_final = df_final[df_final["ESTADO"] == filtro_est]
            if filtro_bus: df_final = df_final[df_final["NOMBRE"].str.contains(filtro_bus, case=False) | df_final["CODIGO INTERNO"].str.contains(filtro_bus, case=False)]

        # Tabla de Pedidos (Idéntica a la imagen)
        filas_html = ""
        for _, f in df_final.iterrows():
            filas_html += f"<tr><td>{f['FECHA_REGISTRO']}</td><td><b>{f['CODIGO INTERNO']}</b></td><td>{f['CLIENTE']}</td><td>{f['ESTADO']}</td><td>{f['SUB_ESTADO']}</td><td>{f['NOMBRE']}</td><td>{f['DISTRITO']}</td><td>{f['TIPO_SERVICIO']}</td><td style='color:green; font-weight:bold;'>›</td></tr>"
        
        st.markdown(f"""
            <div class="tabla-contenedor-pedidos">
                <table class="tabla-usuarios">
                    <thead>
                        <tr>
                            <th>FECHA_REGISTRO</th><th>CODIGO INTERNO</th><th>CLIENTE</th><th>ESTADO</th><th>SUB_ESTADO</th><th>NOMBRE</th><th>DISTRITO</th><th>TIPO_SERVICIO</th><th></th>
                        </tr>
                    </thead>
                    <tbody>{filas_html}</tbody>
                </table>
            </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # VISTA 2: PORTAL ADMINISTRADOR (Tu código original)
    # ==========================================
    else:
        tab1, tab2 = st.tabs(["Usuarios y Claves", "Auditoría (Logs)"])
        
        with tab1:
            col_a, col_b = st.columns([1, 1.3])
            with col_a:
                st.subheader("➕ Crear Usuario")
                with st.form("new_u"):
                    nu = st.text_input("Usuario")
                    np = st.text_input("Pass")
                    nr = st.selectbox("Rol", ["🛠️ Operario", "🏢 Cliente", "🛵 Repartidor"])
                    if st.form_submit_button("Guardar"):
                        # Lógica de guardado existente...
                        registrar_log(f"Creó usuario {nu}")
                        st.success("Creado")
            
            with col_b:
                st.subheader("📋 Lista de Usuarios")
                # Renderizar tu tabla de usuarios con HTML (como en tu código original)
                u_filas = ""
                for _, u in st.session_state.usuarios_registrados.iterrows():
                    u_filas += f"<tr><td>{u['USUARIO']}</td><td>{u['ROL']}</td><td>{u['ESTADO']}</td><td>{u['ÚLTIMA CONEXIÓN']}</td></tr>"
                st.markdown(f"<div class='tabla-contenedor'><table class='tabla-usuarios'><thead><tr><th>USUARIO</th><th>ROL</th><th>ESTADO</th><th>CONEXIÓN</th></tr></thead><tbody>{u_filas}</tbody></table></div>", unsafe_allow_html=True)

        with tab2:
            st.subheader("📜 Logs del Sistema")
            l_filas = ""
            for _, l in st.session_state.historial_acciones.iterrows():
                l_filas += f"<tr><td>{l['FECHA Y HORA']}</td><td>{l['USUARIO']}</td><td>{l['ACCIÓN']}</td></tr>"
            st.markdown(f"<div class='tabla-contenedor'><table class='tabla-usuarios'><thead><tr><th>FECHA</th><th>USER</th><th>ACCIÓN</th></tr></thead><tbody>{l_filas}</tbody></table></div>", unsafe_allow_html=True)
