import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN VISUAL DE LA PLATAFORMA (Identidad Corporativa de Alfa Cargo Express)
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide")

# Diseño estético con CSS personalizado
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #0F172A; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: bold;
        width: 100%;
    }
    .card-metrica {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        text-align: center;
        border: 1px solid #E2E8F0;
    }
    .numero-metrica { font-size: 36px; font-weight: bold; color: #1E3A8A; }
    .label-metrica { font-size: 14px; color: #64748B; font-weight: 600; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# 2. SISTEMA DE ALMACENAMIENTO DE DATOS (Simulación de Base de Datos)
if 'db_logistica' not in st.session_state:
    st.session_state.db_logistica = pd.DataFrame([
        {"ID ENVÍO": "ALFA-124", "CLIENTE": "María Rodríguez", "ORIGEN": "Surco", "DESTINO": "Santa Anita", "ESTADO": "EN RUTA", "CONDUCTOR": "Juan Pérez", "EVIDENCIA": "Ninguna"},
        {"ID ENVÍO": "ALFA-123", "CLIENTE": "Inversiones Globales", "ORIGEN": "Callao", "DESTINO": "Ate", "ESTADO": "DELIVERED", "CONDUCTOR": "Luis Vargas", "EVIDENCIA": "Código de barra verificado + Foto de fachada"},
        {"ID ENVÍO": "ALFA-122", "CLIENTE": "Pedro Castillo", "ORIGEN": "Chorrillos", "DESTINO": "San Miguel", "ESTADO": "POR RECOGER", "CONDUCTOR": "Por Asignar", "EVIDENCIA": "Ninguna"}
    ])

# Base de datos de usuarios registrados (Usuario: {Contraseña, Rol})
if 'usuarios_registrados' not in st.session_state:
    st.session_state.usuarios_registrados = {
        "admin": {"pass": "admin123", "rol": "👨‍💼 Portal Administrador"},
        "repartidor1": {"pass": "driver123", "rol": "🛵 Portal Repartidor"},
        "cliente1": {"pass": "cliente123", "rol": "📦 Portal Cliente"}
    }

# Control de sesión activa
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None
if 'rol_actual' not in st.session_state:
    st.session_state.rol_actual = None

# =====================================================================
# BARRA LATERAL (ALFA CARGO EXPRESS)
# =====================================================================
st.sidebar.markdown("<h2 style='text-align: center; color: #3B82F6;'>🚚 ALFA CARGO<br>EXPRESS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px;'>Logistics Management v1.1</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# =====================================================================
# SISTEMA DE LOGEO Y REGISTRO (PANTALLA DE ACCESO DE USUARIOS)
# =====================================================================
if st.session_state.usuario_actual is None:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🔒 Control de Acceso - Alfa Cargo Express</h1>", unsafe_allow_html=True)
    
    opcion_acceso = st.radio("¿Qué deseas hacer?", ["Iniciar Sesión", "Registrar Nuevo Usuario"], horizontal=True)
    
    col_form, _ = st.columns([1.5, 2])
    
    with col_form:
        if opcion_acceso == "Iniciar Sesión":
            st.subheader("Ingresa tus credenciales")
            input_user = st.text_input("Usuario:")
            input_pass = st.text_input("Contraseña:", type="password")
            
            if st.button("🔓 Entrar al Sistema"):
                if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                    st.session_state.usuario_actual = input_user
                    st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                    st.success(f"Bienvenido {input_user}")
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos.")
                    
        else:
            st.subheader("Formulario de Registro")
            nuevo_user = st.text_input("Crea un Nombre de Usuario:")
            nuevo_pass = st.text_input("Crea una Contraseña:", type="password")
            selec_rol = st.selectbox("Selecciona tu función en la empresa:", ["👨‍💼 Portal Administrador", "🛵 Portal Repartidor", "📦 Portal Cliente"])
            
            if st.button("📝 Completar Registro"):
                if nuevo_user.strip() == "" or nuevo_pass.strip() == "":
                    st.warning("⚠️ El usuario y la contraseña no pueden estar vacíos.")
                elif nuevo_user in st.session_state.usuarios_registrados:
                    st.error("❌ Este usuario ya existe. Elige otro nombre.")
                else:
                    st.session_state.usuarios_registrados[nuevo_user] = {"pass": nuevo_pass, "rol": selec_rol}
                    st.success("🎉 ¡Registro exitoso! Ahora puedes cambiar a 'Iniciar Sesión' con tus nuevos datos.")

# =====================================================================
# INTERFAZ UNA VEZ INICIADA LA SESIÓN
# =====================================================================
else:
    # Botón de Cerrar Sesión en la barra lateral
    st.sidebar.markdown(f"**Sesión:** {st.session_state.usuario_actual} ({st.session_state.rol_actual})")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_actual = None
        st.session_state.rol_actual = None
        st.rerun()

    # -----------------------------------------------------------------
    # MODULO A: INTERFAZ ADMINISTRADOR
    # -----------------------------------------------------------------
    if st.session_state.rol_actual == "👨‍💼 Portal Administrador":
        st.markdown("<h1 style='color: #1E3A8A;'>PANEL DE CONTROL ADMINISTRATIVO</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="card-metrica"><div class="numero-metrica">28</div><div class="label-metrica">Envíos Hoy</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card-metrica"><div class="numero-metrica">12</div><div class="label-metrica">En Ruta</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="card-metrica"><div class="numero-metrica">150</div><div class="label-metrica">Entregados</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        tab_lista, tab_carga = st.tabs(["📋 Monitoreo de Envíos", "📥 Carga Masiva (Excel/CSV)"])
        
        with tab_lista:
            st.dataframe(st.session_state.db_logistica, use_container_width=True)
            
        with tab_carga:
            st.markdown("### Importación Masiva para Alfa Cargo Express")
            plantilla = pd.DataFrame(columns=["ID ENVÍO", "CLIENTE", "ORIGEN", "DESTINO", "CONDUCTOR"])
            csv_data = plantilla.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DESCARGAR PLANTILLA (.CSV)", data=csv_data, file_name="plantilla_alfa.csv", mime="text/csv")
            
            archivo = st.file_uploader("Sube tu archivo CSV aquí", type=["csv"])
            if archivo is not None:
                nuevos_datos = pd.read_csv(archivo)
                nuevos_datos["ESTADO"] = "POR RECOGER"
                nuevos_datos["EVIDENCIA"] = "Ninguna"
                st.session_state.db_logistica = pd.concat([st.session_state.db_logistica, nuevos_datos], ignore_index=True)
                st.success("✔️ Pedidos cargados correctamente al sistema central.")
                st.dataframe(nuevos_datos, use_container_width=True)

    # -----------------------------------------------------------------
    # MODULO B: INTERFAZ REPARTIDOR (MÓVIL + ESCANER)
    # -----------------------------------------------------------------
    elif st.session_state.rol_actual == "🛵 Portal Repartidor":
        st.markdown("<h1 style='color: #1E3A8A;'>📱 RUTA DEL REPARTIDOR</h1>", unsafe_allow_html=True)
        
        pedidos_pendientes = st.session_state.db_logistica[st.session_state.db_logistica["ESTADO"] != "DELIVERED"]
        
        if pedidos_pendientes.empty:
            st.success("🎉 ¡Felicidades! Completaste todas tus entregas asignadas.")
        else:
            id_selec = st.selectbox("Selecciona la Orden a procesar:", pedidos_pendientes["ID ENVÍO"].tolist())
            datos_orden = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == id_selec].iloc[0]
            
            st.markdown(f"""
                <div style='background-color: #EFF6FF; padding: 20px; border-radius: 12px; border-left: 5px solid #2563EB;'>
                    <b>📦 Código de Envío:</b> {datos_orden['ID ENVÍO']}<br>
                    <b>👤 Destinatario:</b> {datos_orden['CLIENTE']}<br>
                    <b>📍 Destino:</b> {datos_orden['DESTINO']}
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Opción Obligatoria de Escaneo solicitada
            st.subheader("📷 1. Escaneo de Código de Barras")
            scan_code = st.camera_input("Enfoca el código de barras del producto físico:")
            
            st.subheader("📸 2. Evidencia Adicional de Entrega")
            nota = st.text_input("Notas o comentarios adicionales:")
            
            if st.button("✅ REGISTRAR ENTREGA Y ESCANEO"):
                if scan_code is None:
                    st.error("⚠️ Para marcar como entregado es obligatorio activar la cámara y escanear/capturar el código de barra.")
                else:
                    idx = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == id_selec].index[0]
                    st.session_state.db_logistica.at[idx, "ESTADO"] = "DELIVERED"
                    st.session_state.db_logistica.at[idx, "EVIDENCIA"] = f"Código verificado por escáner. Nota: '{nota}'"
                    st.success(f"✔️ ¡Orden {id_selec} confirmada mediante código de barras!")
                    st.rerun()

    # -----------------------------------------------------------------
    # MODULO C: INTERFAZ CLIENTE
    # -----------------------------------------------------------------
    else:
        st.markdown("<h1 style='color: #1E3A8A;'>📦 PORTAL DE SEGUIMIENTO (CLIENTES)</h1>", unsafe_allow_html=True)
        st.write("Consulta el estado logístico de tus encomiendas con Alfa Cargo Express.")
        
        buscar_id = st.text_input("Introduce tu código de rastreo (Ej: ALFA-124):").strip().upper()
        
        if buscar_id:
            if buscar_id in st.session_state.db_logistica["ID ENVÍO"].values:
                resultado = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == buscar_id].iloc[0]
                color_estado = "#10B981" if resultado["ESTADO"] == "DELIVERED" else "#F59E0B"
                
                st.markdown(f"""
                    <div style='background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); border-top: 4px solid {color_estado};'>
                        <h3>Estado Actual: <span style='color: {color_estado};'>{resultado['ESTADO']}</span></h3>
                        <p><b>Ruta de Entrega:</b> {resultado['ORIGEN']} ➡️ {resultado['DESTINO']}</p>
                        <p><b>Verificación del sistema:</b> {resultado['EVIDENCIA']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Código de rastreo no encontrado en Alfa Cargo Express.")
