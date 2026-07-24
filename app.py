import base64
from datetime import datetime
import os
import textwrap
import plotly.express as px
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

# CSS GENERAL DEL SISTEMA
st.markdown(
    """
    <style>
    /* OCULTAR SCROLLBAR GLOBAL DE LA VENTANA */
    html, body, .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* OCULTAR SIDEBAR Y CABECERA DE STREAMLIT */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { 
        display: none !important; 
    }
    
    .block-container { 
        max-width: 95% !important; 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A; 
    }

    /* ESTILOS DE TABLA INTERACTIVA */
    .tabla-contenedor {
        max-height: 420px;
        overflow-y: auto;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
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
    .stTextInput input, .stDateInput input, .stSelectbox div { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
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

    /* BOTONES LOGOUT */
    #logout_btn button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #logout_btn button p { color: #991B1B !important; font-weight: 700 !important; }

    /* TARJETAS DE DETALLE */
    .card-detalle {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# DATOS EN SESIÓN - BASE DE DATOS DE PEDIDOS (Basada en tus imágenes)
if "pedidos_db" not in st.session_state:
    st.session_state.pedidos_db = pd.DataFrame([
        {
            "FECHA_REGISTRO": "2026-07-08",
            "CODIGO_INTERNO": "Tramontina",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "ENTREGADO",
            "SUB_ESTADO": "ENTREGA EFECTIVA",
            "NOMBRE": "CECILIA LOO",
            "DIRECCION": "AV. LA MAR 576",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "ATE",
            "DOCUMENTO": "TRAMONTINA",
            "TELEFONO": "999999999",
            "DESCRIPCION": "CAJAS",
            "PESO": 1.00,
            "TIPO_SERVICIO": "SAME-DAY",
            "PLACA": "ABR120",
            "EVIDENCIA": "https://raw.githubusercontent.com/streamlit/doc-tutorial-do-not-delete/main/file.png",
        },
        {
            "FECHA_REGISTRO": "2026-06-11",
            "CODIGO_INTERNO": "SIN NUMERO",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "ENTREGADO",
            "SUB_ESTADO": "ENTREGA EFECTIVA",
            "NOMBRE": "LUIS FELIPE LLOSA",
            "DIRECCION": "CALLE LOS PINOS 123",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "SAN ISIDRO",
            "DOCUMENTO": "73629102",
            "TELEFONO": "987654321",
            "DESCRIPCION": "PAQUETE PEQUEÑO",
            "PESO": 0.50,
            "TIPO_SERVICIO": "SAME-DAY",
            "PLACA": "ABR120",
            "EVIDENCIA": "https://raw.githubusercontent.com/streamlit/doc-tutorial-do-not-delete/main/file.png",
        },
        {
            "FECHA_REGISTRO": "2026-06-13",
            "CODIGO_INTERNO": "BLC1-48039",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "ENTREGADO",
            "SUB_ESTADO": "ENTREGA EFECTIVA",
            "NOMBRE": "JOHN CASAS AGUILAR",
            "DIRECCION": "AV. LARCO 890",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "MIRAFLORES",
            "DOCUMENTO": "10492817",
            "TELEFONO": "912345678",
            "DESCRIPCION": "CAJA MEDIANA",
            "PESO": 2.50,
            "TIPO_SERVICIO": "SAME-DAY",
            "PLACA": "ABR120",
            "EVIDENCIA": "https://raw.githubusercontent.com/streamlit/doc-tutorial-do-not-delete/main/file.png",
        },
        {
            "FECHA_REGISTRO": "2026-06-13",
            "CODIGO_INTERNO": "LWE2026 - 424",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "EN TRÁNSITO",
            "SUB_ESTADO": "EN RUTA",
            "NOMBRE": "MARIA EMILIA GUZMAN",
            "DIRECCION": "AV. CAMINO REAL 400",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "SANTIAGO DE SURCO",
            "DOCUMENTO": "45928103",
            "TELEFONO": "955443322",
            "DESCRIPCION": "SOBRE DOCUMENTOS",
            "PESO": 0.20,
            "TIPO_SERVICIO": "NEXT-DAY",
            "PLACA": "C8X-401",
            "EVIDENCIA": "",
        },
    ])

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


# MODAL DE SOPORTE
@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
    st.markdown(
        """
    <div style="color: #FFFFFF !important; line-height: 1.6;">
        <p style="color: #FFFFFF !important; font-size: 15px; margin-bottom: 15px;">
            Por motivos de seguridad corporativa, la asignación y restablecimiento de contraseñas es gestionada de manera directa por el área de Administración.
        </p>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">💬 <b>WhatsApp Soporte:</b> +51 987 654 321</div>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo Institucional:</b> soporte@alfacargo.pe</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Entendido", use_container_width=True):
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
            ' margin-bottom: 15px;">Módulo de Operaciones e Integración Logística</div>',
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

