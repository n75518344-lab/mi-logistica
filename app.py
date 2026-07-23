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

# CSS Y ESTILOS
st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { 
        display: none !important; 
    }
    .stApp { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
    }
    .block-container { 
        max-width: 90% !important; 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important; 
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A !important; 
    }
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 16px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 28px !important; 
        border-top: 5px solid #0F382C !important; 
    }
    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
    }
    
    /* SELECTBOX Y NAVEGACIÓN */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    
    /* BOTONES PRIMARIOS */
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        border-radius: 8px !important; 
        border: none !important; 
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] > button p { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
    }
    div[data-testid="stButton"] > button { 
        border-radius: 8px !important; 
    }

    /* PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; gap: 6px; }
    .stTabs [data-baseweb="tab"] { background-color: #E2E8F0 !important; border-radius: 8px 8px 0px 0px !important; }
    .stTabs [data-baseweb="tab"] p { color: #334155 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] { background-color: #0F382C !important; }
    .stTabs [aria-selected="true"] p { color: #FFFFFF !important; font-weight: 800 !important; }

    /* TABLAS COMPACTAS Y TEXTO BLANCO EN ENCABEZADOS */
    .stTable, [data-testid="stTable"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stTable th, [data-testid="stTable"] th { 
        background-color: #0F382C !important; 
        padding: 8px 12px !important; 
        border-bottom: 1px solid #0B2B22 !important;
        text-align: left !important;
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
        padding: 10px 12px !important;
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

if "solicitudes_clave" not in st.session_state:
  st.session_state.solicitudes_clave = pd.DataFrame([
      {
          "FECHA": "2026-07-22 10:15",
          "USUARIO": "cliente_global",
          "MOTIVO": "Olvidé mi contraseña",
          "ESTADO": "PENDIENTE",
      }
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


# VISTA DE LOGIN
if st.session_state.usuario_actual is None:
  col_left, col_right = st.columns([1.3, 1.0], gap="large")
  with col_right:
    with st.form("login_form"):
      st.markdown(
          '<h2 style="text-align: center; color: #0F382C;">Acceso'
          " Administrador</h2>",
          unsafe_allow_html=True,
      )
      u = st.text_input("Usuario")
      p = st.text_input("Contraseña", type="password")
      if st.form_submit_button("Ingresar"):
        df_u = st.session_state.usuarios_registrados
        match = df_u[(df_u["USUARIO"] == u) & (df_u["PASS"] == p)]
        if not match.empty:
          st.session_state.usuario_actual = u
          st.session_state.rol_actual = match.iloc[0]["ROL"]
          registrar_log("Inicio de sesión Admin")
          st.rerun()
        else:
          st.error("Credenciales incorrectas")

# VISTA PRINCIPAL (ADMINISTRADOR)
else:
  c1, c2 = st.columns([5, 1])
  with c1:
    st.markdown(
        f"<h2 style='color:#0F382C; margin:0;'>🌲 ALFA CARGO EXPRESS — Portal"
        f" Administrador</h2><p>Admin activo:"
        f" <b>{st.session_state.usuario_actual}</b></p>",
        unsafe_allow_html=True,
    )
  with c2:
    if st.button("🚪 Cerrar Sesión", key="logout"):
      registrar_log("Cierre de sesión")
      st.session_state.usuario_actual = None
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  # NUEVAS PESTAÑAS EXCLUSIVAS DE ADMINISTRACIÓN
  tab1, tab2, tab3, tab4 = st.tabs([
      "👥 Control de Usuarios",
      "🔑 Restablecer Contraseñas",
      "⚙️ Configuración del Sistema",
      "📜 Registro de Auditoría",
  ])

  # PESTAÑA 1: CONTROL DE USUARIOS (CREAR, ELIMINAR Y CAMBIAR ESTADO)
  with tab1:
    col_a, col_b = st.columns([1, 1.3], gap="large")

    with col_a:
      st.subheader("➕ Crear Nuevo Usuario")
      with st.form("form_crear"):
        nu = st.text_input("Nombre de Usuario")
        np = st.text_input("Contraseña Inicial", type="password")
        nr = st.selectbox(
            "Rol",
            [
                "🛠️ Operario",
                "🏢 Cliente",
                "🛵 Repartidor (App)",
                "👨‍💼 Portal Administrador",
            ],
        )
        if st.form_submit_button("Guardar Usuario"):
          if (
              nu
              and np
              and nu
              not in st.session_state.usuarios_registrados["USUARIO"].values
          ):
            nueva_f = pd.DataFrame(
                [{"USUARIO": nu, "PASS": np, "ROL": nr, "ESTADO": "Activo"}]
            )
            st.session_state.usuarios_registrados = pd.concat(
                [st.session_state.usuarios_registrados, nueva_f],
                ignore_index=True,
            )
            registrar_log(f"Creó al usuario '{nu}'")
            st.success("Usuario creado con éxito")
            st.rerun()
          else:
            st.error("Error: Usuario existente o campos vacíos")

    with col_b:
      st.subheader("📋 Lista de Usuarios y Acciones")
      st.table(
          st.session_state.usuarios_registrados[["USUARIO", "ROL", "ESTADO"]]
      )

      st.markdown("---")
      st.subheader("🗑️ Eliminar / Dar de Baja Usuario")
      usr_eliminar = st.selectbox(
          "Selecciona usuario a gestionar",
          st.session_state.usuarios_registrados["USUARIO"].tolist(),
      )

      col_e1, col_e2 = st.columns(2)
      with col_e1:
        if st.button("🚫 Dar de Baja / Inactivar", use_container_width=True):
          st.session_state.usuarios_registrados.loc[
              st.session_state.usuarios_registrados["USUARIO"] == usr_eliminar,
              "ESTADO",
          ] = "Inactivo"
          registrar_log(f"Inactivó al usuario '{usr_eliminar}'")
          st.success(f"Usuario {usr_eliminar} inhabilitado")
          st.rerun()

      with col_e2:
        if st.button("❌ Eliminar Definitivamente", use_container_width=True):
          if usr_eliminar != st.session_state.usuario_actual:
            st.session_state.usuarios_registrados = (
                st.session_state.usuarios_registrados[
                    st.session_state.usuarios_registrados["USUARIO"]
                    != usr_eliminar
                ]
            )
            registrar_log(f"Eliminó al usuario '{usr_eliminar}'")
            st.success(f"Usuario {usr_eliminar} eliminado")
            st.rerun()
          else:
            st.error("No puedes eliminar tu propio usuario activo.")

  # PESTAÑA 2: RESTABLECER CONTRASEÑAS (SOLICITUDES Y RESET DIRECTO)
  with tab2:
    st.subheader("📩 Solicitudes Pendientes de Contraseña")
    st.table(st.session_state.solicitudes_clave)

    st.markdown("---")
    st.subheader("🔑 Restablecer Clave de Forma Directa")
    col_r1, col_r2 = st.columns(2)

    with col_r1:
      usr_reset = st.selectbox(
          "Seleccionar Usuario",
          st.session_state.usuarios_registrados["USUARIO"].tolist(),
          key="select_reset",
      )
    with col_r2:
      nueva_pass_admin = st.text_input(
          "Nueva Contraseña Temporal", type="password"
      )

    if st.button("🔄 Actualizar Contraseña"):
      if nueva_pass_admin:
        st.session_state.usuarios_registrados.loc[
            st.session_state.usuarios_registrados["USUARIO"] == usr_reset,
            "PASS",
        ] = nueva_pass_admin
        # Cambiar estado de la solicitud a ATENDIDO si existía
        st.session_state.solicitudes_clave.loc[
            st.session_state.solicitudes_clave["USUARIO"] == usr_reset, "ESTADO"
        ] = "ATENDIDO"
        registrar_log(f"Restableció la contraseña de '{usr_reset}'")
        st.success(f"✅ Contraseña de {usr_reset} actualizada correctamente.")
        st.rerun()

  # PESTAÑA 3: CONFIGURACIÓN DEL SISTEMA
  with tab3:
    st.subheader("⚙️ Parámetros Generales de la Empresa")
    with st.form("form_config"):
      c_empresa = st.text_input(
          "Nombre de la Empresa", value="Alfa Cargo Express S.A.C."
      )
      c_ruc = st.text_input("RUC", value="20601234567")
      c_correo = st.text_input("Correo de Soporte", value="soporte@alfacargo.pe")
      c_moneda = st.selectbox("Moneda del Sistema", ["Soles (S/)", "Dólares ($)"])

      if st.form_submit_button("Guardar Cambios de Configuración"):
        registrar_log("Actualizó la configuración general del sistema")
        st.success("Configuración guardada.")

  # PESTAÑA 4: AUDITORÍA (HISTORIAL DE SEGURIDAD)
  with tab4:
    st.subheader("📜 Historial de Actividad y Seguridad (Logs)")
    st.table(st.session_state.historial_acciones)
