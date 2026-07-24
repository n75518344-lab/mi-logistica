import base64
from datetime import datetime
import os
import plotly.express as px
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express",
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

# CSS GENERAL PARA EL ESTILO APPSHEET
st.markdown(
    """
    <style>
    /* ESTILOS GENERALES Y FONDO */
    html, body, .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* PERSONALIZACIÓN DE LA BARRA LATERAL (SIDEBAR) ESTILO APPSHEET */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 1rem;
    }
    
    .block-container { 
        max-width: 98% !important; 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A; 
    }

    /* TARJETAS DE DETALLE LATERAL */
    .card-detalle {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* BOTONES DEL MENÚ LATERAL */
    .stButton > button {
        border-radius: 6px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# BASE DE DATOS DE PEDIDOS (Basada en tus imágenes)
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
        },
        {
            "USUARIO": "operador1",
            "PASS": "123",
            "ROL": "🛠️ Operario",
            "ESTADO": "Activo",
        },
    ])


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
        <div style="line-height: 1.6;">
            <p style="font-size: 15px; margin-bottom: 15px;">
                La asignación y restablecimiento de contraseñas es gestionada de manera directa por el área de Administración.
            </p>
            <div style="font-size: 14px; margin-bottom: 8px;">💬 <b>WhatsApp Soporte:</b> +51 987 654 321</div>
            <div style="font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo:</b> soporte@alfacargo.pe</div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Entendido", use_container_width=True):
        st.rerun()


# PANTALLA DE LOGIN (Si no ha iniciado sesión)
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
            ' margin-bottom: 15px;">Módulo de Operaciones e Integración'
            " Logística</div>",
            unsafe_allow_html=True,
        )
        img_b64 = obtener_imagen_github("alfa_warehouse.jpg")
        if img_b64:
            st.markdown(
                f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%;'
                ' max-height: 260px; object-fit: contain; border-radius: 12px;"'
                " />",
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
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")

        if st.button(
            "❓ ¿Necesitas ayuda con tu acceso o contraseña?",
            use_container_width=True,
        ):
            mostrar_modal_soporte()

# SISTEMA PRINCIPAL (CON MENÚ LATERAL ESTILO APPSHEET)
else:
    with st.sidebar:
        st.markdown(
            "### 🌲 **ALFA CARGO EXPRESS**",
            help="Plataforma Logística",
        )
        st.divider()

        # Opciones idénticas a tu menú lateral de AppSheet
        menu_seleccion = st.radio(
            "Navegación",
            [
                "📊 DASHBOARD",
                "📦 PEDIDOS",
                "👤 Iniciar Sesion / Cuenta",
                "ℹ️ About",
                "💬 Feedback",
                "🧩 App Gallery",
            ],
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown(
            f"👤 **{st.session_state.usuario_actual}**"
            f" <br><small>{st.session_state.rol_actual}</small>",
            unsafe_allow_html=True,
        )

        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.query_params.clear()
            st.rerun()

    # VISTA: DASHBOARD PRINCIPAL
    if "DASHBOARD" in menu_seleccion:
        st.markdown(
            "### 📊 DASHBOARD <span style='font-size:16px; color:#64748B;'>>&nbsp;"
            " Detalle de pedidos</span>",
            unsafe_allow_html=True,
        )

        # BARRA DE FILTROS DESPLEGABLE (Estilo acordeón superior o lateral limpio)
        with st.expander("🔍 FILTROS AVANZADOS (Desplegable)", expanded=False):
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            with f_col1:
                f_inicio = st.date_input(
                    "Fecha Inicial", value=pd.to_datetime("2026-06-01")
                )
            with f_col2:
                f_final = st.date_input(
                    "Fecha Final", value=pd.to_datetime("2026-07-31")
                )
            with f_col3:
                estado_opt = st.selectbox(
                    "Estado",
                    ["TODOS"]
                    + list(st.session_state.pedidos_db["ESTADO"].unique()),
                )
            with f_col4:
                tipo_opt = st.selectbox(
                    "Tipo de Servicio",
                    ["TODOS"]
                    + list(
                        st.session_state.pedidos_db["TIPO_SERVICIO"].unique()
                    ),
                )

        # FILTRADO DE DATOS
        df_filtered = st.session_state.pedidos_db.copy()
        df_filtered["FECHA_REGISTRO_DT"] = pd.to_datetime(
            df_filtered["FECHA_REGISTRO"]
        )
        df_filtered = df_filtered[
            (df_filtered["FECHA_REGISTRO_DT"] >= pd.to_datetime(f_inicio))
            & (df_filtered["FECHA_REGISTRO_DT"] <= pd.to_datetime(f_final))
        ]
        if estado_opt != "TODOS":
            df_filtered = df_filtered[df_filtered["ESTADO"] == estado_opt]
        if tipo_opt != "TODOS":
            df_filtered = df_filtered[
                df_filtered["TIPO_SERVICIO"] == tipo_opt
            ]

        # DISTRIBUCIÓN IDÉNTICA A LA IMAGEN 1 y 4 (Tabla grande + Gráficos abajo/derecha)
        st.markdown("#### Detalle de pedidos")
        st.dataframe(
            df_filtered[[
                "FECHA_REGISTRO",
                "CODIGO_INTERNO",
                "CLIENTE",
                "ESTADO",
                "SUB_ESTADO",
                "NOMBRE",
                "DISTRITO",
                "TIPO_SERVICIO",
            ]],
            use_container_width=True,
            hide_index=True,
        )

        # GRÁFICOS INFERIORES
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.markdown("##### Avance de ruta")
            if not df_filtered.empty:
                fig_pie = px.pie(
                    df_filtered,
                    names="ESTADO",
                    color="ESTADO",
                    color_discrete_map={
                        "ENTREGADO": "#1D70B8",
                        "EN TRÁNSITO": "#F59E0B",
                    },
                    hole=0.4,
                )
                fig_pie.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10), height=220
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Sin datos para gráfica.")

        with g_col2:
            st.markdown("##### Cantidad de Pedidos")
            if not df_filtered.empty:
                df_counts = (
                    df_filtered.groupby("FECHA_REGISTRO")
                    .size()
                    .reset_index(name="Count")
                )
                fig_bar = px.bar(
                    df_counts,
                    x="FECHA_REGISTRO",
                    y="Count",
                    color_discrete_sequence=["#1D70B8"],
                )
                fig_bar.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10), height=220
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Sin datos para gráfica.")

    # VISTA: PEDIDOS Y FICHA TÉCNICA LATERAL (Como en la Imagen 2 y 3)
    elif "PEDIDOS" in menu_seleccion:
        st.markdown(
            "### 📦 GESTIÓN DE PEDIDOS Y DETALLE TÉCNICO",
            unsafe_allow_html=True,
        )

        col_tabla, col_ficha = st.columns([1.6, 1], gap="medium")

        with col_tabla:
            st.markdown("#### Lista de Registros")
            df_pedidos = st.session_state.pedidos_db

            # Selector para ver la tarjeta técnica del pedido
            codigo_sel = st.selectbox(
                "Seleccionar Código Interno para ver Ficha:",
                df_pedidos["CODIGO_INTERNO"].unique(),
            )

            st.dataframe(
                df_pedidos[[
                    "FECHA_REGISTRO",
                    "CODIGO_INTERNO",
                    "CLIENTE",
                    "ESTADO",
                    "SUB_ESTADO",
                    "NOMBRE",
                    "DISTRITO",
                ]],
                use_container_width=True,
                hide_index=True,
            )

        with col_ficha:
            st.markdown("#### Pedidos filtro (Detalle)")
            pedido_info = df_pedidos[
                df_pedidos["CODIGO_INTERNO"] == codigo_sel
            ].iloc[0]

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
                unsafe_allow_html=True,
            )

            st.markdown("#### 📸 EVIDENCIA_1")
            if pedido_info["EVIDENCIA"]:
                st.image(
                    pedido_info["EVIDENCIA"],
                    caption="Comprobante de Entrega",
                    width=250,
                )
            else:
                st.warning("No hay evidencia fotográfica adjunta.")

    # VISTAS SECUNDARIAS DEL MENÚ
    elif "About" in menu_seleccion:
        st.markdown("### ℹ️ Acerca de Alfa Cargo Express")
        st.write(
            "Sistema de control logístico optimizado para operaciones de"
            " última milla y distribución en Lima metropolitana."
        )

    elif "Feedback" in menu_seleccion:
        st.markdown("### 💬 Buzón de Sugerencias")
        st.text_area("Escribe tus comentarios para mejoras operativas:")
        if st.button("Enviar Comentario"):
            st.success("¡Gracias! Tu feedback ha sido registrado.")

    elif "App Gallery" in menu_seleccion:
        st.markdown("### 🧩 Galería de Módulos")
        st.info(
            "Próximamente más integraciones de despacho automatizado y control"
            " de flota satelital."
        )
