import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. ESTILOS CSS - PANTALLA GENERAL Y PANEL DE CONTROL
st.markdown(
    """
    <style>
    /* Ocultar barra lateral */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Fondo general tipo iMile */
    .stApp {
        background-color: #EEF4FC !important;
    }

    /* CONTENEDOR PRINCIPAL */
    .block-container {
        max-width: 88% !important;
        padding-top: 3.5rem !important;
        padding-bottom: 2.5rem !important;
        margin: 0 auto !important;
    }

    /* ENCABEZADO SUPERIOR CON LOGO PRINCIPAL */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 35px;
    }
    
    .brand-logo {
        font-size: 32px !important;
        font-weight: 900;
        color: #0F172A;
        letter-spacing: -0.5px;
    }

    /* COLUMNA IZQUIERDA LOGIN */
    .hero-title {
        color: #1E293B;
        font-size: 24px !important;
        font-weight: 700;
        margin-bottom: 22px;
        letter-spacing: -0.2px;
    }
    
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 22px;
    }
    .value-item {
        color: #1E293B;
        font-weight: 700;
        font-size: 15px;
        display: flex;
        align-items: center;
    }
    .value-item::before {
        content: "▌";
        color: #2563EB;
        font-weight: bold;
        margin-right: 10px;
        font-size: 18px;
    }

    .hero-image {
        width: 100%;
        height: 330px;
        object-fit: cover;
        border-radius: 12px !important;
        display: block;
    }

    /* TARJETA BLANCA DE LOGIN */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.06) !important;
        padding: 50px 40px 68px 40px !important;
        margin-top: 0px !important;
    }

    .card-title {
        text-align: center;
        color: #0F172A;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 28px;
    }

    .stTextInput {
        margin-bottom: 12px !important;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    .stTextInput label {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin-bottom: 4px !important;
    }

    .stCheckbox label p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-testid="stFormSubmitButton"] {
        width: 100% !important;
        margin-top: 24px !important;
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 13px 0px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1D4ED8 !important;
    }

    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin-top: 58px;
    }

    /* ESTILOS PARA EL PANEL DE CONTROL POST-LOGIN */
    .dashboard-title {
        color: #0F172A !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        margin-bottom: 2px !important;
    }
    .dashboard-sub {
        color: #475569 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* BOTÓN CERRAR SESIÓN ELEGANTE */
    div[data-testid="stButton"] > button {
        background-color: #EF4444 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #DC2626 !important;
    }

    /* CORRECCIÓN DE LA TABLA (DATAFRAME) EN MODO CLARO */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 10px !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #E2E8F0 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. BASE DE DATOS Y ESTADOS
if "db_logistica" not in st.session_state:
  st.session_state.db_logistica = pd.DataFrame([
      {
          "ID ENVÍO": "ALFA-124",
          "CLIENTE": "María Rodríguez",
          "ORIGEN": "Surco",
          "DESTINO": "Santa Anita",
          "ESTADO": "EN RUTA",
          "CONDUCTOR": "Juan Pérez",
          "EVIDENCIA": "Ninguna",
      },
      {
          "ID ENVÍO": "ALFA-123",
          "CLIENTE": "Inversiones Globales",
          "ORIGEN": "Callao",
          "DESTINO": "Ate",
          "ESTADO": "DELIVERED",
          "CONDUCTOR": "Luis Vargas",
          "EVIDENCIA": "Código de barra verificado + Foto de fachada",
      },
  ])

if "usuarios_registrados" not in st.session_state:
  st.session_state.usuarios_registrados = {
      "admin": {"pass": "admin123", "rol": "👨‍💼 Portal Administrador"}
  }

if "usuario_actual" not in st.session_state:
  st.session_state.usuario_actual = None
if "rol_actual" not in st.session_state:
  st.session_state.rol_actual = None

# 4. PANTALLA PRINCIPAL DE LOGIN
if st.session_state.usuario_actual is None:

  st.markdown(
      """
        <div class="header-container">
            <div class="brand-logo">
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #475569; font-size: 15px; font-weight: 600;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col_left, col_right = st.columns([1.3, 1.0], gap="large")

  with col_left:
    st.markdown(
        '<div class="hero-title">Excelencia Logística y Control'
        ' Operativo</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
            <div class="value-grid">
                <div class="value-item">Tiempos Récord de Entrega</div>
                <div class="value-item">Trazabilidad en Tiempo Real</div>
                <div class="value-item">Seguridad Garantizada</div>
                <div class="value-item">Cobertura Lima y Provincias</div>
                <div class="value-item">Confirmación por Escáner</div>
                <div class="value-item">Soporte Corporativo 24/7</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # AQUÍ SE REEMPLAZA EL ENLACE DE LA IMAGEN DE PINTEREST
    # Usamos la CDN directa de Pinterest (i.pinimg.com) para que cargue la imagen
    p_image_url = (
        "https://i.pinimg.com/564x/88/11/57/881157483316153777.jpg"
    )

    st.markdown(
        f'<img src="{p_image_url}" class="hero-image" />',
        unsafe_allow_html=True,
    )

  with col_right:
    with st.form("login_form"):
      st.markdown(
          '<div class="card-title">Bienvenido</div>', unsafe_allow_html=True
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

      col_opt1, col_opt2 = st.columns([1, 1.2])
      with col_opt1:
        remember = st.checkbox("Recordar", value=True)
      with col_opt2:
        st.markdown(
            '<div style="text-align: right; padding-top: 3px;"><a href="#"'
            ' style="color: #2563EB; font-size: 13px; font-weight: 600;'
            ' text-decoration: none;">¿Olvidaste tu contraseña?</a></div>',
            unsafe_allow_html=True,
        )

      submit_btn = st.form_submit_button(
          "Iniciar Sesión", use_container_width=True
      )

      if submit_btn:
        if (
            input_user in st.session_state.usuarios_registrados
            and st.session_state.usuarios_registrados[input_user]["pass"]
            == input_pass
        ):
          st.session_state.usuario_actual = input_user
          st.session_state.rol_actual = st.session_state.usuarios_registrados[
              input_user
          ]["rol"]
          st.rerun()
        else:
          st.error("❌ Credenciales incorrectas.")

      st.markdown(
          """
                <div class="login-footer">
                    Copyright © 2026 Alfa Cargo Express. All rights reserved.
                </div>
            """,
          unsafe_allow_html=True,
      )

# 5. SESIÓN INICIADA (SISTEMA CENTRAL)
else:
  col_nav1, col_nav2 = st.columns([5, 1])
  with col_nav1:
    st.markdown(
        f"""
            <div class="dashboard-title">
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span> — {st.session_state.rol_actual}
            </div>
            <div class="dashboard-sub">
                Usuario activo: <strong>{st.session_state.usuario_actual}</strong> | Estado: Conectado
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_nav2:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", key="logout_btn"):
      st.session_state.usuario_actual = None
      st.session_state.rol_actual = None
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)
  st.dataframe(st.session_state.db_logistica, use_container_width=True)
