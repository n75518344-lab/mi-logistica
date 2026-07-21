import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN VISUAL (Identidad Corporativa Alfa Cargo Express)
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide")

# ESTILOS CSS - LIMPION Y CORPORATIVO
st.markdown("""
    <style>
    /* Fondo general gris tenue */
    .stApp {
        background-color: #F1F5F9;
    }
    
    /* Barra lateral azul marino */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Tarjeta central de Login */
    .login-card {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.08);
        border: 1px solid #E2E8F0;
        max-width: 480px;
        margin: 0 auto;
    }
    
    /* Encabezado del Login */
    .login-header {
        color: #0F172A;
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }
    .login-subtitle {
        color: #64748B;
        font-size: 14px;
        text-align: center;
        margin-bottom: 28px;
    }
    
    /* Botones primarios corporativos */
    .stButton>button {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1E40AF !important;
        box-shadow: 0px 4px 12px rgba(29, 78, 216, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS Y SESIÓN
if 'db_logistica' not in st.session_state:
    st.session_state.db_logistica = pd.DataFrame([
        {"ID ENVÍO": "ALFA-124", "CLIENTE": "María Rodríguez", "ORIGEN": "Surco", "DESTINO": "Santa Anita", "ESTADO": "EN RUTA", "CONDUCTOR": "Juan Pérez", "EVIDENCIA": "Ninguna"},
        {"ID ENVÍO": "ALFA-123", "CLIENTE": "Inversiones Globales", "ORIGEN": "Callao", "DESTINO": "Ate", "ESTADO": "DELIVERED", "CONDUCTOR": "Luis Vargas", "EVIDENCIA": "Código de barra verificado + Foto de fachada"},
        {"ID ENVÍO": "ALFA-122", "CLIENTE": "Pedro Castillo", "ORIGEN": "Chorrillos", "DESTINO": "San Miguel", "ESTADO": "POR RECOGER", "CONDUCTOR": "Por Asignar", "EVIDENCIA": "Ninguna"}
    ])

if 'usuarios_registrados' not in st.session_state:
    st.session_state.usuarios_registrados = {
        "admin": {"pass": "admin123", "rol": "👨‍💼 Portal Administrador"}
    }

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None
if 'rol_actual' not in st.session_state:
    st.session_state.rol_actual = None

# 3. BARRA LATERAL INSTITUCIONAL
st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='margin:0; font-size: 20px; font-weight: 800; letter-spacing: 1px; color: #60A5FA;'>ALFA CARGO</h2>
        <p style='margin:0; font-size: 12px; font-weight: 600; color: #94A3B8; letter-spacing: 2px;'>EXPRESS</p>
    </div>
    <hr style='border-color: #334155; margin: 15px 0;'>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 12px; color: #94A3B8; text-align: center;'>Plataforma Logística v2.0<br>Central Lima - Operativa 24/7</p>", unsafe_allow_html=True)

# 4. PANTALLA DE LOGIN CON TARJETA CORPORATIVA
if st.session_state.usuario_actual is None:
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("""
            <div class="login-card">
                <div class="login-header">ALFA CARGO EXPRESS</div>
                <div class="login-subtitle">Ingresa tus credenciales para acceder al sistema</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulario dentro de la tarjeta
        input_user = st.text_input("Usuario:", key="user_login")
        input_pass = st.text_input("Contraseña:", type="password", key="pass_login")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Iniciar Sesión"):
            if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                st.session_state.usuario_actual = input_user
                st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

# 5. SESIÓN INICIADA (PANEL DE TRABAJO)
else:
    st.sidebar.markdown(f"**Usuario:** {st.session_state.usuario_actual}")
    st.sidebar.markdown(f"**Rol:** {st.session_state.rol_actual}")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_actual = None
        st.session_state.rol_actual = None
        st.rerun()
        
    st.markdown(f"# Bienvenido al {st.session_state.rol_actual}")
    st.dataframe(st.session_state.db_logistica, use_container_width=True)
