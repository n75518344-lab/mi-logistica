import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS - CARD DE LOGIN INTEGRADA (ESTILO INSTAGRAM / IMILE)
st.markdown("""
    <style>
    /* Ocultar la barra lateral completamente */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Fondo general gris tenue */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Títulos de la sección izquierda */
    .hero-title {
        color: #0F172A;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 16px;
    }
    
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 20px;
    }
    .value-item {
        color: #334155;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
    }
    .value-item::before {
        content: "▌";
        color: #2563EB;
        font-weight: bold;
        margin-right: 8px;
    }

    /* TARJETA BLANCA DE LOGIN CONTENEDORA */
    div[data-testid="stColumn"]:nth-child(3) {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.04);
        max-width: 380px !important;
        margin: 0 auto;
    }

    /* ESTILO DE CAMPOS DE TEXTO */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }
    .stTextInput label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* BOTÓN QUE ABARCA EL 100% DE LA TARJETA */
    .stButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 11px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
    }

    /* LINKS Y CHECKBOXES */
    .forgot-pass {
        text-align: center;
        margin-top: 10px;
    }
    .forgot-pass a {
        color: #2563EB;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
    }
    .forgot-pass a:hover {
        text-decoration: underline;
    }

    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
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

# 4. PANTALLA PRINCIPAL DE LOGIN
if st.session_state.usuario_actual is None:
    
    # Encabezado superior
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 30px 20px 30px;'>
            <div style='font-size: 22px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #64748B; font-size: 13px; font-weight: 500;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_space, col_right = st.columns([1.5, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA (MARCA & ILUSTRACIÓN 3D TIPO IMILE) ---
    with col_left:
        st.markdown('<div class="hero-title">Excelencia Logística y Control Operativo</div>', unsafe_allow_html=True)
        
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
        
        # Ilustración isométrica 3D estilo iMile
        st.image("https://cdni.iconscout.com/illustration/premium/thumb/logistics-warehouse-management-5381831-4501062.png", use_container_width=True)

    # --- COLUMNA DERECHA (TARJETA COMPACTA INTEGRADA) ---
    with col_right:
        st.markdown("<h3 style='text-align: center; color: #0F172A; font-size: 22px; font-weight: 700; margin-bottom: 20px;'>Iniciar Sesión</h3>", unsafe_allow_html=True)
        
        input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
        input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
        
        # Opciones: Recuerdame + Olvidaste tu contraseña
        col_opt1, col_opt2 = st.columns([1, 1])
        with col_opt1:
            remember = st.checkbox("Recuérdame", value=True)
        with col_opt2:
            st.markdown('<div style="text-align: right; padding-top: 5px;"><a href="#" style="color: #2563EB; font-size: 12px; font-weight: 600; text-decoration: none;">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
        
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

# 5. SESIÓN INICIADA (PANEL DE TRABAJO)
else:
    col_nav1, col_nav2 = st.columns([5, 1])
    with col_nav1:
        st.markdown(f"### 🔷 ALFA CARGO EXPRESS — {st.session_state.rol_actual}")
        st.caption(f"Usuario activo: {st.session_state.usuario_actual}")
    with col_nav2:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.rerun()
            
    st.markdown("---")
    st.dataframe(st.session_state.db_logistica, use_container_width=True)
