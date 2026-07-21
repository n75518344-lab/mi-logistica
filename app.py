import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS - RÉPLICA EXACTA DE LA ESTRUCTURA IMILE
st.markdown("""
    <style>
    /* Ocultar barra lateral */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Fondo con tono azul suave idéntico a iMile */
    .stApp {
        background-color: #EEF4FC !important;
    }

    /* CONTENEDOR PRINCIPAL CENTRADO (Evita que esté pegado a los bordes) */
    .block-container {
        max-width: 1120px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: 0 auto !important;
    }

    /* ESTILOS DE LA COLUMNA IZQUIERDA */
    .hero-title {
        color: #0F172A;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 25px;
    }
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 25px;
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
        color: #3B82F6;
        font-weight: bold;
        margin-right: 8px;
        font-size: 16px;
    }

    /* TARJETA BLANCA FLOTANTE ESTILO IMILE */
    [data-testid="column"]:nth-child(3) {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.06) !important;
        padding: 35px 30px !important;
    }

    /* ENCABEZADO Y TABS DE LA TARJETA */
    .card-title {
        text-align: center;
        color: #0F172A;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .card-tabs {
        display: flex;
        justify-content: center;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .card-tab-active {
        color: #2563EB;
        font-weight: 700;
        font-size: 14px;
        padding-bottom: 8px;
        border-bottom: 2px solid #2563EB;
        margin-right: 25px;
    }
    .card-tab-inactive {
        color: #94A3B8;
        font-weight: 600;
        font-size: 14px;
        padding-bottom: 8px;
    }

    /* CAJAS DE TEXTO (INPUTS) CON BORDE DEFINIDO Y LIMPIO */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }
    .stTextInput input::placeholder {
        color: #94A3B8 !important;
    }
    .stTextInput label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* CHECKBOX Y ENLACE DE CONTRASEÑA */
    .stCheckbox label p {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }

    /* BOTÓN AZUL EXACTO AL DE IMILE */
    .stButton>button {
        background-color: #6366F1 !important; /* Azul/Púrpura suave tipo iMile */
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 12px 0px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 15px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #4F46E5 !important;
    }

    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        margin-top: 25px;
        line-height: 1.4;
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
    
    # Encabezado superior tipo iMile (Logo izquierda, idioma/ubicación derecha)
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
            <div style='font-size: 22px; font-weight: 900; color: #1E3A8A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #475569; font-size: 13px; font-weight: 600;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_space, col_right = st.columns([1.3, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA (CONTENIDO Y MODELO 3D) ---
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
        
        # Almacén 3D limpio al estilo iMile
        st.markdown("""
            <div style='text-align: center; margin-top: 15px;'>
                <img src='https://illustrations.popsy.co/blue/delivery-truck.svg' style='max-width: 380px; width: 100%; height: auto;' />
            </div>
        """, unsafe_allow_html=True)

    # --- COLUMNA DERECHA (TARJETA DE LOGIN IMILE) ---
    with col_right:
        st.markdown('<div class="card-title">Bienvenido a Alfa Cargo</div>', unsafe_allow_html=True)
        
        # Pestañas superiores estilizadas
        st.markdown("""
            <div class="card-tabs">
                <span class="card-tab-active">Iniciar Sesión</span>
                <span class="card-tab-inactive">Acceso Corporativo</span>
            </div>
        """, unsafe_allow_html=True)
        
        input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
        input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
        
        col_opt1, col_opt2 = st.columns([1, 1.1])
        with col_opt1:
            remember = st.checkbox("Recordar", value=True)
        with col_opt2:
            st.markdown('<div style="text-align: right; padding-top: 3px;"><a href="#" style="color: #2563EB; font-size: 12px; font-weight: 600; text-decoration: none;">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
        
        # Botón estilo iMile
        if st.button("Iniciar Sesión"):
            if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                st.session_state.usuario_actual = input_user
                st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
        
        st.markdown("""
            <div class="login-footer">
                Copyright © 2026 Alfa Cargo Express. All rights reserved.
            </div>
        """, unsafe_allow_html=True)

# 5. SESIÓN INICIADA (SISTEMA CENTRAL)
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
