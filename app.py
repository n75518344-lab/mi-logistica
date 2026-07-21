import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Alfa Cargo Express", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# 2. HACK DE ESTILOS CSS AVANZADOS (Fuerza el diseño tipo Instagram/iMile)
st.markdown("""
    <style>
    /* Ocultar elementos nativos molestos */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Encabezado e izquierdo */
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
        color: #2563EB;
        font-weight: bold;
        margin-right: 8px;
    }

    /* CONTENEDOR LOGIN INTEGRADO (Estilo Instagram) */
    .login-container {
        background-color: #FFFFFF;
        padding: 35px 30px;
        border-radius: 4px;
        border: 1px solid #DBDBDB;
        max-width: 350px;
        margin: 0 auto;
        text-align: center;
    }
    
    /* Forzar diseño limpio en los inputs nativos dentro de la columna */
    .stTextInput label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        text-align: left !important;
        display: block;
    }
    .stTextInput input {
        background-color: #FAFAFA !important;
        color: #262626 !important;
        border: 1px solid #DBDBDB !important;
        border-radius: 4px !important;
        padding: 9px 12px !important;
    }
    
    /* Arreglo del input de contraseña y el botón del ojo */
    div[data-testid="stTextInput"] div {
        background-color: transparent !important;
    }
    div[data-testid="stTextInput"] button {
        background-color: transparent !important;
        color: #737373 !important;
        border: none !important;
    }

    /* Botón Iniciar Sesión que ocupa el 100% */
    div.stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 8px 0px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
    }

    /* Links inferiores estilo red social */
    .login-link {
        color: #1E3A8A;
        font-size: 12px;
        text-decoration: none;
        font-weight: 500;
        display: block;
        margin-top: 15px;
    }
    .login-link:hover {
        text-decoration: underline;
    }
    
    .login-footer {
        text-align: center;
        color: #8E8E8E;
        font-size: 11px;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS Y ESTADOS
if 'db_logistica' not in st.session_state:
    st.session_state.db_logistica = pd.DataFrame([
        {"ID ENVÍO": "ALFA-124", "CLIENTE": "María Rodríguez", "ORIGEN": "Surco", "DESTINO": "Santa Anita", "ESTADO": "EN RUTA", "CONDUCTOR": "Juan Pérez", "EVIDENCIA": "Ninguna"},
        {"ID ENVÍO": "ALFA-123", "CLIENTE": "Inversiones Globales", "ORIGEN": "Callao", "DESTINO": "Ate", "ESTADO": "DELIVERED", "CONDUCTOR": "Luis Vargas", "EVIDENCIA": "Verificado"}
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
    
    # Header minimalista superior
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; padding: 15px 40px 10px 40px;'>
            <div style='font-size: 22px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;'>
                🔷 ALFA CARGO <span style='color: #2563EB;'>EXPRESS</span>
            </div>
            <div style='color: #64748B; font-size: 13px; font-weight: 500;'>
                🌐 Central Lima, Perú
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Columnas: Izquierda (Imagen/Valores), Derecha (Tarjeta Compacta)
    col_left, col_space, col_right = st.columns([1.4, 0.1, 1.0])
    
    # --- COLUMNA IZQUIERDA: VALORES E IMAGEN ESTILO IMILE ---
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
        
        # Imagen Logística 3D limpia inspirada en iMile
        st.image("https://img.freepik.com/premium-vector/isometric-smart-logistics-concept-warehouse-with-goods-forklift-truck-delivery-van-smart-shipping-isolated-vector-illustration_612085-2415.jpg", use_container_width=True)

    # --- COLUMNA DERECHA: TARJETA INTEGRADA COMPACTA ---
    with col_right:
        # Iniciamos el contenedor div de la tarjeta
        st.markdown("""
            <div class="login-container">
                <div style='font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 25px; letter-spacing: -0.5px;'>
                    Iniciar Sesión
                </div>
        """, unsafe_allow_html=True)
        
        # Inputs del formulario dentro de la tarjeta
        input_user = st.text_input("Usuario", placeholder="Teléfono, usuario o correo", key="u_login")
        input_pass = st.text_input("Contraseña", type="password", placeholder="Contraseña", key="p_login")
        
        # Checkbox integrado para "Recuérdame"
        recuerdame = st.checkbox("Recuérdame", value=False, key="chk_remember")
        
        # Botón de Login
        if st.button("Iniciar Sesión"):
            if input_user in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[input_user]["pass"] == input_pass:
                st.session_state.usuario_actual = input_user
                st.session_state.rol_actual = st.session_state.usuarios_registrados[input_user]["rol"]
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
        
        # Links finales y cierre del contenedor
        st.markdown("""
                <a href="#" class="login-link">¿Olvidaste tu contraseña?</a>
                <div class="login-footer">
                    © 2026 Alfa Cargo Express S.A.C.<br>Todos los derechos reservados.
                </div>
            </div>
        """, unsafe_allow_html=True)

# 5. INTEGRACIÓN DEL DASHBOARD INTERNO
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