# DASHBOARD OPERATORIO Y ADMINISTRADOR
else:
    # BARRA SUPERIOR
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(
            f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 5px;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong> ({st.session_state.rol_actual})</div>
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

    # VISTA OPERARIO (REPLICANDO APPSHEET)
    if st.session_state.rol_actual == "🛠️ Operario":
        tab_dash, tab_detalle = st.tabs(["📊 DASHBOARD", "📦 PEDIDOS / DETALLE"])

        # DATOS FILTRADOS EN MEMORIA
        df_pedidos = st.session_state.pedidos_db

        with tab_dash:
            col_filtros, col_graf1, col_graf2 = st.columns([1, 1.2, 1.2], gap="medium")

            with col_filtros:
                st.markdown("### 🔍 FILTROS")
                f_inicio = st.date_input("FECHA_INICIAL", value=pd.to_datetime("2026-06-01"))
                f_final = st.date_input("FECHA_FINAL", value=pd.to_datetime("2026-07-31"))
                estado_opt = st.selectbox("ESTADO", ["TODOS"] + list(df_pedidos["ESTADO"].unique()))
                tipo_opt = st.selectbox("TIPO_SERVICIO", ["TODOS"] + list(df_pedidos["TIPO_SERVICIO"].unique()))

            # APLICAR FILTROS
            df_filtered = df_pedidos.copy()
            df_filtered["FECHA_REGISTRO_DT"] = pd.to_datetime(df_filtered["FECHA_REGISTRO"])
            df_filtered = df_filtered[
                (df_filtered["FECHA_REGISTRO_DT"] >= pd.to_datetime(f_inicio)) &
                (df_filtered["FECHA_REGISTRO_DT"] <= pd.to_datetime(f_final))
            ]
            if estado_opt != "TODOS":
                df_filtered = df_filtered[df_filtered["ESTADO"] == estado_opt]
            if tipo_opt != "TODOS":
                df_filtered = df_filtered[df_filtered["TIPO_SERVICIO"] == tipo_opt]

            with col_graf1:
                st.markdown("### Avance de ruta")
                if not df_filtered.empty:
                    fig_pie = px.pie(
                        df_filtered, 
                        names="ESTADO", 
                        color="ESTADO",
                        color_discrete_map={"ENTREGADO": "#1D70B8", "EN TRÁNSITO": "#F59E0B"},
                        hole=0.4
                    )
                    fig_pie.update_layout(margin=dict(t=20, b=20, l=10, r=10), height=250)
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Sin datos")

            with col_graf2:
                st.markdown("### Cantidad de Pedidos")
                if not df_filtered.empty:
                    df_counts = df_filtered.groupby("FECHA_REGISTRO").size().reset_index(name="Count")
                    fig_bar = px.bar(
                        df_counts, 
                        x="FECHA_REGISTRO", 
                        y="Count",
                        color_discrete_sequence=["#1D70B8"]
                    )
                    fig_bar.update_layout(margin=dict(t=20, b=20, l=10, r=10), height=250)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("Sin datos")

            st.divider()
            st.markdown("### Detalle de pedidos")
            st.dataframe(
                df_filtered[["FECHA_REGISTRO", "CODIGO_INTERNO", "CLIENTE", "ESTADO", "SUB_ESTADO", "NOMBRE", "DISTRITO", "TIPO_SERVICIO"]],
                use_container_width=True,
                hide_index=True
            )

        with tab_detalle:
            col_list, col_card = st.columns([1.8, 1], gap="medium")

            with col_list:
                st.markdown("### Lista de Pedidos")
                codigo_sel = st.selectbox(
                    "Selecciona un Pedido para inspeccionar ficha completa:",
                    df_pedidos["CODIGO_INTERNO"].unique()
                )

                st.dataframe(
                    df_pedidos[["FECHA_REGISTRO", "CODIGO_INTERNO", "CLIENTE", "ESTADO", "SUB_ESTADO", "NOMBRE", "DISTRITO", "TIPO_SERVICIO"]],
                    use_container_width=True,
                    hide_index=True
                )

            with col_card:
                st.markdown("### 📋 Pedidos filtro (Detalle)")
                pedido_info = df_pedidos[df_pedidos["CODIGO_INTERNO"] == codigo_sel].iloc[0]

                st.markdown(
                    f"""
                    <div class="card-detalle">
                        <p><b>NOMBRE:</b> {pedido_info['NOMBRE']}</p>
                        <p><b>DIRECCION:</b> {pedido_info['DIRECCION']}</p>
                        <p><b>DEPARTAMENTO:</b> {pedido_info['DEPARTAMENTO']}</p>
                        <p><b>PROVINCIA:</b> {pedido_info['PROVINCIA']}</p>
                        <p><b>DISTRITO:</b> {pedido_info['DISTRITO']}</p>
                        <p><b>DOCUMENTO:</b> {pedido_info['DOCUMENTO']}</p>
                        <p><b>TELEFONO:</b> {pedido_info['TELEFONO']}</p>
                        <p><b>DESCRIPCION:</b> {pedido_info['DESCRIPCION']}</p>
                        <p><b>PESO:</b> {pedido_info['PESO']} kg</p>
                        <p><b>TIPO_SERVICIO:</b> {pedido_info['TIPO_SERVICIO']}</p>
                        <p><b>PLACA:</b> {pedido_info['PLACA']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("#### 📸 EVIDENCIA_1")
                if pedido_info["EVIDENCIA"]:
                    st.image(pedido_info["EVIDENCIA"], caption="Comprobante de Entrega", width=220)
                else:
                    st.warning("Sin imagen de evidencia adjunta.")

    # MANTENER VISTA ADMIN EN CASO DE LOGUEARSE COMO ADMIN
    else:
        st.subheader("👨‍💼 Panel de Control de Administración")
        st.dataframe(st.session_state.usuarios_registrados, use_container_width=True)
