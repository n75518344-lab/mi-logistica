import base64
from datetime import datetime
import os
import textwrap
import pandas as pd
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express - Portal Operaciones",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# REVISAR SESIÓN
query_params = st.query_params

if "usuario_actual" not in st.session_state:
  if "saved_user" in query_params:
    st.session_state.usuario_actual = query_params["saved_user"]
    st.session_state.rol_actual = query_params.get("saved_rol", "🛠️ Operario")
  else:
    st.session_state.usuario_actual = "operador1"  # Para pruebas directas
    st.session_state.rol_actual = "🛠️ Operario"

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

    /* CONTENEDORES CON SCROLL INTELIGENTE PARA TABLAS */
    .tabla-contenedor {
        max-height: 480px;
        height: fit-content;
        overflow-y: auto;
        overflow-x: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* BARRA DE SCROLL MODERNA Y FINITA */
    .tabla-contenedor::-webkit-scrollbar {
        width: 6px !important;
        height: 6px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-track {
        background: transparent !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb {
        background-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }

    .tabla-contenedor::-webkit-scrollbar-thumb:hover {
        background-color: #94A3B8 !important;
    }

    /* ESTILOS DE TABLA OPERATIVA */
    .tabla-pedidos {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
    }
    .tabla-pedidos th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 10px 12px;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 700;
        white-space: nowrap;
    }
    .tabla-pedidos td {
        padding: 8px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
        white-space: nowrap;
    }
    .tabla-pedidos tr:hover {
        background-color: #F1F5F9;
    }

    /* INPUTS Y SELECTBOX */
    .stTextInput input, div[data-baseweb="select"] > div { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
    }

    /* BOTONES */
    div[data-testid="stButton"] > button { 
        background-color: #0F382C !important; 
        color: #FFFFFF !important;
        border-radius: 8px !important; 
        font-weight: 600 !important;
        border: none !important;
    }

    #logout_btn button {
        background-color: #FEE2E2 !important;
        border: 1px solid #FCA5A5 !important;
    }
    #logout_btn button p { color: #991B1B !important; font-weight: 700 !important; }

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

    /* PESTAÑAS MINIMALISTAS */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: transparent !important; 
        gap: 20px !important; 
        border-bottom: 2px solid #CBD5E1 !important; 
    }
    .stTabs [data-baseweb="tab"] p { 
        color: #64748B !important; 
        font-weight: 600 !important; 
    }
    .stTabs [aria-selected="true"] { 
        border-bottom: 3px solid #0F382C !important; 
    }
    .stTabs [aria-selected="true"] p { 
        color: #0F382C !important; 
        font-weight: 800 !important; 
    }
    </style>
