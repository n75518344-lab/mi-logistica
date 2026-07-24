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

# CSS GENERAL PARA EL ESTILO APPSHEET IDÉNTICO A LA SEGUNDA IMAGEN
st.markdown(
    """
    <style>
    /* ESTILOS GENERALES Y FONDO CLARO */
    html, body, .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }

    /* OCULTAR HEADER NATIVO DE STREAMLIT PARA PONER EL NUEVO NAVBAR SUPERIOR */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* PERSONALIZACIÓN DE LA BARRA LATERAL (SIDEBAR) ESTILO APPSHEET */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 0.5rem !important;
    }
    
    .block-container { 
        max-width: 98% !important; 
        padding-top: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A; 
    }

    /* TARJETAS DE DETALLE */
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

# BASE DE DATOS DE PEDIDOS (Ampliada para mostrar scroll y vista idéntica a imagen 2)
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
            "CODIGO_INTERNO": "BLC2-5014",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "ENTREGADO",
            "SUB_ESTADO": "ENTREGA EFECTIVA",
            "NOMBRE": "JUAN CARLOS REYES HAWKINS",
            "DIRECCION": "AV. PAPARK 450",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "MIRAFLORES",
            "DOCUMENTO": "40291827",
            "TELEFONO": "922334455",
            "DESCRIPCION": "SOBRE",
            "PESO": 0.30,
            "TIPO_SERVICIO": "SAME-DAY",
            "PLACA": "ABR120",
            "EVIDENCIA": "",
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
        {
            "FECHA_REGISTRO": "2026-06-16",
            "CODIGO_INTERNO": "BLC1-48086",
            "CLIENTE": "UNIMARKET",
            "ESTADO": "ENTREGADO",
            "SUB_ESTADO": "ENTREGA EFECTIVA",
            "NOMBRE": "ELSA ROSARIO UGARTE",
            "DIRECCION": "CALLE LIBERTAD 200",
            "DEPARTAMENTO": "LIMA",
            "PROVINCIA": "LIMA",
            "DISTRITO": "MIRAFLORES",
            "DOCUMENTO": "08273645",
            "TELEFONO": "944332211",
            "DESCRIPCION": "PAQUETE",
            "PESO": 1.20,
            "TIPO_SERVICIO": "SAME-DAY",
            "PLACA": "ABR120",
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


@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
    st.markdown(
        """
        <div style="line-height: 1.6;">
            <p style="font-size: 15px; margin-bottom: 15px;">
                La asignación y restablecimiento de contraseñas es gestionada por el área de Administración.
            </p>
            <div style="font-size: 14px; margin-bottom: 8px;">💬 <b>WhatsApp Soporte:</b> +51 987 654 321</div>
            <div style="font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo:</b> soporte@alfacargo.pe</div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("Entendido", use_container_width=True):
        st.rerun()


# PANTALLA DE LOGIN
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

# APLICACIÓN PRINCIPAL CON BARRA SUPERIOR Y MENÚ LATERAL ESTILO APPSHEET EXACTO
else:
    # BARRA SUPERIOR IDÉNTICA A LA SEGUNDA IMAGEN (Navbar AppSheet)
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; padding: 8px 15px; margin-top: -30px; margin-left: -30px; margin-right: -30px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 18px; font-weight: bold; cursor: pointer;">☰</span>
                <div style="background-color: #0F382C; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 14px;">α</div>
                <span style="font-size: 16px; font-weight: 800; color: #0F172A; letter-spacing: 0.5px;">ALFA CARGO EXPRESS</span>
            </div>
            <div style="flex-grow: 1; max-width: 400px; margin: 0 20px;">
                <input type="text" placeholder="🔍 Search Detalle de pedidos" style="width: 100%; padding: 6px 12px; border: 1px solid #CBD5E1; border-radius: 4px; font-size: 13px; background-color: #F8FAFC;" disabled>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="border: 1px solid #E2E8F0; padding: 4px 8px; border-radius: 4px; font-size: 12px; background: #FFFFFF;">🔄</span>
                <span style="border: 1px solid #E2E8F0; padding: 4px 8px; border-radius: 4px; font-size: 12px; background: #FFFFFF;">⚙️</span>
                <div style="background-color: #0F382C; color: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;">O</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # Menú lateral idéntico a la segunda imagen
        menu_seleccion = st.radio(
            "Navegación",
            [
                "📊 DASHBOARD",
                "📦 PEDIDOS",
                "👤 Iniciar Sesion",
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

    # VISTA: DASHBOARD / DETALLE DE PEDIDOS (Idéntico a Imagen 2)
    if "DASHBOARD" in menu_seleccion or "PEDIDOS" in menu_seleccion:
        # Barra de ruta de vistas estilo AppSheet (Ej: DASHBOARD > Detalle de pedidos)
        col_path, col_actions = st.columns([3, 1])
        with col_path:
            st.markdown(
                "<span style='font-weight: 700; color: #0F172A;'>DASHBOARD</span>"
                " <span style='color: #64748B;'>>&nbsp; Detalle de"
                " pedidos</span>",
                unsafe_allow_html=True,
            )

        with col_actions:
            # Botones de acción rápida superiores (simulados idénticos a imagen 2)
            act_cols = st.columns(4)
            with act_cols[0]:
                st.button("📥", help="Descargar")
            with act_cols[1]:
                st.button("🔄", help="Actualizar vista")
            with act_cols[2]:
                st.button("➕ Add", help="Añadir registro")
            with act_cols[3]:
                st.button("🎛️", help="Filtros")

        st.markdown("<br>", unsafe_allow_html=True)

        # TABLA PRINCIPAL EXÁCTAMENTE IGUAL A LA SEGUNDA IMAGEN
        df_display = st.session_state.pedidos_db[
            [
                "FECHA_REGISTRO",
                "CODIGO_INTERNO",
                "CLIENTE",
                "ESTADO",
                "SUB_ESTADO",
                "NOMBRE",
                "DISTRITO",
                "TIPO_SERVICIO",
            ]
        ].copy()

        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # SECCIÓN DE GRÁFICOS INFERIORES
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.markdown("##### Avance de ruta")
            fig_pie = px.pie(
                st.session_state.pedidos_db,
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

        with g_col2:
            st.markdown("##### Cantidad de Pedidos")
            df_counts = (
                st.session_state.pedidos_db.groupby("FECHA_REGISTRO")
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

    elif "About" in menu_seleccion:
        st.markdown("### ℹ️ Acerca de Alfa Cargo Express")
        st.write(
            "Plataforma de control logístico de última milla para operaciones"
            " comerciales."
        )

    elif "Feedback" in menu_seleccion:
        st.markdown("### 💬 Buzón de Sugerencias")
        st.text_area("Escribe tus comentarios:")
        if st.button("Enviar"):
            st.success("¡Enviado con éxito!")

    elif "App Gallery" in menu_seleccion:
        st.markdown("### 🧩 Galería de Módulos")
        st.info("Módulos adicionales en desarrollo.")

    elif "Iniciar Sesion" in menu_seleccion:
        st.markdown("### 👤 Gestión de Cuenta")
        st.write(f"Usuario activo actualmente: {st.session_state.usuario_actual}")
