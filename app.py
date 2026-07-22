import base64
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

# REVISAR SESIÓN
query_params = st.query_params

if "usuario_actual" not in st.session_state:
  if "saved_user" in query_params:
    st.session_state.usuario_actual = query_params["saved_user"]
    st.session_state.rol_actual = query_params.get("saved_rol", "Administrador")
  else:
    st.session_state.usuario_actual = None
    st.session_state.rol_actual = None

# 2. ESTILOS CSS - VERDE OSCURO CORPORATIVO (ESTILO APPSHEET)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    .stApp { background-color: #F4F7F6 !important; }

    .block-container {
        max-width: 92% !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* HEADER VERDE OSCURO */
    .brand-logo { font-size: 28px !important; font-weight: 900; color: #0F382C; }
    
    /* LOGIN CARD */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border-top: 6px solid #0F382C !important;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08) !important;
        padding: 35px !important;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #0F382C !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
    }

    div[data-testid="stFormSubmitButton"] > button {
        background-color: #0F382C !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 0px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1B4D3E !important;
    }

    /* CHECKBOX "RECORDAR" */
    [data-testid="stCheckbox"] label p {
        color: #0F382C !important;
        font-weight: 700 !important;
    }

    /* PESTAÑAS (TABS) VERDE OSCURO */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0 !important;
        border-radius: 6px 6px 0px 0px !important;
        padding: 10px 20px !important;
        color: #0F382C !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F382C !important;
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] p { color: #FFFFFF !important; }

    /* DETALLE LATERAL TIPO APPSHEET */
    .detail-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .detail-label { font-size: 11px; color: #64748B; font-weight: 800; text-transform: uppercase; margin-top: 8px; }
    .detail-val { font-size: 14px; color: #0F382C; font-weight: 700; }

    /* VISTA MÓVIL REPARTIDOR */
    .mobile-card {
        background: #FFFFFF;
        border-left: 5px solid #0F382C;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. DATOS DE PRUEBA INITIALES
if "db_pedidos" not in st.session_state:
  st.session_state.db_pedidos = pd.DataFrame([
      {
          "FECHA_REGISTRO": "8/7/2026",
          "CODIGO INTERNO": "Tramontina",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "ENTREGADO",
          "SUB_ESTADO": "ENTREGA EFECTIVA",
          "NOMBRE": "CECILIA LOO",
          "DISTRITO": "ATE",
          "DIRECCION": "AV. LA MAR 576",
          "TELEFONO": "999999999",
          "PESO": "1.00",
          "TIPO_SERVICIO": "SAME-DAY",
          "REPARTIDOR": "Juan Pérez",
          "EVIDENCIA": "https://via.placeholder.com/150",
      },
      {
          "FECHA_REGISTRO": "11/6/2026",
          "CODIGO INTERNO": "SIN NUMERO",
          "CLIENTE": "UNIMARKET",
          "ESTADO": "EN RUTA",
          "SUB_ESTADO": "EN TRANSITO",
          "NOMBRE": "LUIS FELIPE LLOSA",
          "DISTRITO": "SAN ISIDRO",
          "DIRECCION": "CALLE LOS OLIVOS 123",
          "TELEFONO": "987654321",
          "PESO": "2.50",
          "TIPO_SERVICIO": "SAME-DAY",
          "REPARTIDOR": "Juan Pérez",
          "EVIDENCIA": "Sin evidencia",
      },
  ])

if "usuarios" not in st.session_state:
  st.session_state.usuarios = {
      "admin": {"pass": "admin123", "rol": "👑 Administrador"},
      "operativa": {"pass": "op123", "rol": "⚙️ Operativo"},
      "unimarket": {"pass": "cliente123", "rol": "🏢 Cliente"},
      "driver1": {"pass": "driver123", "rol": "🚚 Repartidor (App)"},
  }


def obtener_imagen_github(nombre_archivo="alfa_warehouse.jpg"):
  if os.path.exists(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
      return base64.b64encode(f.read()).decode("utf-8")
  return None


# 4. PANTALLA LOGIN
if st.session_state.usuario_actual is None:
  col_a, col_b = st.columns([1.2, 1.0], gap="large")

  with col_a:
    st.markdown(
        '<div class="brand-logo">🌲 ALFA CARGO EXPRESS</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Sistema de Control Logístico & Distribución")
    st.markdown(
        "--- \n* Trazabilidad en tiempo real.\n* Confirmación y digitalización"
        " de guías.\n* Cobertura Lima y Provincias."
    )

    img_b64 = obtener_imagen_github("alfa_warehouse.jpg")
    if img_b64:
      st.markdown(
          f'<img src="data:image/jpeg;base64,{img_b64}" style="width:100%;'
          ' border-radius:10px; margin-top:15px;" />',
          unsafe_allow_html=True,
      )

  with col_b:
    with st.form("form_login"):
      st.markdown(
          "<h2 style='text-align:center; color:#0F382C;'>Iniciar Sesión</h2>",
          unsafe_allow_html=True,
      )
      u_input = st.text_input("Usuario")
      p_input = st.text_input("Contraseña", type="password")
      remember = st.checkbox("Recordar Sesión", value=True)

      if st.form_submit_button("Ingresar al Sistema", use_container_width=True):
        if (
            u_input in st.session_state.usuarios
            and st.session_state.usuarios[u_input]["pass"] == p_input
        ):
          st.session_state.usuario_actual = u_input
          st.session_state.rol_actual = st.session_state.usuarios[u_input][
              "rol"
          ]

          if remember:
            st.query_params["saved_user"] = u_input
            st.query_params["saved_rol"] = st.session_state.rol_actual

          st.rerun()
        else:
          st.error("❌ Credenciales inválidas.")

# 5. VISTAS SEGÚN EL ROL
else:
  # HEADER
  col_head1, col_head2 = st.columns([5, 1])
  with col_head1:
    st.markdown(
        f"<h2 style='color:#0F382C; margin:0;'>🌲 ALFA CARGO —"
        f" {st.session_state.rol_actual}</h2>",
        unsafe_allow_html=True,
    )
    st.caption(f"Usuario: **{st.session_state.usuario_actual}**")
  with col_head2:
    if st.button("🚪 Salir"):
      st.session_state.usuario_actual = None
      st.session_state.rol_actual = None
      st.query_params.clear()
      st.rerun()

  st.markdown("---")

  # -------------------------------------------------------------
  # A. ROL ADMINISTRADOR ("DIOS") -> SOLO GESTIÓN DE USUARIOS
  # -------------------------------------------------------------
  if st.session_state.rol_actual == "👑 Administrador":
    st.markdown("### 👑 Panel Global: Creación de Usuarios")

    col_u1, col_u2 = st.columns([1, 1], gap="large")
    with col_u1:
      with st.form("form_crear_usr"):
        st.markdown("#### ➕ Crear Nuevo Usuario")
        new_u = st.text_input("Nombre de Usuario")
        new_p = st.text_input("Contraseña", type="password")
        new_r = st.selectbox(
            "Rol",
            ["⚙️ Operativo", "🏢 Cliente", "🚚 Repartidor (App)"],
        )

        if st.form_submit_button("Registrar Usuario"):
          if new_u and new_p:
            st.session_state.usuarios[new_u] = {"pass": new_p, "rol": new_r}
            st.success(f"¡Usuario **{new_u}** creado correctamente!")
          else:
            st.warning("Completa los datos.")

    with col_u2:
      st.markdown("#### 👥 Usuarios Activos")
      df_u = pd.DataFrame([
          {"Usuario": k, "Rol": v["rol"]}
          for k, v in st.session_state.usuarios.items()
      ])
      st.dataframe(df_u, use_container_width=True)

  # -------------------------------------------------------------
  # B. ROL OPERATIVO -> SUBIR DATA Y DETALLE DE PEDIDOS (IMÁGENES 1 Y 2)
  # -------------------------------------------------------------
  elif st.session_state.rol_actual == "⚙️ Operativo":
    tab_pedidos, tab_cargar = st.tabs(
        ["📦 Detalle de Pedidos", "📤 Cargar Base (Excel/CSV)"]
    )

    with tab_pedidos:
      st.markdown("### DASHBOARD > Detalle de pedidos")

      # Distribución tipo Imagen 2 (Tabla a la izquierda, detalle a la derecha)
      col_tabla, col_detalle = st.columns([2.2, 1.0], gap="medium")

      with col_tabla:
        st.dataframe(
            st.session_state.db_pedidos[[
                "FECHA_REGISTRO",
                "CODIGO INTERNO",
                "CLIENTE",
                "ESTADO",
                "SUB_ESTADO",
                "NOMBRE",
                "DISTRITO",
                "TIPO_SERVICIO",
            ]],
            use_container_width=True,
        )

      with col_detalle:
        st.markdown(
            "### 🔎 Pedidos filtro",
            unsafe_allow_html=True,
        )

        # Seleccionar pedido para ver detalle
        codigos = st.session_state.db_pedidos["CODIGO INTERNO"].tolist()
        sel_cod = st.selectbox("Seleccionar Código:", codigos)

        pedido_sel = st.session_state.db_pedidos[
            st.session_state.db_pedidos["CODIGO INTERNO"] == sel_cod
        ].iloc[0]

        st.markdown(
            f"""
                <div class="detail-card">
                    <div class="detail-label">NOMBRE</div><div class="detail-val">{pedido_sel['NOMBRE']}</div>
                    <div class="detail-label">DIRECCIÓN</div><div class="detail-val">{pedido_sel['DIRECCION']}</div>
                    <div class="detail-label">DISTRITO</div><div class="detail-val">{pedido_sel['DISTRITO']}</div>
                    <div class="detail-label">TELÉFONO</div><div class="detail-val">{pedido_sel['TELEFONO']}</div>
                    <div class="detail-label">PESO</div><div class="detail-val">{pedido_sel['PESO']} KG</div>
                    <div class="detail-label">REPARTIDOR ASIGNADO</div><div class="detail-val">{pedido_sel['REPARTIDOR']}</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_cargar:
      st.markdown("### 📤 Cargar Nueva Base de Pedidos")
      uploaded_file = st.file_uploader(
          "Arrastra tu archivo Excel o CSV", type=["csv", "xlsx"]
      )
      if uploaded_file:
        df_subido = (
            pd.read_csv(uploaded_file)
            if uploaded_file.name.endswith(".csv")
            else pd.read_excel(uploaded_file)
        )
        st.dataframe(df_subido.head())
        if st.button("✅ Confirmar e Importar"):
          st.session_state.db_pedidos = pd.concat(
              [st.session_state.db_pedidos, df_subido], ignore_index=True
          )
          st.success("¡Base integrada!")
          st.rerun()

  # -------------------------------------------------------------
  # C. ROL CLIENTE -> SEGUIMIENTO Y DASHBOARD PROPIO
  # -------------------------------------------------------------
  elif st.session_state.rol_actual == "🏢 Cliente":
    st.markdown("### 🏢 Portal de Clientes — Monitoreo de Envíos")

    # Métricas del cliente
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pedidos", len(st.session_state.db_pedidos))
    c2.metric("Entregados", "1")
    c3.metric("En Ruta", "1")

    st.markdown("#### Mis Pedidos Activos")
    st.dataframe(
        st.session_state.db_pedidos[[
            "FECHA_REGISTRO",
            "CODIGO INTERNO",
            "ESTADO",
            "NOMBRE",
            "DISTRITO",
            "EVIDENCIA",
        ]],
        use_container_width=True,
    )

  # -------------------------------------------------------------
  # D. ROL REPARTIDOR (VISTA MÓVIL APP)
  # -------------------------------------------------------------
  elif st.session_state.rol_actual == "🚚 Repartidor (App)":
    st.markdown("### 📱 App Repartidor — Lista de Hoja de Ruta")

    pedidos_driver = st.session_state.db_pedidos[
        st.session_state.db_pedidos["REPARTIDOR"] == "Juan Pérez"
    ]

    for idx, row in pedidos_driver.iterrows():
      st.markdown(
          f"""
            <div class="mobile-card">
                <h4 style="margin:0; color:#0F382C;">📦 {row['CODIGO INTERNO']} - {row['NOMBRE']}</h4>
                <p style="margin:5px 0; color:#334155;">📍 {row['DIRECCION']} ({row['DISTRITO']})</p>
                <p style="margin:0; color:#64748B;">Estado actual: <strong>{row['ESTADO']}</strong></p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      with st.expander(f"📷 Actualizar Entrega ({row['CODIGO INTERNO']})"):
        nuevo_estado = st.selectbox(
            "Resultado de visita:",
            ["ENTREGADO", "NO ENTREGADO / MOTIVADO"],
            key=f"st_{idx}",
        )
        foto = st.file_uploader(
            "Subir Foto / Evidencia", type=["png", "jpg"], key=f"foto_{idx}"
        )

        if st.button("Guardar Conformidad", key=f"btn_{idx}"):
          st.session_state.db_pedidos.at[idx, "ESTADO"] = nuevo_estado
          st.session_state.db_pedidos.at[idx, "SUB_ESTADO"] = (
              "ENTREGA EFECTIVA"
              if nuevo_estado == "ENTREGADO"
              else "DIRECCION INCORRECTA"
          )
          st.success("¡Registro actualizado desde la App!")
          st.rerun()
