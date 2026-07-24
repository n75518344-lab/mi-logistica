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

# INICIALIZACIÓN DE DATOS DEL SISTEMA
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

if "paquetes_almacen" not in st.session_state:
    st.session_state.paquetes_almacen = pd.DataFrame([
        {
            "GUIA": "PKG-1001",
            "REMITENTE": "Alicorp S.A.",
            "DESTINATARIO": "Juan Pérez",
            "DESTINO": "Miraflores, Lima",
            "ESTADO": "En Almacén",
            "REPARTIDOR": "Sin asignar",
            "FECHA": datetime.now().strftime("%Y-%m-%d"),
        },
        {
            "GUIA": "PKG-1002",
            "REMITENTE": "Nexus Logistics",
            "DESTINATARIO": "Maria Gómez",
            "DESTINO": "Los Olivos, Lima",
            "ESTADO": "En Almacén",
            "REPARTIDOR": "Sin asignar",
            "FECHA": datetime.now().strftime("%Y-%m-%d"),
        },
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


# CSS GENERAL
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
        max-width: 88% !important; 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #0F172A; }

    /* CONTRASTE EN INPUTS Y SELECTS */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], .stTextInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div, .stTextInput input {
        color: #0F172A !important;
    }

    /* BARRA DE SCROLL TABLAS */
    .tabla-contenedor, .tabla-contenedor-logs {
        max-height: 280px;
        height: fit-content;
        overflow-y: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px !important;
    }
    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 14px;
        text-align: left;
    }
    .tabla-usuarios th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 10px 14px;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .tabla-usuarios td {
        padding: 8px 14px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
    }

    /* EXPANDER Y FORMULARIOS */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 12px !important; 
        border: 1px solid #E2E8F0 !important; 
        padding: 20px !important; 
        border-top: 5px solid #0F382C !important; 
    }
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important; 
        width: 100% !important;
    }

    /* BOTONES ACCIÓN GENERALES */
    #logout_btn button {
        background-color: #0F382C !important;
        color: #FFFFFF !important;
        border: 1px solid #0F382C !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# MODAL DE SOPORTE
