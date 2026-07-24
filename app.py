import base64
from datetime import datetime, date, timedelta
import os
import textwrap
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Alfa Cargo Express - Admin",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

# CSS GENERAL Y CORRECCIÓN DE MENÚS Y LABELS
st.markdown(
    """
    <style>
    html, body, .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #CBD5E1 !important; }
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] { padding-top: 1rem !important; }
    [data-testid="stSidebarHeader"] { display: none !important; }
    
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stElementToolbar"] { display: none !important; }
    
    .block-container { max-width: 96% !important; padding-top: 1rem !important; padding-bottom: 2rem !important; }
    
    div[data-baseweb="select"] > div { background-color: #FFFFFF !important; border-color: #0F382C !important; border-width: 2px !important; }
    div[data-baseweb="select"] *, div[data-baseweb="select"] input, div[data-baseweb="select"] span { color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; }
    
    .stTextInput input { background-color: #FFFFFF !important; color: #0F172A !important; border: 2px solid #0F382C !important; border-radius: 8px !important; padding: 6px 10px !important; }

    div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button { 
        background-color: #FFFFFF !important;  
        border: 2px solid #0F382C !important;
        border-radius: 8px !important; 
        font-weight: 600 !important; 
    }
    div[data-testid="stButton"] > button div, div[data-testid="stButton"] > button span, div[data-testid="stButton"] > button p { color: #0F382C !important; }
    div[data-testid="stButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover { background-color: #0F382C !important; }
    div[data-testid="stButton"] > button:hover div, div[data-testid="stButton"] > button:hover span { color: #FFFFFF !important; }

    .contenedor-btn-custom button { background-color: #FFFFFF !important; border: 2px solid #0F382C !important; border-radius: 8px !important; }
    .contenedor-btn-custom button div, .contenedor-btn-custom button span { color: #0F382C !important; font-weight: 700 !important; }
    .contenedor-btn-custom button:hover { background-color: #0F382C !important; }
    .contenedor-btn-custom button:hover div, .contenedor-btn-custom button:hover span { color: #FFFFFF !important; }

    .tabla-contenedor-logs {
        max-height: 530px;
        height: fit-content;
        overflow-y: auto;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 10px !important;
    }

    .tabla-usuarios {
        width: 100% !important;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
    }
    .tabla-usuarios th {
        background-color: #0F382C;
        color: #FFFFFF !important;
        padding: 10px 12px;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 700;
    }
    .tabla-usuarios td {
        padding: 9px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
    }
    .tabla-usuarios tr:hover { background-color: #F1F5F9; }

    [data-testid="stForm"] { background-color: #FFFFFF !important; border-radius: 14px !important; border: 1px solid #E2E8F0 !important; padding: 28px !important; border-top: 6px solid #0F382C !important; }
    div[data-testid="stFormSubmitButton"] > button { background-color: #0F382C !important; border-radius: 8px !important; border: none !important; width: 100% !important; }
    div[data-testid="stFormSubmitButton"] > button p { color: #FFFFFF !important; font-weight: 700 !important; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; gap: 28px !important; border-bottom: 2px solid #CBD5E1 !important; }
    .stTabs [data-baseweb="tab"] p { color: #64748B !important; font-weight: 500 !important; font-size: 15px !important; }
    .stTabs [aria-selected="true"] p { color: #0F382C !important; font-weight: 700 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# DATOS INICIALES Y POLÍTICA DE 90 DÍAS
if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = pd.DataFrame([
        {"USUARIO": "admin", "PASS": "admin123", "ROL": "👨‍💼 Portal Administrador", "ESTADO": "Activo", "ÚLTIMA CONEXIÓN": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"USUARIO": "operador1", "PASS": "123", "ROL": "🛠️ Operario", "ESTADO": "Activo", "ÚLTIMA CONEXIÓN": "Nunca"},
    ])

if "df_pedidos" not in st.session_state:
    lista_inicial = []
    for i in range(1, 70):
        dias_atras = i % 85 
        f_reg = (datetime.now() - timedelta(days=dias_atras)).strftime("%d/%m/%Y")
        lista_inicial.append({
            "FECHA_REGISTRO": f_reg, 
            "CODIGO INTERNO": f"BLC1-{48000+i}", 
            "CLIENTE": "UNIMARKET" if i % 2 == 0 else "ALICORP", 
            "ESTADO": "ENTREGADO" if i % 3 == 0 else "EN RUTA", 
            "SUB_ESTADO": "EFECTIVA" if i % 3 == 0 else "PENDIENTE", 
            "NOMBRE": f"CLIENTE {i}", 
            "DISTRITO": "LIMA", 
            "TIPO_SERVICIO": "SAME-DAY"
        })
    st.session_state.df_pedidos = pd.DataFrame(lista_inicial)

# APLICACIÓN DE LA REGLA DE 90 DÍAS (ELIMINACIÓN AUTOMÁTICA)
if not st.session_state.df_pedidos.empty and "FECHA_REGISTRO" in st.session_state.df_pedidos.columns:
    st.session_state.df_pedidos["_fecha_dt"] = pd.to_datetime(
        st.session_state.df_pedidos["FECHA_REGISTRO"], format="%d/%m/%Y", errors="coerce"
    )
    limite_90_dias = datetime.now() - timedelta(days=90)
    st.session_state.df_pedidos = st.session_state.df_pedidos[
        st.session_state.df_pedidos["_fecha_dt"] >= limite_90_dias
    ].drop(columns=["_fecha_dt"])

if "historial_acciones" not in st.session_state:
    st.session_state.historial_acciones = pd.DataFrame([{
        "FECHA Y HORA": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "USUARIO": "admin",
        "ACCIÓN": "Inicio de sistema"
    }])

if "pagina_actual_tabla" not in st.session_state:
    st.session_state.pagina_actual_tabla = 1

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

@st.dialog("📌 Soporte y Recuperación de Credenciales")
def mostrar_modal_soporte():
    st.markdown("""
    <div style="color: #FFFFFF !important; line-height: 1.6;">
        <p style="color: #FFFFFF !important; font-size: 15px; margin-bottom: 15px;">
            La asignación y restablecimiento de contraseñas es gestionada por el área de Administración.
        </p>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">💬 <b>WhatsApp:</b> +51 987 654 321</div>
        <div style="color: #FFFFFF !important; font-size: 14px; margin-bottom: 8px;">✉️ <b>Correo:</b> soporte@alfacargo.pe</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Entendido", use_container_width=True): st.rerun()

@st.dialog("➕ Añadir Registro de Pedido")
def modal_add_pedido():
    with st.form("add_p"):
        c1, c2 = st.columns(2)
        cod = c1.text_input("Código Interno")
        cli = c2.text_input("Cliente")
        nom = st.text_input("Nombre Destinatario")
        est = st.selectbox("Estado", ["ENTREGADO", "EN RUTA", "PENDIENTE"])
        if st.form_submit_button("Guardar Pedido", use_container_width=True):
            nuevo = pd.DataFrame([{
                "FECHA_REGISTRO": datetime.now().strftime("%d/%m/%Y"), 
                "CODIGO INTERNO": cod, "CLIENTE": cli, "ESTADO": est, 
                "SUB_ESTADO": "REGISTRADO", "NOMBRE": nom, "DISTRITO": "LIMA", "TIPO_SERVICIO": "SAME-DAY"
            }])
            st.session_state.df_pedidos = pd.concat([st.session_state.df_pedidos, nuevo], ignore_index=True)
            registrar_log(f"Añadió pedido {cod}")
            st.rerun()

@st.dialog("📤 Subir Data Masiva")
def modal_upload():
    file = st.file_uploader("Selecciona archivo Excel o CSV", type=["xlsx", "csv"])
    if file and st.button("Procesar y Cargar"):
        registrar_log("Subida de archivo masivo")
        st.rerun()

# FLUJO DE LOGIN
if st.session_state.usuario_actual is None:
    st.markdown('<div style="font-size: 28px; font-weight: 900; color: #0F382C; margin-bottom: 20px;">🌲 ALFA CARGO EXPRESS</div>', unsafe_allow_html=True)
    col_left, col_right = st.columns([1.2, 1.0], gap="large")
    with col_left:
        st.markdown('<div style="color: #0F172A; font-size: 22px; font-weight: 700; margin-bottom: 15px;">Módulo de Administración del Sistema</div>', unsafe_allow_html=True)
        img_b64 = obtener_imagen_github("alfa_warehouse.jpg")
        if img_b64:
            st.markdown(f'<img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; max-height: 260px; object-fit: contain; border-radius: 12px;" />', unsafe_allow_html=True)
    with col_right:
        with st.form("login_form"):
            st.markdown('<h3 style="text-align: center; color: #0F382C; font-weight:800; margin-bottom: 20px;">Bienvenido</h3>', unsafe_allow_html=True)
            input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
            input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
            remember = st.checkbox("Recordar inicio de sesión", value=True)
            if st.form_submit_button("Ingresar al Portal"):
                df_users = st.session_state.usuarios_registrados
                user_match = df_users[(df_users["USUARIO"] == input_user) & (df_users["PASS"] == input_pass)]
                if not user_match.empty:
                    st.session_state.usuario_actual = input_user
                    st.session_state.rol_actual = user_match.iloc[0]["ROL"]
                    if remember:
                        st.query_params["saved_user"] = input_user
                        st.query_params["saved_rol"] = st.session_state.rol_actual
                    registrar_log("Inicio de sesión exitoso")
                    st.rerun()
        if st.button("❓ ¿Necesitas ayuda con tu acceso?", use_container_width=True):
            mostrar_modal_soporte()
else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(f"""
            <div style="font-size: 22px; font-weight: 800; color: #0F382C;">🌲 ALFA CARGO EXPRESS — Portal {st.session_state.rol_actual}</div>
            <div style="font-size: 13px; color: #475569; font-weight: 600;">Usuario activo: <strong>{st.session_state.usuario_actual}</strong></div>
        """, unsafe_allow_html=True)
    with col_nav2:
        if st.button("🚪 Cerrar Sesión", key="logout"):
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.query_params.clear()
            st.rerun()

    st.markdown("<hr style='margin: 8px 0px; border-color: #CBD5E1;'>", unsafe_allow_html=True)

    # ==========================================
    # VISTA OPERARIO
    # ==========================================
    if st.session_state.rol_actual == "🛠️ Operario":
        csv = st.session_state.df_pedidos.to_csv(index=False).encode('utf-8')
        st.markdown("<h3 style='margin:0 0 8px 0;'>Gestión de Envíos <span style='font-size:12px; color:#64748B;'>(Retención automática de 90 días)</span></h3>", unsafe_allow_html=True)
        
        _, col_b1, col_b2, col_b3 = st.columns([2.5, 0.9, 0.9, 0.9])
        with col_b1:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            st.download_button("📥 Descargar", data=csv, file_name="pedidos.csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b2:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("📤 Cargar Data", use_container_width=True): modal_upload()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b3:
            st.markdown('<div class="contenedor-btn-custom">', unsafe_allow_html=True)
            if st.button("➕ Nuevo Pedido", use_container_width=True): modal_add_pedido()
            st.markdown('</div>', unsafe_allow_html=True)

        # SIDEBAR CON MÁSCARA AUTOMÁTICA DD/MM/YYYY
        with st.sidebar:
            st.markdown("<h2 style='color: #0F382C; font-size: 22px; font-weight: 800; margin: 0px 0px 4px 0px;'>🌲 ALFA EXPRESS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; color: #64748B; margin-top: 0px; margin-bottom: 14px;'>Filtra los registros de envíos de manera rápida.</p>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 0px 0px 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0F382C; margin:0 0 6px 0;'>📅 Rango de Fechas (DD/MM/YYYY):</p>", unsafe_allow_html=True)
            txt_fecha_inicio = st.text_input("Fecha Inicial", value="", placeholder="DD/MM/YYYY", key="f_ini")
            txt_fecha_fin = st.text_input("Fecha Final", value="", placeholder="DD/MM/YYYY", key="f_fin")

            # Script JavaScript para la máscara automática en los inputs de fecha
            components.html("""
                <script>
                const doc = window.parent.document;
                function aplicarMascaraLimpia(input) {
                    if (!input.dataset.masked) {
                        input.dataset.masked = "true";
                        input.setAttribute("maxlength", "10");
                        
                        input.addEventListener("input", function(e) {
                            let val = this.value.replace(/\\D/g, "");
                            if (val.length > 8) val = val.slice(0, 8);
                            
                            let res = "";
                            if (val.length > 0) res += val.substring(0, 2);
                            if (val.length >= 3) res += "/" + val.substring(2, 4);
                            if (val.length >= 5) res += "/" + val.substring(4, 8);

                            if (this.value !== res) {
                                this.value = res;
                                this.dispatchEvent(new Event('input', { bubbles: true }));
                            }
                        });
                    }
                }
                function observarInputs() {
                    doc.querySelectorAll('input').forEach(input => {
                        if (input.getAttribute('placeholder') === 'DD/MM/YYYY') {
                            aplicarMascaraLimpia(input);
                        }
                    });
                }
                setInterval(observarInputs, 300);
                </script>
            """, height=0)

            st.markdown("<hr style='margin: 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0F382C; margin:0 0 6px 0;'>🔍 Búsqueda por Texto:</p>", unsafe_allow_html=True)
            filtro_codigo_txt = st.text_input("Código Interno", placeholder="Ej: BLC1-480...", key="b_cod")
            filtro_nombre_txt = st.text_input("Nombre Destinatario", placeholder="Ej: Cliente...", key="b_nom")

            st.markdown("<hr style='margin: 14px 0px;'>", unsafe_allow_html=True)

            st.markdown("<p style='font-weight:700; font-size:14px; color:#0F382C; margin:0 0 6px 0;'>📌 Selección Múltiple:</p>", unsafe_allow_html=True)
            clientes_unicos = sorted(st.session_state.df_pedidos["CLIENTE"].astype(str).unique().tolist())
            filtro_cliente = st.multiselect("Cliente", options=clientes_unicos, placeholder="Todos")

        # FILTRADO DE DATOS
        df_filtrado = st.session_state.df_pedidos.copy()
        if "FECHA_REGISTRO" in df_filtrado.columns:
            df_filtrado["_fecha_temp"] = pd.to_datetime(df_filtrado["FECHA_REGISTRO"], format="%d/%m/%Y", errors="coerce")
            
            f_ini_parsed = None
            f_fin_parsed = None

            if txt_fecha_inicio.strip():
                try: f_ini_parsed = datetime.strptime(txt_fecha_inicio.strip(), "%d/%m/%Y").date()
                except ValueError: pass

            if txt_fecha_fin.strip():
                try: f_fin_parsed = datetime.strptime(txt_fecha_fin.strip(), "%d/%m/%Y").date()
                except ValueError: pass

            if f_ini_parsed and f_fin_parsed:
                df_filtrado = df_filtrado[(df_filtrado["_fecha_temp"].dt.date >= f_ini_parsed) & (df_filtrado["_fecha_temp"].dt.date <= f_fin_parsed)]
            elif f_ini_parsed and not f_fin_parsed:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date == f_ini_parsed]
            elif not f_ini_parsed and f_fin_parsed:
                df_filtrado = df_filtrado[df_filtrado["_fecha_temp"].dt.date <= f_fin_parsed]

            df_filtrado = df_filtrado.drop(columns=["_fecha_temp"])

        if filtro_cliente: df_filtrado = df_filtrado[df_filtrado["CLIENTE"].astype(str).isin(filtro_cliente)]
        if filtro_codigo_txt: df_filtrado = df_filtrado[df_filtrado["CODIGO INTERNO"].astype(str).str.contains(filtro_codigo_txt, case=False, na=False)]
        if filtro_nombre_txt: df_filtrado = df_filtrado[df_filtrado["NOMBRE"].astype(str).str.contains(filtro_nombre_txt, case=False, na=False)]

        if "FECHA_REGISTRO" in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values(by="FECHA_REGISTRO", ascending=False)

        # ==========================================
        # PAGINACIÓN AUTOMÁTICA DE 50 EN 50
        # ==========================================
        TAMANO_PAGINA = 50
        total_registros = len(df_filtrado)
        total_paginas = max(1, (total_registros + TAMANO_PAGINA - 1) // TAMANO_PAGINA)

        if st.session_state.pagina_actual_tabla > total_paginas:
            st.session_state.pagina_actual_tabla = total_paginas

        col_inf1, col_inf2, col_inf3, col_inf4 = st.columns([3.5, 1.2, 0.4, 0.4])
        
        inicio_idx = (st.session_state.pagina_actual_tabla - 1) * TAMANO_PAGINA
        fin_idx = min(inicio_idx + TAMANO_PAGINA, total_registros)
        rango_texto = f"{inicio_idx + 1}-{fin_idx} de {total_registros}" if total_registros > 0 else "0 de 0"

        with col_inf1:
            st.markdown(f"<p style='color: #475569; font-size: 14px; margin-top: 8px;'>Registros mostrados: <b>{rango_texto}</b> (Bloques automáticos de 50)</p>", unsafe_allow_html=True)
        with col_inf2:
            st.markdown(f"<p style='text-align: right; color: #475569; font-size: 14px; margin-top: 8px;'>Pág. {st.session_state.pagina_actual_tabla} de {total_paginas}</p>", unsafe_allow_html=True)
        with col_inf3:
            if st.button("〈", use_container_width=True, disabled=(st.session_state.pagina_actual_tabla <= 1)):
                st.session_state.pagina_actual_tabla -= 1
                st.rerun()
        with col_inf4:
            if st.button("〉", use_container_width=True, disabled=(st.session_state.pagina_actual_tabla >= total_paginas)):
                st.session_state.pagina_actual_tabla += 1
                st.rerun()

        df_paginado = df_filtrado.iloc[inicio_idx:fin_idx]
        columnas_pedidos = df_paginado.columns.tolist()

        filas_pedidos_html = ""
        for _, fila in df_paginado.iterrows():
            filas_pedidos_html += "<tr>"
            for col in columnas_pedidos:
                filas_pedidos_html += f"<td>{fila[col]}</td>"
            filas_pedidos_html += "</tr>"

        tabla_pedidos_html = textwrap.dedent(f"""
            <div class="tabla-contenedor-logs">
                <table class="tabla-usuarios">
                    <thead>
                        <tr>{"".join([f"<th>{col}</th>" for col in columnas_pedidos])}</tr>
                    </thead>
                    <tbody>
                        {filas_pedidos_html if not df_paginado.empty else "<tr><td colspan='100%' style='text-align:center;'>No se encontraron registros activos en los últimos 90 días</td></tr>"}
                    </tbody>
                </table>
            </div>
            """).strip()

        st.markdown(tabla_pedidos_html, unsafe_allow_html=True)

    # ==========================================
    # VISTA ADMINISTRADOR
    # ==========================================
    else:
        tab1, tab2 = st.tabs(["Usuarios y Claves", "Auditoría (Logs)"])
        with tab1:
            st.subheader("👥 Gestión de Usuarios")
            st.dataframe(st.session_state.usuarios_registrados, use_container_width=True)
        with tab2:
            st.subheader("📋 Auditoría de Acciones")
            st.dataframe(st.session_state.historial_acciones, use_container_width=True)
