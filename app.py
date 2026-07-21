import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA (Sin barra lateral)
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS (Diseño compacto tipo iMile/Instagram + Ocultar Sidebar)
st.markdown("""
    <style>
    /* Ocultar la barra lateral por completo */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Fondo limpio gris tenue */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Encabezado y títulos */
    .hero-title {
        color: #0F172A;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 16px;
    }
    
    /* Cuadrícula de valores */
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
    
    /* Tarjeta de Login compacta (Estilo Instagram / iMile) */
    div[data-testid="column"]:nth-child(3) {
        max-width: 360px !important;
        margin: 0 auto;
    }
    
    /* Ajustes para textos y campos dentro de las columnas */
    .stTextInput label {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    .stTextInput input {
        border-radius: 6px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 8px 12px !important;
    }
    
    /* Botón compacto corporativo */
    .stButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
    }
    
    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 11px;
        margin-top: 20px;
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
    
    # Barra superior limpia
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 15px 40px 25px 40px;'>
            <div style='font-size: 22px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #64748B; font-size: 13px; font-weight: 500;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Distribución de 2 columnas principales
    col_left, col_space, col_right = st.columns([1.4, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA (MARCA & FOTO LOGÍSTICA REAL) ---
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
        
        # Imagen de logística profesional / almacén neutral (sin marcas de terceros)
        st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1000&q=80", use_container_width=True)

    # --- COLUMNA DERECHA (TARJETA COMPACTA DE LOGIN) ---
    with col_right:
        # Formulario compacto
        st.markdown("<h2 style='text-align: center; color: #0F172A; font-size: 22px; font-weight: 700; margin-bottom: 2px;'>Bienvenido</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B; font-size: 13px; margin-bottom: 20px;'>Ingresa tus credenciales</p>", unsafe_allow_html=True)
        
        input_user = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_login")
        input_pass = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_login")
        
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

# 5. SESIÓN INICIADA (DASHBOARD)
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
