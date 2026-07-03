import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN VISUAL DE LA PLATAFORMA (Identidad Corporativa)
st.set_page_config(page_title="Envíos Express Lima", page_icon="🚚", layout="wide")

# Diseño estético con CSS para imitar la interfaz premium de las imágenes
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
    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS EN MEMORIA (Para la simulación)
if 'db_logistica' not in st.session_state:
    st.session_state.db_logistica = pd.DataFrame([
        {"ID ENVÍO": "EE00124", "CLIENTE": "María Rodríguez", "ORIGEN": "Surco", "DESTINO": "Santa Anita", "ESTADO": "EN RUTA", "CONDUCTOR": "Juan Pérez", "EVIDENCIA": "Ninguna"},
        {"ID ENVÍO": "EE00123", "CLIENTE": "Inversiones Globales", "ORIGEN": "Callao", "DESTINO": "Ate", "ESTADO": "DELIVERED", "CONDUCTOR": "Luis Vargas", "EVIDENCIA": "Foto de fachada + Recibido por recepción"},
        {"ID ENVÍO": "EE00122", "CLIENTE": "Pedro Castillo", "ORIGEN": "Chorrillos", "DESTINO": "San Miguel", "ESTADO": "POR RECOGER", "CONDUCTOR": "Por Asignar", "EVIDENCIA": "Ninguna"}
    ])

