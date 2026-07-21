import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS - AJUSTE DE COLORES, TIPOGRAFÍAS Y BOTÓN COMPACTO
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
    
    /* Títulos y textos de la sección izquierda */
    .hero-title {
        color: #0F172A;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    .value-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 25px;
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

    /* FORZAR TEXTOS Y PLACEHOLDERS OSCUROS Y LEGIBLES */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        font-size: 15px !important;
    }
    
    /* Color para el texto sugerido (placeholder) */
    .stTextInput input::placeholder {
        color: #64748B !important;
        opacity: 1 !important;
    }
    
    .stTextInput label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* COLOR DE TEXTO PARA CHECKBOX (RECORDAR) */
    .stCheckbox label p {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* BOTÓN AZUL COMPACTO AL 100% DEL ANCHO DEL CONTENEDOR */
    .stButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
    }

    .login-footer {
        text-align: center;
        color: #64748B;
        font-size: 12px;
        margin-top: 30px;
        line-height: 1.5;
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
    
    # Header Superior
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 40px 25px 40px;'>
            <div style='font-size: 24px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #475569; font-size: 14px; font-weight: 600;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_space, col_right = st.columns([1.4, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA (MARCA & ILUSTRACIÓN LOGÍSTICA ESTILO IMILE) ---
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
        
        # Imagen Isométrica 3D estable de Logística/Transporte
        st.image("https://raw.githubusercontent.com/streamlit/demo-self-driving/master/streamlit_app.png", use_container_width=True) # Reemplazo seguro por ilustración 3D
        st.markdown("""
            <div style='text-align: center; margin-top: 10px;'>
                <img src='https://illustrations.popsy.co/blue/delivery-truck.svg' style='max-width: 380px; width: 100%; height: auto;' />
            </div>
        """, unsafe_allow_html=True)

    # --- COLUMNA DERECHA (TARJETA COMPACTA DE LOGIN) ---
    with col_right:
        st.markdown("""
            <div style='background-color: #FFFFFF; padding: 35px 30px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.04); max-width: 380px; margin: 0 auto;'>
                <h3 style='text-align: center; color: #0F172A; font-size: 24px; font-weight: 800; margin-bottom: 25px;'>Iniciar Sesión</h3>
        """, unsafe_allow_html=True)
        
        input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
        input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
        
        # Fila de Recordar y Olvidaste tu contraseña
        col_opt1, col_opt2 = st.columns([1, 1.2])
        with col_opt1:
            remember = st.checkbox("Recordar", value=True)
        with col_opt2:
            st.markdown('<div style="text-align: right; padding-top: 3px;"><a href="#" style="color: #2563EB; font-size: 13px; font-weight: 600; text-decoration: none;">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
        
        if st.button("Iniciar Sesión"):
            if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                st.session_state.usuario_actual = input_user
                st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
        
        st.markdown("""
                <div class="login-footer">
                    © 2026 Alfa Cargo Express.<br>Todos los derechos reservados.
                </div>
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