""",
    unsafe_allow_html=True,
)

# DATA DE PRUEBA OPERATIVA
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

# CABECERA OPERATIVA GENERAL
col_h1, col_h2 = st.columns([5, 1])
with col_h1:
  st.markdown(
      f"""
    <div style="font-size: 22px; font-weight: 900; color: #0F382C; margin-bottom: 0px;">🌲 ALFA CARGO EXPRESS — Portal Operaciones</div>
    <div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 5px;">Operador Activo: <strong>{st.session_state.usuario_actual}</strong> | Central Almacén Lima</div>
    """,
      unsafe_allow_html=True,
  )
with col_h2:
  st.markdown('<div id="logout_btn">', unsafe_allow_html=True)
  if st.button("🚪 Cerrar Sesión", key="logout"):
    st.session_state.usuario_actual = None
    st.rerun()
  st.markdown("</div>", unsafe_allow_html=True)

# PESTAÑAS PRINCIPALES DEL OPERADOR
tab_dash, tab_pedidos, tab_carga = st.tabs(
    ["📊 Panel de Control", "📦 Gestión de Pedidos", "📥 Cargar Data"]
)

# -------------------------------------------------------------
# TAB 1: PANEL DE CONTROL (MÉTRICAS RÁPIDAS)
# -------------------------------------------------------------
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
        f'<div class="kpi-card"><div class="kpi-title">EN ALMACÉN</div><div'
        f' class="kpi-value" style="color:#DC2626;">{pendientes}</div></div>',
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)
  st.subheader("Avance de Ruta del Día")
  st.bar_chart(df["ESTADO"].value_counts())

# -------------------------------------------------------------
# TAB 2: GESTIÓN DE PEDIDOS Y DETALLE INTERACTIVO
# -------------------------------------------------------------
with tab_pedidos:
  col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 1, 1])

  with col_filtro1:
    buscar = st.text_input(
        "🔍 Buscar por Cliente, Código, Nombre o Distrito:",
        placeholder="Ej: UNIMARKET / ATE / Tramontina",
    )
  with col_filtro2:
    filtro_estado = st.selectbox(
        "Filtrar por Estado:",
        ["TODOS", "ENTREGADO", "EN RUTA", "PENDIENTE"],
    )
  with col_filtro3:
    filtro_cliente = st.selectbox(
        "Filtrar por Cliente:",
        ["TODOS"] + list(st.session_state.pedidos_df["CLIENTE"].unique()),
    )

  # APLICAR FILTROS
  df_filtrado = st.session_state.pedidos_df.copy()

  if buscar:
    df_filtrado = df_filtrado[
        df_filtrado.apply(
            lambda row: row.astype(str)
            .str.contains(buscar, case=False)
            .any(),
            axis=1,
        )
    ]

  if filtro_estado != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["ESTADO"] == filtro_estado]

  if filtro_cliente != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["CLIENTE"] == filtro_cliente]

  col_tabla, col_detalle = st.columns([1.8, 1.2], gap="medium")

  with col_tabla:
    st.markdown(
        "**Lista de Pedidos** *(Selecciona uno abajo para ver la ficha"
        " completa)*"
    )

    # GENERAR TABLA HTML PERSONALIZADA
    filas_html = ""
    for idx, row in df_filtrado.iterrows():
      badge_color = (
          "#16A34A"
          if row["ESTADO"] == "ENTREGADO"
          else ("#D97706" if row["ESTADO"] == "EN RUTA" else "#DC2626")
      )

      filas_html += f"""
            <tr>
                <td><b>{row['FECHA_REGISTRO']}</b></td>
                <td><b>{row['CODIGO_INTERNO']}</b></td>
                <td>{row['CLIENTE']}</td>
                <td><span style="color: {badge_color}; font-weight: bold;">{row['ESTADO']}</span></td>
                <td>{row['NOMBRE']}</td>
                <td>{row['DISTRITO']}</td>
            </tr>
            """

    tabla_html = f"""
        <div class="tabla-contenedor">
            <table class="tabla-pedidos">
                <thead>
                    <tr>
                        <th>FECHA</th>
                        <th>CÓDIGO</th>
                        <th>CLIENTE</th>
                        <th>ESTADO</th>
                        <th>DESTINATARIO</th>
                        <th>DISTRITO</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_html}
                </tbody>
            </table>
        </div>
        """
    st.markdown(tabla_html, unsafe_allow_html=True)

  with col_detalle:
    st.markdown("**📌 Ficha y Evidencia de Pedido**")

    # SELECTOR DE PEDIDO A DETALLAR
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

      # SIMULACIÓN DE FOTO POD/EVIDENCIA
      st.image(
          "https://via.placeholder.com/350x180.png?text=FOTO+EVIDENCIA+GUIA+FIRMADA",
          caption=f"Evidencia registrada para {registro['CODIGO_INTERNO']}",
          use_container_width=True,
      )
    else:
      st.warning("No hay pedidos coincidentes con los filtros.")

# -------------------------------------------------------------
# TAB 3: CARGA DE DATA (EXCEL / CSV)
# -------------------------------------------------------------
with tab_carga:
  st.subheader("📥 Cargar Matriz de Envíos Masivos")
  st.markdown(
      "Sube el archivo Excel o CSV proporcionado por el cliente para procesar"
      " las guías."
  )

  uploaded_file = st.file_uploader(
      "Selecciona el archivo Excel/CSV", type=["xlsx", "csv"]
  )

  if uploaded_file is not None:
    try:
      if uploaded_file.name.endswith(".csv"):
        df_nuevo = pd.read_csv(uploaded_file)
      else:
        df_nuevo = pd.read_excel(uploaded_file)

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
