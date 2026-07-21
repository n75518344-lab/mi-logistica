import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS - TARJETA MAXIMIZADA VERTICALMENTE
st.markdown("""
    <style>
    /* Ocultar barra lateral */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Fondo general tipo iMile */
    .stApp {
        background-color: #EEF4FC !important;
    }

    /* CONTENEDOR PRINCIPAL */
    .block-container {
        max-width: 88% !important;
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* COLUMNA IZQUIERDA */
    .hero-title {
        color: #0F172A;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 22px;
    }
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 24px;
    }
    .value-item {
        color: #1E293B;
        font-weight: 700;
        font-size: 15px;
        display: flex;
        align-items: center;
    }
    .value-item::before {
        content: "▌";
        color: #2563EB;
        font-weight: bold;
        margin-right: 10px;
        font-size: 18px;
    }

    /* MARCO DE IMAGEN IZQUIERDA (Aumentado para acompañar a la derecha) */
    .image-card-frame {
        background-color: #E2ECF9;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.03);
    }
    .hero-image {
        width: 100%;
        height: 360px;
        object-fit: cover;
        border-radius: 12px;
    }

    /* TARJETA BLANCA DE LOGIN - MÁXIMO ESPACIO INFERIOR */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border-radius: 22px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0px 12px 35px rgba(0, 0, 0, 0.06) !important;
        padding: 60px 42px 90px 42px !important; /* Espaciado extra amplio abajo */
        margin-top: 0px !important;
    }

    /* TÍTULO AMPLIO CON MÁS SEPARACIÓN */
    .card-title {
        text-align: center;
        color: #0F172A;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 35px;
    }

    /* INPUTS CON MÁS MARGEN VERTICAL */
    .stTextInput {
        margin-bottom: 16px !important;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 13px 16px !important;
        font-size: 15px !important;
    }
    .stTextInput label {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin-bottom: 6px !important;
    }

    /* CHECKBOX Y ENLACE */
    .stCheckbox label p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* BOTÓN DE INICIO DE SESIÓN */
    div[data-testid="stFormSubmitButton"] {
        width: 100% !important;
        margin-top: 30px !important;
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px 0px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1D4ED8 !important;
    }

    /* FOOTER CON GRAN SEPARACIÓN HACIA ABAJO */
    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin-top: 70px;
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
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;'>
            <div style='font-size: 26px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #475569; font-size: 15px; font-weight: 600;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.3, 1.0], gap="large")
    
    # --- COLUMNA IZQUIERDA ---
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
        
        st.markdown("""
            <div class="image-card-frame">
                <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80" class="hero-image" />
            </div>
        """, unsafe_allow_html=True)

    # --- COLUMNA DERECHA (TARJETA LOGIN EXTRA MÁS ALTA) ---
    with col_right:
        with st.form("login_form"):
            st.markdown('<div class="card-title">Bienvenido a Alfa Cargo</div>', unsafe_allow_html=True)
            
            input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
            input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
            
            col_opt1, col_opt2 = st.columns([1, 1.2])
            with col_opt1:
                remember = st.checkbox("Recordar", value=True)
            with col_opt2:
                st.markdown('<div style="text-align: right; padding-top: 3px;"><a href="#" style="color: #2563EB; font-size: 13px; font-weight: 600; text-decoration: none;">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
            
            submit_btn = st.form_submit_button("Iniciar Sesión", use_container_width=True)
            
            if submit_btn:
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
