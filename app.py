import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS PROFESIONALES (Inspirados en iMile / DHL)
st.markdown("""
    <style>
    /* Fondo general gris azulado suave */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Ocultar barra lateral si no hay sesión iniciada para aprovechar el ancho */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    
    /* Pila de valores corporativos */
    .hero-title {
        color: #1E3A8A;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 20px;
    }
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 25px;
    }
    .value-item {
        color: #334155;
        font-weight: 600;
        font-size: 15px;
        display: flex;
        align-items: center;
    }
    .value-item::before {
        content: "▌";
        color: #2563EB;
        font-weight: bold;
        margin-right: 8px;
    }
    
    /* Tarjeta de Login (Derecha) */
    div[data-testid="stVerticalBlock"] > div.login-box {
        background-color: #FFFFFF;
        padding: 35px 30px;
        border-radius: 16px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
    }
    
    /* Ajustes para que las etiquetas de los inputs sean oscuras y legibles */
    .stTextInput label {
        color: #1E293B !important;
        font-weight: 600 !important;
    }
    
    /* Botón azul corporativo */
    .stButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
    }
    
    /* Footer de derechos de autor */
    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS Y ESTADOS
if 'db_logistica' not in st.session_state:
    st.session_state.db_logistica = pd.DataFrame([
        {"ID ENVÍO": "ALFA-124", "CLIENTE": "María Rodríguez", "ORIGEN": "Surco", "DESTINO": "Santa Anita", "ESTADO": "EN RUTA", "CONDUCTOR": "Juan Pérez", "EVIDENCIA": "Ninguna"},
        {"ID ENVÍO": "ALFA-123", "CLIENTE": "Inversiones Globales", "ORIGEN": "Callao", "DESTINO": "Ate", "ESTADO": "DELIVERED", "CONDUCTOR": "Luis Vargas", "EVIDENCIA": "Código de barra verificado + Foto de fachada"}
    ])

if 'usuarios_registrados' not in st.session_state:
    st.session_state.usuarios_registrados = {
        "admin": {"pass": "admin123", "rol": "👨‍💼 Portal Administrador"}
    }

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None
if 'rol_actual' not in st.session_state:
    st.session_state.rol_actual = None

# 4. PANTALLA PRINCIPAL DE LOGIN (DISTRIBUCIÓN 2 COLUMNAS)
if st.session_state.usuario_actual is None:
    
    # Encabezado con Logo / Nombre
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 20px 30px 20px;'>
            <div style='font-size: 24px; font-weight: 900; color: #1E3A8A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #64748B; font-size: 14px; font-weight: 500;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_space, col_right = st.columns([1.3, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA (MARCA & ILUSTRACIÓN) ---
    with col_left:
        st.markdown('<div class="hero-title">Excelencia Logística y Compromiso Total</div>', unsafe_allow_html=True)
        
        # Cuadrícula de valores corporativos
        st.markdown("""
            <div class="value-grid">
                <div class="value-item">Tiempos Récord de Entrega</div>
                <div class="value-item">Trazabilidad en Tiempo Real</div>
                <div class="value-item">Seguridad Garantizada</div>
                <div class="value-item">Cobertura Lima y Provincias</div>
                <div class="value-item">Confirmación por Escáner</div>
                <div class="value-item">Soporte Corporativo 24/7</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Imagen / Ilustración Logística
        st.image("https://img.freepik.com/free-vector/isometric-logistics-flowchart-with_1284-25532.jpg", use_container_width=True)

    # --- COLUMNA DERECHA (FORMULARIO EN TARJETA) ---
    with col_right:
        with st.container():
            st.markdown("<h2 style='text-align: center; color: #0F172A; font-size: 24px; font-weight: 700; margin-bottom: 5px;'>Bienvenido</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #64748B; font-size: 14px; margin-bottom: 25px;'>Ingresa a la plataforma corporativa</p>", unsafe_allow_html=True)
            
            input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
            input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Iniciar Sesión"):
                if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                    st.session_state.usuario_actual = input_user
                    st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")
            
            st.markdown("""
                <div class="login-footer">
                    © 2026 Alfa Cargo Express S.A.C.<br>Todos los derechos reservados.
                </div>
            """, unsafe_allow_html=True)

# 5. SESIÓN INICIADA (SISTEMA CENTRAL)
else:
    st.sidebar.markdown(f"**Usuario:** {st.session_state.usuario_actual}")
    st.sidebar.markdown(f"**Rol:** {st.session_state.rol_actual}")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_actual = None
        st.session_state.rol_actual = None
        st.rerun()
        
    st.markdown(f"# {st.session_state.rol_actual}")
    st.dataframe(st.session_state.db_logistica, use_container_width=True)
