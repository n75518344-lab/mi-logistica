import base64
from datetime import datetime
import os
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

# CSS PERFECCIONADO PARA LOGIN Y DASHBOARD
st.markdown(
    """
    <style>
    /* OCULTAR SIDEBAR Y CABECERA */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { 
        display: none !important; 
    }
    
    /* FONDO Y TEXTOS PRINCIPALES */
    .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }
    .block-container { 
        max-width: 88% !important; 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A !important; 
    }

    /* CONTENEDOR DE FORMULARIO DE LOGIN (TARJETA DERECHA) */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 14px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 28px !important; 
        border-top: 6px solid #0F382C !important; 
    }

    /* INPUTS DE TEXTO */
    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    .stTextInput input::placeholder { color: #94A3B8 !important; }

    /* LIMPIEZA DEL OJO EN CONTRASEÑA */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        border: none !important;
    }
    button[aria-label="Show password"], button[aria-label="Hide password"] {
        background-color: transparent !important;
        border: none !important;
    }
    button[aria-label="Show password"] svg, button[aria-label="Hide password"] svg {
        fill: #0F382C !important;
    }

    /* CORRECCIÓN DEL BOTÓN "INGRESAR AL PORTAL" */
    div[data-testid="stFormSubmitButton"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin-top: 10px !important;
    }
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        border-radius: 8px !important; 
        border: none !important; 
        padding: 12px 20px !important; 
        width: 100% !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[data-testid="stFormSubmitButton"] > button p, 
    div[data-testid="stFormSubmitButton"] > button span,
    div[data-testid="stFormSubmitButton"] > button div { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 15px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover { 
        background-color: #15803D !important; 
    }

    /* SELECTBOX */
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
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    li[role="option"], div[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"]:hover, div[role="option"]:hover {
        background-color: #F1F5F9 !important;
        color: #0F382C !important;
    }

    /* BOTONES ESTÁNDAR FUERA DE FORMULARIOS */
    div[data-testid="stButton"] > button { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
        font-weight: 600 !important;
    }

    /* BOTÓN CERRAR SESIÓN */
    #logout_btn button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #logout_btn button p, #logout_btn button span {
        color: #991B1B !important;
        font-weight: 700 !important;
    }

    /* BOTONES ACCIÓN USUARIO */
    #btn_inactivar button {
        background-color: #FEF3C7 !important;
        border: 1px solid #FCD34D !important;
    }
    #btn_inactivar button p, #btn_inactivar button span {
        color: #92400E !important;
        font-weight: 700 !important;
    }

    #btn_eliminar button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #btn_eliminar button p, #btn_eliminar button span {
        color: #991B1B !important;
        font-weight: 700 !important;
    }

    /* PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        gap: 8px; 
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: #E2E8F0 !important; 
        border-radius: 8px 8px 0px 0px !important; 
        padding: 8px 16px !important;
        border: none !important; 
    }
    .stTabs [data-baseweb="tab"] p { 
        color: #334155 !important; 
        font-weight: 700 !important; 
    }
    .stTabs [aria-selected="true"] { 
        background-color: #0F382C !important; 
    }
    .stTabs [aria-selected="true"] p { 
        color: #FFFFFF !important; 
        font-weight: 800 !important; 
    }

    /* TABLAS COMPACTAS */
    .stTable, [data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stTable th, [data-testid="stTable"] th { 
        background-color: #0F382C !important; 
        padding: 8px 12px !important; 
        border: none !important;
    }
    .stTable th *, [data-testid="stTable"] th * { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 13px !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .stTable td, [data-testid="stTable"] td { 
        color: #1E293B !important; 
        background-color: #FFFFFF !important; 
        padding: 8px 12px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        font-size: 13.5px !important;
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


# MODAL / VENTANA EMERGENTE DE SOPORTE PARA CLAVES
@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
  st.markdown("""
        <div style="font-size: 14.5px; color: #FFFFFF !important; line-height: 1.6;">
            <p style="color: #FFFFFF !important; font-size: 14.5px;">
                Por motivos de seguridad corporativa, la asignación y restablecimiento de contraseñas es gestionada de manera directa por el área de Administración.
            </p>
            <p style="color: #FFFFFF !important; font-weight: 700; margin-top: 15px; margin-bottom: 8px;">
                Canales de atención:
            </p>
            <ul style="color: #FFFFFF !important; list-style-type: none; padding-left: 0;">
                <li style="color: #FFFFFF !important; margin-bottom: 6px;">💬 <strong>WhatsApp Soporte:</strong> +51 987 654 321</li>
                <li style="color: #FFFFFF !important; margin-bottom: 6px;">✉️ <strong>Correo Institucional:</strong> soporte@alfacargo.pe</li>
                <li style="color: #FFFFFF !important; margin-bottom: 6px;">🕒 <strong>Horario de Atención:</strong> Lun a Vie de 8:00 am a 6:00 pm</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("Entendido", use_container_width=True):
    st.rerun()


# VISTA DE LOGIN
if st.session_state.usuario_actual is None:
  st.markdown(
      """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
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
          ' max-height: 280px; object-fit: contain; border-radius: 12px;" />',
          unsafe_allow_html=True,
      )

  with col_right:
    with st.form("login_form"):
      st.markdown(
          '<h3 style="text-align: center; color: #0F382C; font-weight:800;'
          ' margin-bottom: 20px;">Acceso Administrador</h3>',
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

    # ENLACE DE SOPORTE FUERA DEL FORMULARIO PARA ABRIR MODAL
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(
        "❓ ¿Necesitas ayuda con tu acceso o contraseña?",
        use_container_width=True,
    ):
      mostrar_modal_soporte()

# VISTA DASHBOARD (ADMINISTRADOR)
else:
  col_nav1, col_nav2 = st.columns([5, 1])
  with col_nav1:
    st.markdown(
        f"""
            <div style="font-size: 24px; font-weight: 800; color: #0F382C;">🌲 ALFA CARGO EXPRESS — Portal Administrador</div>
            <div style="font-size: 14px; color: #475569; font-weight: 600;">Admin activo: <strong>{st.session_state.usuario_actual}</strong></div>
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

  st.markdown("<br>", unsafe_allow_html=True)

  tab1, tab2 = st.tabs(
      ["👥 Control de Usuarios y Claves", "📜 Registro de Auditoría (Logs)"]
  )

  # TAB 1: CONTROL DE USUARIOS Y CLAVES
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
            [
                "🛠️ Operario",
                "🏢 Cliente",
                "🛵 Repartidor (App)",
                "👨‍💼 Portal Administrador",
            ],
        )

        btn_crear = st.form_submit_button("Guardar Usuario")

        if btn_crear:
          if nu and np:
            if (
                nu
                in st.session_state.usuarios_registrados["USUARIO"].values
            ):
              st.error("El nombre de usuario ya existe.")
            else:
              nueva_f = pd.DataFrame(
                  [{"USUARIO": nu, "PASS": np, "ROL": nr, "ESTADO": "Activo"}]
              )
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
      st.table(
          st.session_state.usuarios_registrados[["USUARIO", "ROL", "ESTADO"]]
      )

      st.markdown("---")
      st.subheader("⚙️ Gestión de Claves y Accesos")
      usr_gestion = st.selectbox(
          "Selecciona un usuario para gestionar",
          st.session_state.usuarios_registrados["USUARIO"].tolist(),
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
            st.success(
                f"✅ Contraseña de '{usr_gestion}' actualizada correctamente."
            )
            st.rerun()
          else:
            st.warning("Escribe la nueva clave.")

      col_e1, col_e2 = st.columns(2)
      with col_e1:
        st.markdown('<div id="btn_inactivar">', unsafe_allow_html=True)
        if st.button(
            "🚫 Dar de Baja / Inactivar",
            use_container_width=True,
            key="inactivar_btn",
        ):
          st.session_state.usuarios_registrados.loc[
              st.session_state.usuarios_registrados["USUARIO"] == usr_gestion,
              "ESTADO",
          ] = "Inactivo"
          registrar_log(f"Inactivó al usuario '{usr_gestion}'")
          st.success(f"Usuario '{usr_gestion}' marcado como Inactivo.")
          st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

      with col_e2:
        st.markdown('<div id="btn_eliminar">', unsafe_allow_html=True)
        if st.button(
            "❌ Eliminar Cuenta",
            use_container_width=True,
            key="eliminar_btn",
        ):
          if usr_gestion != st.session_state.usuario_actual:
            st.session_state.usuarios_registrados = (
                st.session_state.usuarios_registrados[
                    st.session_state.usuarios_registrados["USUARIO"]
                    != usr_gestion
                ]
            )
            registrar_log(f"Eliminó al usuario '{usr_gestion}'")
            st.success(f"Usuario '{usr_gestion}' eliminado.")
            st.rerun()
          else:
            st.error("No puedes eliminar la cuenta actualmente en uso.")
        st.markdown("</div>", unsafe_allow_html=True)

  # TAB 2: AUDITORÍA
  with tab2:
    st.subheader("📜 Historial de Seguridad y Movimientos")
    st.table(st.session_state.historial_acciones)
