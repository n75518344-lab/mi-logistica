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

# CSS ULTRA ESTRICTO - REESCRITURA DE BASEWEB Y WIDGETS
st.markdown(
    """
    <style>
    /* OCULTAR ELEMENTOS NATIVOS */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { display: none !important; }
    
    /* FONDO DE PÁGINA */
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    .block-container { max-width: 90% !important; padding-top: 2rem !important; padding-bottom: 2rem !important; }
    
    /* RESET DE TEXTOS */
    h1, h2, h3, h4, h5, h6, p, label, span, div, small {
        color: #0F172A !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* HEADER Y LANDING */
    .header-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
    .brand-logo { font-size: 30px !important; font-weight: 900; color: #0F382C !important; }
    .hero-title { color: #0F172A !important; font-size: 22px !important; font-weight: 700; margin-bottom: 20px; }
    .value-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
    .value-item { color: #334155 !important; font-weight: 600; font-size: 14px; display: flex; align-items: center; }
    .value-item::before { content: "▌"; color: #0F382C !important; margin-right: 8px; font-size: 16px; }
    .hero-image { width: 100%; height: 320px; object-fit: cover; border-radius: 12px !important; }

    /* FORMULARIO CONTENEDOR */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 16px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 32px !important; 
        border-top: 5px solid #0F382C !important; 
    }
    .card-title { text-align: center; color: #0F382C !important; font-size: 26px; font-weight: 800; margin-bottom: 20px; }

    /* FIX INPUTS Y PLACEHOLDERS */
    .stTextInput input, .stTextInput input:focus { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
    }
    .stTextInput input::placeholder { color: #94A3B8 !important; opacity: 1 !important; }

    /* FIX SELECTBOX (DESPLEGABLE / MENU) */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"]:hover {
        background-color: #F1F5F9 !important;
    }

    /* FIX ICONO DE OJITO EN CONTRASEÑA Y FLECHA DE SELECTBOX */
    button[aria-label="Show password"], button[aria-label="Hide password"], [data-baseweb="icon"] {
        background-color: transparent !important;
        color: #0F382C !important;
    }
    svg { fill: #0F382C !important; }

    /* BOTONES PRIMARIOS */
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        border-radius: 8px !important; 
        border: none !important; 
        padding: 10px 0px !important; 
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] > button p, 
    div[data-testid="stFormSubmitButton"] > button span { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
    }
    div[data-testid="stFormSubmitButton"] > button:hover { background-color: #15803D !important; }

    /* BOTÓN CERRAR SESIÓN */
    div[data-testid="stButton"] > button { 
        background-color: #DC2626 !important; 
        border: none !important; 
        border-radius: 8px !important; 
    }
    div[data-testid="stButton"] > button p, 
    div[data-testid="stButton"] > button span { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }

    /* FIX PESTAÑAS (ST.TABS) */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; gap: 6px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #E2E8F0 !important; 
        border-radius: 8px 8px 0px 0px !important; 
        padding: 8px 16px !important; 
        border: none !important; 
    }
    .stTabs [data-baseweb="tab"] p { color: #334155 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] { background-color: #0F382C !important; }
    .stTabs [aria-selected="true"] p { color: #FFFFFF !important; font-weight: 800 !important; }

    /* TABLAS ESTÁTICAS Y NATIVAS */
    .stTable, [data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stTable td, .stTable th { color: #0F172A !important; background-color: #FFFFFF !important; }
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
            <div class="brand-logo">🌲 ALFA CARGO EXPRESS</div>
            <div style='color: #64748B; font-size: 14px; font-weight: 600;'>🌐 Central Lima, Perú</div>
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

# VISTA DASHBOARD (POST-LOGIN)
else:
  col_nav1, col_nav2 = st.columns([5, 1])
  with col_nav1:
    st.markdown(
        f"""
            <div style="font-size: 24px; font-weight: 800; color: #0F382C;">🌲 ALFA CARGO EXPRESS — {st.session_state.rol_actual}</div>
            <div style="font-size: 14px; color: #475569; font-weight: 600;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong></div>
        """,
        unsafe_allow_html=True,
    )
  with col_nav2:
    if st.button("🚪 Cerrar Sesión", key="logout_btn"):
      registrar_log("Cierre de sesión")
      st.session_state.usuario_actual = None
      st.session_state.rol_actual = None
      st.query_params.clear()
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  tab_users, tab_envios, tab_kpi, tab_audit = st.tabs([
      "👥 Gestión de Usuarios",
      "📦 Control de Envíos",
      "📊 Métricas Rápidas",
      "📜 Historial de Actividad",
  ])

  # TAB 1: USUARIOS
  with tab_users:
    col_u1, col_u2 = st.columns([1, 1.4], gap="large")

    with col_u1:
      st.subheader("Crear Nuevo Usuario")
      with st.form("form_crear_usuario"):
        nuevo_u = st.text_input(
            "Nombre de Usuario", placeholder="Ej: operario_lima"
        )
        nuevo_p = st.text_input(
            "Contraseña", type="password", placeholder="Escribe la clave"
        )
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
      # Usamos st.table para garantizar 0 errores de renderizado oscuro
      st.table(
          st.session_state.usuarios_registrados[["USUARIO", "ROL", "ESTADO"]]
      )

  # TAB 2: ENVÍOS
  with tab_envios:
    st.subheader("Listado General de Envíos")
    st.table(st.session_state.db_logistica)

  # TAB 3: METRICAS
  with tab_kpi:
    st.subheader("Resumen del Estado Operativo")
    df_env = st.session_state.db_logistica
    m1, m2, m3 = st.columns(3)
    m1.metric("📦 Total de Envíos", len(df_env))
    m2.metric("✅ Entregados", len(df_env[df_env["ESTADO"] == "DELIVERED"]))
    m3.metric("🚚 En Ruta", len(df_env[df_env["ESTADO"] == "EN RUTA"]))

  # TAB 4: AUDITORIA
  with tab_audit:
    st.subheader("Registro de Movimientos")
    st.table(st.session_state.historial_acciones)
