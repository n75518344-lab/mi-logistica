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

# REVISAR SESIÓN Y QUERY PARAMS
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
    /* BLOQUEAR SCROLLBAR GLOBAL DE LA PANTALLA */
    html, body, .stApp { 
        overflow: hidden !important; 
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
        padding-bottom: 1rem !important; 
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div { 
        color: #0F172A; 
    }

    /* BOTÓN CERRAR SESIÓN CORREGIDO */
    div[data-testid="stButton"] > button[key="logout_btn_global"] {
        background-color: #FEE2E2 !important;
        color: #991B1B !important;
        border: 1px solid #FCA5A5 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    /* CONTENEDORES CON SCROLL INTELIGENTE PARA TABLAS */
    .tabla-contenedor, .tabla-contenedor-logs {
        max-height: 250px;
        height: fit-content;
        overflow-y: auto;
        overflow-x: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px !important;
    }

    .tabla-contenedor-operador {
        max-height: 480px;
        height: fit-content;
        overflow-y: auto;
        overflow-x: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
    }

    .tabla-contenedor::-webkit-scrollbar,
    .tabla-contenedor-logs::-webkit-scrollbar,
    .tabla-contenedor-operador::-webkit-scrollbar {
        width: 6px !important;
        height: 6px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb,
    .tabla-contenedor-logs::-webkit-scrollbar-thumb,
    .tabla-contenedor-operador::-webkit-scrollbar-thumb {
        background-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }

    /* ESTILOS DE TABLA */
    .tabla-usuarios, .tabla-pedidos {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
    }
    .tabla-usuarios th, .tabla-pedidos th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 10px 12px;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 700;
        white-space: nowrap;
    }
    .tabla-usuarios td, .tabla-pedidos td {
        padding: 8px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
        white-space: nowrap;
    }
    .tabla-usuarios tr:hover, .tabla-pedidos tr:hover {
        background-color: #F1F5F9;
    }

    /* INPUTS Y SELECTBOX */
    .stTextInput input, div[data-baseweb="select"] > div { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
    }

    /* FORMULARIO LOGIN */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 14px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 28px !important; 
        border-top: 6px solid #0F382C !important; 
    }

    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        color: #FFFFFF !important;
        border-radius: 8px !important; 
        border: none !important; 
        padding: 12px 20px !important; 
        width: 100% !important;
        min-height: 48px !important;
        font-weight: 700 !important;
    }

    /* TARJETAS DE KPIS */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.02);
    }
    .kpi-title { font-size: 13px; color: #64748B; font-weight: 600; }
    .kpi-value { font-size: 24px; color: #0F382C; font-weight: 800; margin-top: 5px; }

    /* EXPANDER */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        gap: 20px !important; 
        border-bottom: 2px solid #CBD5E1 !important; 
    }
    .stTabs [data-baseweb="tab"] p { color: #64748B !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #0F382C !important; }
    .stTabs [aria-selected="true"] p { color: #0F382C !important; font-weight: 800 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. INICIALIZACIÓN DE DATOS EN SESIÓN
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

if "historial_acciones" not in st.session_state:
  st.session_state.historial_acciones = pd.DataFrame([
      {
          "FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "USUARIO": "system",
          "ACCIÓN": "Inicio de sistema",
      }
  ])

if "pedidos_df" not in st.session_state:
  st.session_state.pedidos_df = pd.DataFrame([
      {
          "FECHA_REGISTRO": "08/07/2026",
          "CODIGO_INTERNO": "Tramontina",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "ENTREGADO",
          "SUB_ESTADO": "ENTREGA EFECTIVA",
          "NOMBRE": "CECILIA LOO",
          "DIRECCION": "AV. LA MAR 576",
          "DISTRITO": "ATE",
          "TIPO_SERVICIO": "SAME-DAY",
          "PLACA": "ABR120",
          "TELEFONO": "999999999",
      },
      {
          "FECHA_REGISTRO": "11/06/2026",
          "CODIGO_INTERNO": "SIN NUMERO",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "ENTREGADO",
          "SUB_ESTADO": "ENTREGA EFECTIVA",
          "NOMBRE": "LUIS FELIPE LLOSA",
          "DIRECCION": "CALLE LOS PINOS 123",
          "DISTRITO": "SAN ISIDRO",
          "TIPO_SERVICIO": "SAME-DAY",
          "PLACA": "BC-8921",
          "TELEFONO": "988888888",
      },
      {
          "FECHA_REGISTRO": "13/06/2026",
          "CODIGO_INTERNO": "BLC1-48039",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "ENTREGADO",
          "SUB_ESTADO": "ENTREGA EFECTIVA",
          "NOMBRE": "JOHN CASAS AGUILAR",
          "DIRECCION": "AV. LARCO 456",
          "DISTRITO": "MIRAFLORES",
          "TIPO_SERVICIO": "SAME-DAY",
          "PLACA": "ABR120",
          "TELEFONO": "977777777",
      },
      {
          "FECHA_REGISTRO": "13/06/2026",
          "CODIGO_INTERNO": "BLC2-5014",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "EN RUTA",
          "SUB_ESTADO": "EN TRÁNSITO",
          "NOMBRE": "JUAN CARLOS REYES",
          "DIRECCION": "JR. BENAVIDES 890",
          "DISTRITO": "MIRAFLORES",
          "TIPO_SERVICIO": "NEXT-DAY",
          "PLACA": "CD-4321",
          "TELEFONO": "966666666",
      },
      {
          "FECHA_REGISTRO": "13/06/2026",
          "CODIGO_INTERNO": "LWE2026-424",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "PENDIENTE",
          "SUB_ESTADO": "EN ALMACÉN",
          "NOMBRE": "MARIA EMILIA GUZMAN",
          "DIRECCION": "AV. PRIMAVERA 102",
          "DISTRITO": "SURCO",
          "TIPO_SERVICIO": "SAME-DAY",
          "PLACA": "SIN ASIGNAR",
          "TELEFONO": "955555555",
      },
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


def cerrar_sesion():
  registrar_log("Cierre de sesión")
  st.session_state.usuario_actual = None
  st.session_state.rol_actual = None
  st.query_params.clear()
  st.rerun()


# =============================================================
# VISTA 1: LOGIN
# =============================================================
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
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Módulo Administrador</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Módulo Operador / Almacén</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Tracking y Evidencias</div>
            <div style="color: #334155; font-weight: 600; font-size: 14px;">▌ Carga Masiva de Envíos</div>
        </div>
        """,
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

# =============================================================
# MÓDULOS DEL SISTEMA
# =============================================================
else:
  # CABECERA GENERAL DE SESIÓN ACTIVA
  col_nav1, col_nav2 = st.columns([5, 1])
  with col_nav1:
    rol_label = (
        "Portal Administrador"
        if "Administrador" in st.session_state.rol_actual
        else "Portal Operaciones"
    )
    st.markdown(
        f"""
        <div style="font-size: 22px; font-weight: 800; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — {rol_label}</div>
        <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 5px;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong> ({st.session_state.rol_actual})</div>
        """,
        unsafe_allow_html=True,
    )
  with col_nav2:
    if st.button(
        "🚪 Cerrar Sesión", key="logout_btn_global", use_container_width=True
    ):
      cerrar_sesion()

  # -------------------------------------------------------------
  # VISTA 2: INTERFAZ DEL ADMINISTRADOR
  # -------------------------------------------------------------
  if "Administrador" in st.session_state.rol_actual:
    tab1, tab2 = st.tabs(["Usuarios y Claves", "Auditoría (Logs)"])

    with tab1:
      col_a, col_b = st.columns([1, 1.3], gap="large")

      with col_a:
        st.subheader("➕ Crear Nuevo Usuario")
        with st.form("form_crear"):
          nu = st.text_input(
              "Nombre de Usuario", placeholder="Ej: operador_lima"
          )
          np = st.text_input(
              "Contraseña Inicial",
              type="password",
              placeholder="Clave temporal",
          )
          nr = st.selectbox(
              "Rol Asignado",
              ["🛠️ Operario", "🏢 Cliente", "🛵 Repartidor (App)"],
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

        tabla_html = f"""
                <div class="tabla-contenedor">
                    <table class="tabla-usuarios">
                        <thead>
                            <tr><th>USUARIO</th><th>ROL</th><th>ESTADO</th><th>ÚLTIMA CONEXIÓN</th></tr>
                        </thead>
                        <tbody>{filas_html}</tbody>
                    </table>
                </div>
                """
        st.markdown(tabla_html, unsafe_allow_html=True)

        st.subheader("⚙️ Gestión de Claves y Accesos")
        lista_usuarios_gestion = st.session_state.usuarios_registrados[
            st.session_state.usuarios_registrados["USUARIO"]
            != st.session_state.usuario_actual
        ]["USUARIO"].tolist()

        if lista_usuarios_gestion:
          usr_gestion = st.selectbox(
              "Selecciona un usuario para gestionar",
              lista_usuarios_gestion,
              key="select_gestion",
          )

          with st.expander("🔑 Restablecer Contraseña Directamente"):
            nueva_pass_admin = st.text_input(
                f"Nueva Contraseña para {usr_gestion}",
                type="password",
                key="n_p_admin",
            )
            if st.button("🔄 Actualizar Clave", use_container_width=True):
              if nueva_pass_admin:
                st.session_state.usuarios_registrados.loc[
                    st.session_state.usuarios_registrados["USUARIO"]
                    == usr_gestion,
                    "PASS",
                ] = nueva_pass_admin
                registrar_log(
                    f"Restableció la contraseña del usuario '{usr_gestion}'"
                )
                st.success(f"✅ Contraseña de '{usr_gestion}' actualizada.")
                st.rerun()

          col_e1, col_e2 = st.columns(2)
          with col_e1:
            if st.button(
                "🚫 Dar de Baja / Inactivar",
                use_container_width=True,
                key="inactivar_btn",
            ):
              st.session_state.usuarios_registrados.loc[
                  st.session_state.usuarios_registrados["USUARIO"]
                  == usr_gestion,
                  "ESTADO",
              ] = "Inactivo"
              registrar_log(f"Inactivó al usuario '{usr_gestion}'")
              st.rerun()

          with col_e2:
            if st.button(
                "❌ Eliminar Cuenta",
                use_container_width=True,
                key="eliminar_btn",
            ):
              st.session_state.usuarios_registrados = (
                  st.session_state.usuarios_registrados[
                      st.session_state.usuarios_registrados["USUARIO"]
                      != usr_gestion
                  ]
              )
              registrar_log(f"Eliminó al usuario '{usr_gestion}'")
              st.rerun()

    with tab2:
      st.subheader("📜 Historial de Seguridad y Movimientos")
      filas_logs = ""
      for _, fila in st.session_state.historial_acciones.iterrows():
        filas_logs += f"<tr><td>{fila['FECHA Y HORA']}</td><td><b>{fila['USUARIO']}</b></td><td>{fila['ACCIÓN']}</td></tr>"

      st.markdown(
          f"""
            <div class="tabla-contenedor-logs">
                <table class="tabla-usuarios">
                    <thead><tr><th>FECHA Y HORA</th><th>USUARIO</th><th>ACCIÓN</th></tr></thead>
                    <tbody>{filas_logs}</tbody>
                </table>
            </div>
            """,
          unsafe_allow_html=True,
      )

  # -------------------------------------------------------------
  # VISTA 3: INTERFAZ DEL OPERADOR (🛠️ Operario)
  # -------------------------------------------------------------
  else:
    tab_dash, tab_pedidos, tab_carga = st.tabs(
        ["📊 Panel de Control", "📦 Gestión de Pedidos", "📥 Cargar Data"]
    )

    with tab_dash:
      df = st.session_state.pedidos_df
      c1, c2, c3, c4 = st.columns(4)
      with c1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">TOTAL'
            f' PEDIDOS</div><div class="kpi-value">{len(df)}</div></div>',
            unsafe_allow_html=True,
        )
      with c2:
        entregados = len(df[df["ESTADO"] == "ENTREGADO"])
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">ENTREGADOS</div><div'
            f' class="kpi-value" style="color:#16A34A;">{entregados}</div></div>',
            unsafe_allow_html=True,
        )
      with c3:
        en_ruta = len(df[df["ESTADO"] == "EN RUTA"])
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">EN RUTA</div><div'
            f' class="kpi-value" style="color:#D97706;">{en_ruta}</div></div>',
            unsafe_allow_html=True,
        )
      with c4:
        pendientes = len(df[df["ESTADO"] == "PENDIENTE"])
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">EN'
            ' ALMACÉN</div><div class="kpi-value"'
            f' style="color:#DC2626;">{pendientes}</div></div>',
            unsafe_allow_html=True,
        )

      st.markdown("<br>", unsafe_allow_html=True)
      st.subheader("Avance de Ruta del Día")
      st.bar_chart(df["ESTADO"].value_counts())

    with tab_pedidos:
      col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
      with col_f1:
        buscar = st.text_input(
            "🔍 Buscar por Cliente, Código, Nombre o Distrito:", key="b_op"
        )
      with col_f2:
        filtro_estado = st.selectbox(
            "Filtrar por Estado:",
            ["TODOS", "ENTREGADO", "EN RUTA", "PENDIENTE"],
            key="e_op",
        )
      with col_f3:
        filtro_cliente = st.selectbox(
            "Filtrar por Cliente:",
            ["TODOS"] + list(st.session_state.pedidos_df["CLIENTE"].unique()),
            key="c_op",
        )

      df_filtrado = st.session_state.pedidos_df.copy()
      if buscar:
        df_filtrado = df_filtrado[
            df_filtrado.apply(
                lambda r: r.astype(str).str.contains(buscar, case=False).any(),
                axis=1,
            )
        ]
      if filtro_estado != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["ESTADO"] == filtro_estado]
      if filtro_cliente != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["CLIENTE"] == filtro_cliente]

      col_tabla, col_detalle = st.columns([1.8, 1.2], gap="medium")

      with col_tabla:
        filas_html = ""
        for _, row in df_filtrado.iterrows():
          badge_color = (
              "#16A34A"
              if row["ESTADO"] == "ENTREGADO"
              else ("#D97706" if row["ESTADO"] == "EN RUTA" else "#DC2626")
          )
          filas_html += f"<tr><td><b>{row['FECHA_REGISTRO']}</b></td><td><b>{row['CODIGO_INTERNO']}</b></td><td>{row['CLIENTE']}</td><td><span style='color:{badge_color}; font-weight:bold;'>{row['ESTADO']}</span></td><td>{row['NOMBRE']}</td><td>{row['DISTRITO']}</td></tr>"

        st.markdown(
            f"""
                <div class="tabla-contenedor-operador">
                    <table class="tabla-pedidos">
                        <thead><tr><th>FECHA</th><th>CÓDIGO</th><th>CLIENTE</th><th>ESTADO</th><th>DESTINATARIO</th><th>DISTRITO</th></tr></thead>
                        <tbody>{filas_html}</tbody>
                    </table>
                </div>
                """,
            unsafe_allow_html=True,
        )

      with col_detalle:
        st.markdown("**📌 Ficha y Evidencia de Pedido**")
        opciones_pedidos = df_filtrado["CODIGO_INTERNO"].tolist()
        if opciones_pedidos:
          pedido_sel = st.selectbox(
              "Seleccionar Código para ver Detalle / POD:", opciones_pedidos
          )
          registro = df_filtrado[
              df_filtrado["CODIGO_INTERNO"] == pedido_sel
          ].iloc[0]

          st.info(
              f"📦 **Código:** {registro['CODIGO_INTERNO']} | **Cliente:**"
              f" {registro['CLIENTE']}"
          )
          st.markdown(f"""
                    * **Destinatario:** {registro['NOMBRE']}
                    * **Teléfono:** {registro['TELEFONO']}
                    * **Dirección:** {registro['DIRECCION']} ({registro['DISTRITO']})
                    * **Servicio:** `{registro['TIPO_SERVICIO']}` | **Placa:** `{registro['PLACA']}`
                    * **Estado:** **{registro['ESTADO']}** ({registro['SUB_ESTADO']})
                    """)
          st.markdown("---")
          st.markdown("**📸 Evidencia de Entrega (POD):**")
          st.image(
              "https://via.placeholder.com/350x180.png?text=FOTO+EVIDENCIA+GUIA+FIRMADA",
              use_container_width=True,
          )
        else:
          st.warning("No hay pedidos para mostrar.")

    with tab_carga:
      st.subheader("📥 Cargar Matriz de Envíos Masivos")
      uploaded_file = st.file_uploader(
          "Selecciona el archivo Excel/CSV", type=["xlsx", "csv"]
      )
      if uploaded_file is not None:
        try:
          df_nuevo = (
              pd.read_csv(uploaded_file)
              if uploaded_file.name.endswith(".csv")
              else pd.read_excel(uploaded_file)
          )
          st.success(
              f"✅ Archivo cargado correctamente con {len(df_nuevo)} registros."
          )
          st.dataframe(df_nuevo.head(), use_container_width=True)
          if st.button("🚀 Importar a la Base de Datos"):
            st.session_state.pedidos_df = pd.concat(
                [st.session_state.pedidos_df, df_nuevo], ignore_index=True
            )
            st.success("¡Data integrada con éxito!")
            st.rerun()
        except Exception as e:
          st.error(f"Error al leer el archivo: {e}")