# 3. MENÚ LATERAL PROFESIONAL
st.sidebar.markdown("<h2 style='text-align: center; color: #3B82F6;'>🚚 ENVÍOS<br>EXPRESS LIMA</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px;'>Lima Logistics v1.0</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

rol = st.sidebar.radio("🔑 SELECCIONA TU PORTAL:", [
    "👨‍💼 Portal Administrador (Tú)", 
    "🛵 Portal Repartidor (Celular)", 
    "📦 Portal Cliente (Seguimiento)"
])

# =====================================================================
# MODULO A: PORTAL ADMINISTRADOR
# =====================================================================
if rol == "👨‍💼 Portal Administrador (Tú)":
    st.markdown("<h1 style='color: #1E3A8A;'>TABLERO PRINCIPAL DE ADMINISTRACIÓN</h1>", unsafe_allow_html=True)
    
    # Indicadores superiores (Tal cual tus imágenes)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card-metrica"><div class="numero-metrica">28</div><div class="label-metrica">Envíos Hoy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-metrica"><div class="numero-metrica">12</div><div class="label-metrica">En Ruta</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card-metrica"><div class="numero-metrica">150</div><div class="label-metrica">Entregados</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pestañas limpias para organizar las tareas
    tab_lista, tab_carga = st.tabs(["📋 Lista de Envíos Recientes", "📥 Importación Masiva (Excel/CSV)"])
    
    with tab_lista:
        col_tabla, col_mapa = st.columns([2, 1])
        with col_tabla:
            st.dataframe(st.session_state.db_logistica, use_container_width=True)
        with col_mapa:
            st.markdown("<div style='background-color: #E2E8F0; padding: 40px; border-radius: 12px; text-align: center; color: #475569;'>🗺️ Mapas de Ruta Lima<br><span style='font-size: 12px;'>Área reservada para GPS de conductores</span></div>", unsafe_allow_html=True)

    with tab_carga:
        st.markdown("### Cargar Nuevos Pedidos del Día")
        # Generar plantilla descargable
        plantilla = pd.DataFrame(columns=["ID ENVÍO", "CLIENTE", "ORIGEN", "DESTINO", "CONDUCTOR"])
        csv_data = plantilla.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DESCARGAR PLANTILLA (.CSV)", data=csv_data, file_name="plantilla_express_lima.csv", mime="text/csv")
        
        st.markdown("---")
        archivo = st.file_uploader("Sube tu archivo Excel o CSV completado aquí", type=["csv"])
        if archivo is not None:
            try:
                nuevos_datos = pd.read_csv(archivo)
                nuevos_datos["ESTADO"] = "POR RECOGER"
                nuevos_datos["EVIDENCIA"] = "Ninguna"
                st.session_state.db_logistica = pd.concat([st.session_state.db_logistica, nuevos_datos], ignore_index=True)
                st.success("✔️ ¡Excelente! Los datos fueron importados y previsualizados con éxito en el Tablero Principal.")
                st.dataframe(nuevos_datos, use_container_width=True)
            except Exception as e:
                st.error("❌ Error de formato. Asegúrate de respetar los encabezados de la plantilla.")

# =====================================================================
# MODULO B: PORTAL REPARTIDOR (MÓVIL)
# =====================================================================
elif rol == "🛵 Portal Repartidor (Celular)":
    st.markdown("<h1 style='color: #1E3A8A;'>📱 APP REPARTIDOR</h1>", unsafe_allow_html=True)
    st.write("Registra entregas y evidencias en tiempo real desde tu ruta.")
    
    pedidos_pendientes = st.session_state.db_logistica[st.session_state.db_logistica["ESTADO"] != "DELIVERED"]
    
    if pedidos_pendientes.empty:
        st.success("🎉 ¡Gran trabajo! No tienes entregas pendientes en tu ruta.")
    else:
        id_selec = st.selectbox("Selecciona la Orden a Entregar:", pedidos_pendientes["ID ENVÍO"].tolist())
        datos_orden = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == id_selec].iloc[0]
        
        # Tarjeta informativa del cliente para el repartidor
        st.markdown(f"""
            <div style='background-color: #EFF6FF; padding: 20px; border-radius: 12px; border-left: 5px solid #2563EB;'>
                <b>📦 ID de Orden:</b> {datos_orden['ID ENVÍO']}<br>
                <b>👤 Destinatario:</b> {datos_orden['CLIENTE']}<br>
                <b>📍 Dirección de Entrega:</b> {datos_orden['DESTINO']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        foto = st.camera_input("📸 Capturar Foto de Evidencia (Fachada / Firma)")
        nota = st.text_input("Comentario o Notas del Conductor:")
        
        if st.button("✅ GUARDAR Y MARCAR COMO ENTREGADO"):
            idx = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == id_selec].index[0]
            st.session_state.db_logistica.at[idx, "ESTADO"] = "DELIVERED"
            st.session_state.db_logistica.at[idx, "EVIDENCIA"] = f"Foto cargada + Nota: '{nota}'" if foto else f"Sin foto + Nota: '{nota}'"
            st.success(f"✔️ ¡Orden {id_selec} actualizada con éxito en la base de datos central!")
            st.rerun()

# =====================================================================
# MODULO C: PORTAL CLIENTE (SEGUIMIENTO DE ENVÍOS)
# =====================================================================
else:
    st.markdown("<h1 style='color: #1E3A8A;'>📦 SEGUIMIENTO DE ENVÍOS</h1>", unsafe_allow_html=True)
    st.write("Consulta el estado de tu paquete en tiempo real.")
    
    buscar_id = st.text_input("Ingresa tu Código de Envío (Ej: EE00124):").strip().upper()
    
    if buscar_id:
        if buscar_id in st.session_state.db_logistica["ID ENVÍO"].values:
            resultado = st.session_state.db_logistica[st.session_state.db_logistica["ID ENVÍO"] == buscar_id].iloc[0]
            
            # Formatear el color del estado dinámicamente
            color_estado = "#10B981" if resultado["ESTADO"] == "DELIVERED" else "#F59E0B"
            
            st.markdown(f"""
                <div style='background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); border-top: 4px solid {color_estado};'>
                    <h3>Estado del Envío: <span style='color: {color_estado};'>{resultado['ESTADO']}</span></h3>
                    <p><b>Destino:</b> {resultado['DESTINO']}</p>
                    <p><b>Repartidor Asignado:</b> {resultado['CONDUCTOR']}</p>
                    <p><b>Detalles de Entrega / Evidencia:</b> {resultado['EVIDENCIA']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ No se encontró ningún envío registrado con ese código. Verifica el ID e intenta de nuevo.")
