import base64
from datetime import datetime
import os
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# REVISAR SESIÓN GUARDADA
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

# ESTILOS CSS - VERDE OSCURO CORPORATIVO
st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .stApp { background-color: #F4F7F6 !important; }
    .block-container { max-width: 88% !important; padding-top: 3.5rem !important; padding-bottom: 2.5rem !important; margin: 0 auto !important; }
    .header-container { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; margin-bottom: 35px; }
    .brand-logo { font-size: 32px !important; font-weight: 900; color: #0F382C; letter-spacing: -0.5px; }
    .hero-title { color: #1E293B; font-size: 24px !important; font-weight: 700; margin-bottom: 22px; letter-spacing: -0.2px; }
    .value-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 22px; }
    .value-item { color: #1E293B; font-weight: 700; font-size: 15px; display: flex; align-items: center; }
    .value-item::before { content: "▌"; color: #0F382C; font-weight: bold; margin-right: 10px; font-size: 18px; }
    .hero-image { width: 100%; height: 330px; object-fit: cover; border-radius: 12px !important; display: block; }
    [data-testid="stForm"] { background-color: #FFFFFF !important; border-radius: 20px !important; border: 1px solid #E2E8F0 !important; box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.06) !important; padding: 40px 40px !important; margin-top: 0px !important; border-top: 6px solid #0F382C !important; }
    .card-title { text-align: center; color: #0F382C; font-size: 28px; font-weight: 800; margin-bottom: 28px; }
    .stTextInput input { background-color: #FFFFFF !important; color: #0F382C !important; border: 1px solid #CBD5E1 !important; border-radius: 10px !important; padding: 12px 16px !important; font-size: 15px !important; }
    .stTextInput label { color: #1E293B !important; font-weight: 700 !important; font-size: 15px !important; margin-bottom: 4px !important; }
    div[data-testid="stFormSubmitButton"] > button { width: 100% !important; background-color: #0F382C !important; color: #FFFFFF !important; border-radius: 10px !important; border: none !important; padding: 13px 0px !important; font-size: 16px !important; font-weight: 700 !important; transition: all 0.2s ease; }
    div[data-testid="stFormSubmitButton"] > button:hover { background-color: #15803D !important; }
    .login-footer { text-align: center; color: #94A3B8; font-size: 13px; margin-top: 30px; }
    .dashboard-title { color: #0F382C !important; font-size: 26px !important; font-weight: 900 !important; margin-bottom: 2px !important; }
    .dashboard-sub { color: #475569 !important; font-size: 14px !important; font-weight: 600 !important; }
    div[data-testid="stButton"] > button { background-color: #EF4444 !important; color: #FFFFFF !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; padding: 8px 16px !important; }
    div[data-testid="stButton"] > button:hover { background-color: #DC2626 !important; }
    [data-testid="stDataFrame"] { background-color: #FFFFFF !important; border-radius: 12px !important; padding: 10px !important; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.04) !important; border: 1px solid #E2E8F0 !important; }
    /* Estilo para las pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #FFFFFF; border-radius: 8px; padding: 10px 20px; font-weight: 700; color: #0F382C; border: 1px solid #E2E8F0; }
    .stTabs [aria-selected="true"] { background-color: #0F382C !important; color: #FFFFFF !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# BASE DE DATOS EN SESIÓN
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
      {
          "USUARIO": "juan_repartidor",
          "PASS": "123",
          "ROL": "🛵 Repartidor (App)",
          "ESTADO": "Activo",
      },
      {
          "USUARIO": "cliente_global",
          "PASS": "123",
          "ROL": "🏢 Cliente",
          "ESTADO": "Activo",
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


# VISTA DE LOGIN
if st.session_state.usuario_actual is None:
  st.markdown(
      """
        <div class="header-container">
            <div class="brand-logo">🌲 ALFA CARGO <span style='color: #0F382C;'>EXPRESS</span></div>
            <div style='color: #475569; font-size: 15px; font-weight: 600;'>🌐 Central Lima, Perú</div>
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

    img_b64 = obtener_imagen_github("alfa_warehouse.jpg")
    if img_b64:
      st.markdown(
          f'<img src="data:image/jpeg;base64,{img_b64}" class="hero-image" />',
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
            ' style="color: #0F382C; font-size: 13px; font-weight: 600;'
            ' text-decoration: none;">¿Olvidaste tu contraseña?</a></div>',
            unsafe_allow_html=True,
        )

      submit_btn = st.form_submit_button(
          "Iniciar Sesión", use_container_width=True
      )

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

          registrar_log("Inicio de sesión correcto")
          st.rerun()
        else:
          st.error("❌ Credenciales incorrectas.")

      st.markdown(
          """
                <div class="login-footer">Copyright © 2026 Alfa Cargo Express. All rights reserved.</div>
            """,
          unsafe_allow_html=True,
      )

# VISTA ADMINISTRADOR (POST-LOGIN)
else:
  col_nav1, col_nav2 = st.columns([5, 1])
  with col_nav1:
    st.markdown(
        f"""
            <div class="dashboard-title">🌲 ALFA CARGO <span style='color: #0F382C;'>EXPRESS</span> — {st.session_state.rol_actual}</div>
            <div class="dashboard-sub">Usuario activo: <strong>{st.session_state.usuario_actual}</strong> | Estado: Conectado</div>
        """,
        unsafe_allow_html=True,
    )
  with col_nav2:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", key="logout_btn"):
      registrar_log("Cierre de sesión")
      st.session_state.usuario_actual = None
      st.session_state.rol_actual = None
      st.query_params.clear()
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  # ESTRUCTURA SIMPLE EN PESTAÑAS (ADMIN)
  tab_users, tab_envios, tab_kpi, tab_audit = st.tabs([
      "👥 Gestión de Usuarios",
      "📦 Control de Envíos",
      "📊 Métricas Rápidas",
      "📜 Historial de Actividad",
  ])

  # PESTAÑA 1: CREAR Y VER USUARIOS
  with tab_users:
    col_u1, col_u2 = st.columns([1, 1.5], gap="large")

    with col_u1:
      st.subheader("Crear Nuevo Usuario")
      with st.form("form_crear_usuario"):
        nuevo_u = st.text_input("Nombre de Usuario")
        nuevo_p = st.text_input("Contraseña", type="password")
        nuevo_r = st.selectbox(
            "Rol asignado",
            ["🛠️ Operario", "🏢 Cliente", "🛵 Repartidor (App)"],
        )

        btn_crear_u = st.form_submit_button("➕ Guardar Usuario")

        if btn_crear_u:
          if nuevo_u and nuevo_p:
            if (
                nuevo_u
                in st.session_state.usuarios_registrados["USUARIO"].values
            ):
              st.error("El nombre de usuario ya existe.")
            else:
              nuevo_row = pd.DataFrame([{
                  "USUARIO": nuevo_u,
                  "PASS": nuevo_p,
                  "ROL": nuevo_r,
                  "ESTADO": "Activo",
              }])
              st.session_state.usuarios_registrados = pd.concat(
                  [st.session_state.usuarios_registrados, nuevo_row],
                  ignore_index=True,
              )
              registrar_log(f"Creó al usuario '{nuevo_u}' con rol '{nuevo_r}'")
              st.success(f"✅ Usuario **{nuevo_u}** creado correctamente.")
              st.rerun()
          else:
            st.warning("Completa todos los campos.")

    with col_u2:
      st.subheader("Usuarios Registrados")
      st.dataframe(
          st.session_state.usuarios_registrados[["USUARIO", "ROL", "ESTADO"]],
          use_container_width=True,
      )

  # PESTAÑA 2: CONTROL GLOBAL DE ENVÍOS
  with tab_envios:
    st.subheader("Listado General de Envíos")
    st.dataframe(st.session_state.db_logistica, use_container_width=True)

  # PESTAÑA 3: MÉTRICAS RÁPIDAS
  with tab_kpi:
    st.subheader("Resumen del Estado Operativo")
    df_env = st.session_state.db_logistica

    total_envios = len(df_env)
    entregados = len(df_env[df_env["ESTADO"] == "DELIVERED"])
    en_ruta = len(df_env[df_env["ESTADO"] == "EN RUTA"])

    m1, m2, m3 = st.columns(3)
    m1.metric("📦 Total de Envíos", total_envios)
    m2.metric("✅ Entregados", entregados)
    m3.metric("🚚 En Ruta", en_ruta)

  # PESTAÑA 4: AUDITORÍA BÁSICA
  with tab_audit:
    st.subheader("Registro de Movimientos")
    st.dataframe(
        st.session_state.historial_acciones, use_container_width=True
    )