@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
    st.markdown(
        """
    <div style="color: #FFFFFF !important;">
        <p style="color: #FFFFFF !important; font-size: 15px;">
            Por motivos de seguridad, el restablecimiento de contraseñas es gestionado por Administración.
        </p>
        <div style="color: #FFFFFF !important;">💬 <b>WhatsApp Soporte:</b> +51 987 654 321</div>
        <div style="color: #FFFFFF !important;">✉️ <b>Correo:</b> soporte@alfacargo.pe</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Entendido", use_container_width=True):
        st.rerun()


# ==========================================
# 1. LOGIN
# ==========================================
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
            ' margin-bottom: 15px;">Sistema Integrado de Gestión Logística</div>',
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
                ' margin-bottom: 20px;">Iniciar Sesión</h3>',
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
            submit_btn = st.form_submit_button("Ingresar al Sistema")

            if submit_btn:
                df_users = st.session_state.usuarios_registrados
                user_match = df_users[
                    (df_users["USUARIO"] == input_user)
                    & (df_users["PASS"] == input_pass)
                ]

                if not user_match.empty:
                    if user_match.iloc[0]["ESTADO"] == "Inactivo":
                        st.error("❌ Esta cuenta se encuentra inactiva.")
                    else:
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
                else:
                    st.error("❌ Credenciales incorrectas.")

        if st.button(
            "❓ ¿Necesitas ayuda con tu acceso o contraseña?",
            use_container_width=True,
        ):
            mostrar_modal_soporte()

# ==========================================
# 2. DASHBOARD OPERADOR
# ==========================================
elif st.session_state.rol_actual == "🛠️ Operario":
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — Módulo de Operaciones</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 10px;">Operador activo: <strong>{st.session_state.usuario_actual}</strong></div>
            """,
            unsafe_allow_html=True,
        )
    with col_nav2:
        st.markdown('<div id="logout_btn">', unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", key="logout_operario"):
            registrar_log("Cierre de sesión")
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.query_params.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    tab_op1, tab_op2 = st.tabs(["📦 Recepción y Despacho", "🚚 Consolidador de Rutas"])

    with tab_op1:
        col_reg, col_list = st.columns([1, 1.4], gap="medium")

        with col_reg:
            st.subheader("📥 Registrar Entrada de Paquete")
            with st.form("form_recepcion"):
                guia = st.text_input("Número de Guía", placeholder="Ej: PKG-1003")
                remitente = st.text_input("Remitente", placeholder="Cliente o Empresa")
                destinatario = st.text_input("Destinatario", placeholder="Nombre completo")
                destino = st.text_input("Dirección / Distrito", placeholder="Ej: Surco, Lima")
                btn_ingresar = st.form_submit_button("Registrar Paquete")

                if btn_ingresar:
                    if guia and destinatario and destino:
                        nuevo_pkg = pd.DataFrame([{
                            "GUIA": guia,
                            "REMITENTE": remitente if remitente else "Particular",
                            "DESTINATARIO": destinatario,
                            "DESTINO": destino,
                            "ESTADO": "En Almacén",
                            "REPARTIDOR": "Sin asignar",
                            "FECHA": datetime.now().strftime("%Y-%m-%d"),
                        }])
                        st.session_state.paquetes_almacen = pd.concat(
                            [st.session_state.paquetes_almacen, nuevo_pkg], ignore_index=True
                        )
                        registrar_log(f"Registró ingreso de paquete {guia}")
                        st.success(f"✅ Paquete {guia} ingresado correctamente.")
                        st.rerun()
                    else:
                        st.warning("Completa los campos requeridos (Guía, Destinatario y Destino).")

        with col_list:
            st.subheader("📋 Inventario en Almacén")
            df_pkg = st.session_state.paquetes_almacen

            # Métricas rápidas
            m1, m2 = st.columns(2)
            m1.metric("Paquetes en Almacén", len(df_pkg[df_pkg["ESTADO"] == "En Almacén"]))
            m2.metric("Paquetes en Tránsito", len(df_pkg[df_pkg["ESTADO"] == "En Tránsito"]))

            # Tabla custom
            filas_pkg = ""
            for _, f in df_pkg.iterrows():
                filas_pkg += f"<tr><td><b>{f['GUIA']}</b></td><td>{f['DESTINATARIO']}</td><td>{f['DESTINO']}</td><td><b>{f['ESTADO']}</b></td><td>{f['REPARTIDOR']}</td></tr>"

            st.markdown(
                f"""
                <div class="tabla-contenedor">
                    <table class="tabla-usuarios">
                        <thead>
                            <tr>
                                <th>GUÍA</th>
                                <th>DESTINATARIO</th>
                                <th>DESTINO</th>
                                <th>ESTADO</th>
                                <th>REPARTIDOR</th>
                            </tr>
                        </thead>
                        <tbody>{filas_pkg}</tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_op2:
        st.subheader("🚚 Asignación de Rutas y Despacho")
        col_c1, col_c2 = st.columns([1, 1.2])

        with col_c1:
            repartidores = st.session_state.usuarios_registrados[
                st.session_state.usuarios_registrados["ROL"] == "🛵 Repartidor (App)"
            ]["USUARIO"].tolist()

            paquetes_disponibles = st.session_state.paquetes_almacen[
                st.session_state.paquetes_almacen["ESTADO"] == "En Almacén"
            ]["GUIA"].tolist()

            if repartidores and paquetes_disponibles:
                rep_seleccionado = st.selectbox("Seleccionar Repartidor", repartidores)
                guias_seleccionadas = st.multiselect(
                    "Seleccionar Guías para la Ruta", paquetes_disponibles
                )

                if st.button("🚀 Asignar y Despachar Ruta", use_container_width=True):
                    if guias_seleccionadas:
                        st.session_state.paquetes_almacen.loc[
                            st.session_state.paquetes_almacen["GUIA"].isin(guias_seleccionadas),
                            ["ESTADO", "REPARTIDOR"],
                        ] = ["En Tránsito", rep_seleccionado]

                        registrar_log(
                            f"Asignó {len(guias_seleccionadas)} paquetes al repartidor"
                            f" {rep_seleccionado}"
                        )
                        st.success(
                            f"✅ Ruta despachada con {len(guias_seleccionadas)} paquetes a"
                            f" {rep_seleccionado}."
                        )
                        st.rerun()
                    else:
                        st.warning("Selecciona al menos una guía.")
            elif not repartidores:
                st.info("No hay repartidores registrados en el sistema.")
            else:
                st.info("No hay paquetes pendientes por asignar en almacén.")

        with col_c2:
            st.subheader("📑 Hoja de Ruta Activa")
            df_transito = st.session_state.paquetes_almacen[
                st.session_state.paquetes_almacen["ESTADO"] == "En Tránsito"
            ]
            if not df_transito.empty:
                st.dataframe(
                    df_transito[["GUIA", "DESTINATARIO", "DESTINO", "REPARTIDOR"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.write("No hay guías en tránsito actualmente.")

# ==========================================
# 3. DASHBOARD ADMINISTRADOR
# ==========================================
else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — Portal Administrador</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 10px;">Admin activo: <strong>{st.session_state.usuario_actual}</strong></div>
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
                        if nu in st.session_state.usuarios_registrados["USUARIO"].values:
                            st.error("El nombre de usuario ya existe.")
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
                            st.success(f"✅ Usuario {nu} creado con éxito")
                            st.rerun()
                    else:
                        st.warning("Completa los campos obligatorios.")

        with col_b:
            st.subheader("📋 Usuarios Registrados")
            df_vista = st.session_state.usuarios_registrados[
                ["USUARIO", "ROL", "ESTADO", "ÚLTIMA CONEXIÓN"]
            ]

            filas_html = ""
            for _, fila in df_vista.iterrows():
                color_estado = "#16A34A" if fila["ESTADO"] == "Activo" else "#DC2626"
                filas_html += f"<tr><td><b>{fila['USUARIO']}</b></td><td>{fila['ROL']}</td><td><span style='color: {color_estado}; font-weight:700;'>{fila['ESTADO']}</span></td><td>{fila['ÚLTIMA CONEXIÓN']}</td></tr>"

            st.markdown(
                f"""
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
                        <tbody>{filas_html}</tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.subheader("⚙️ Gestión de Claves y Accesos")
            lista_usuarios = st.session_state.usuarios_registrados[
                st.session_state.usuarios_registrados["USUARIO"] != st.session_state.usuario_actual
            ]["USUARIO"].tolist()

            if lista_usuarios:
                usr_gestion = st.selectbox("Selecciona usuario a gestionar", lista_usuarios)

                with st.expander("🔑 Restablecer Contraseña Directamente"):
                    nueva_pass = st.text_input("Nueva Contraseña", type="password", key="np_adm")
                    if st.button("🔄 Actualizar Clave", use_container_width=True):
                        if nueva_pass:
                            st.session_state.usuarios_registrados.loc[
                                st.session_state.usuarios_registrados["USUARIO"] == usr_gestion, "PASS"
                            ] = nueva_pass
                            registrar_log(f"Restableció la contraseña de '{usr_gestion}'")
                            st.success(f"Contraseña de '{usr_gestion}' actualizada.")
                            st.rerun()

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    if st.button("🚫 Dar de Baja", use_container_width=True):
                        st.session_state.usuarios_registrados.loc[
                            st.session_state.usuarios_registrados["USUARIO"] == usr_gestion, "ESTADO"
                        ] = "Inactivo"
                        registrar_log(f"Inactivó al usuario '{usr_gestion}'")
                        st.rerun()
                with col_e2:
                    if st.button("❌ Eliminar Cuenta", use_container_width=True):
                        st.session_state.usuarios_registrados = st.session_state.usuarios_registrados[
                            st.session_state.usuarios_registrados["USUARIO"] != usr_gestion
                        ]
                        registrar_log(f"Eliminó al usuario '{usr_gestion}'")
                        st.rerun()

    with tab2:
        st.subheader("📜 Historial de Seguridad y Movimientos")
        df_logs = st.session_state.historial_acciones
        filas_logs = ""
        for _, fila in df_logs.iterrows():
            filas_logs += f"<tr><td>{fila['FECHA Y HORA']}</td><td><b>{fila['USUARIO']}</b></td><td>{fila['ACCIÓN']}</td></tr>"

        st.markdown(
            f"""
            <div class="tabla-contenedor-logs">
                <table class="tabla-usuarios">
                    <thead>
                        <tr>
                            <th>FECHA Y HORA</th>
                            <th>USUARIO</th>
                            <th>ACCIÓN</th>
                        </tr>
                    </thead>
                    <tbody>{filas_logs}</tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )
