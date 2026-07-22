st.markdown(
    """
    <style>
    /* 1. OCULTAR SIDEBAR Y ELEMENTOS NATIVOS */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] { display: none !important; }
    
    /* 2. FONDO GENERAL */
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    .block-container { max-width: 90% !important; padding-top: 2rem !important; padding-bottom: 2rem !important; }
    
    /* 3. TEXTOS Y ENCABEZADOS */
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #0F172A !important; }

    /* 4. CONTENEDOR TARJETA / FORMULARIO */
    [data-testid="stForm"] { 
        background-color: #FFFFFF !important; 
        border-radius: 16px !important; 
        border: 1px solid #E2E8F0 !important; 
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.05) !important; 
        padding: 32px !important; 
        border-top: 5px solid #0F382C !important; 
    }
    .card-title { text-align: center; color: #0F382C !important; font-size: 26px; font-weight: 800; margin-bottom: 20px; }

    /* 5. INPUTS DE TEXTO Y CONTRASEÑA */
    .stTextInput input { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important; 
        border-radius: 8px !important; 
        padding-right: 40px !important;
    }
    .stTextInput input::placeholder { color: #94A3B8 !important; opacity: 1 !important; }

    /* FIX AL OJO DE CONTRASEÑA ("visibili...") */
    div[data-baseweb="input"] > div {
        background-color: transparent !important;
        color: transparent !important;
    }
    button[aria-label="Show password"], 
    button[aria-label="Hide password"],
    div[data-testid="stTextInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #0F382C !important;
        font-size: 0px !important; /* Oculta cualquier texto residual como 'visibility' */
    }
    button[aria-label="Show password"] svg, 
    button[aria-label="Hide password"] svg,
    div[data-testid="stTextInput"] button svg {
        fill: #0F382C !important;
        width: 18px !important;
        height: 18px !important;
    }

    /* 6. FIX AL SELECTBOX Y SU MENÚ DESPLEGABLE (POPOVER) */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    /* Estilo del menú flotante de opciones */
    div[data-baseweb="popover"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    li[role="option"], div[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    li[role="option"]:hover, div[role="option"]:hover {
        background-color: #F1F5F9 !important;
        color: #0F382C !important;
    }

    /* 7. BOTÓN PRINCIPAL (INICIAR SESIÓN / GUARDAR) */
    div[data-testid="stFormSubmitButton"] > button { 
        background-color: #0F382C !important; 
        border-radius: 8px !important; 
        border: none !important; 
        padding: 10px 0px !important; 
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] > button p, 
    div[data-testid="stFormSubmitButton"] > button span { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
    }
    div[data-testid="stFormSubmitButton"] > button:hover { background-color: #15803D !important; }

    /* 8. TABLAS Y PESTAÑAS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; gap: 6px; }
    .stTabs [data-baseweb="tab"] { background-color: #E2E8F0 !important; border-radius: 8px 8px 0px 0px !important; border: none !important; }
    .stTabs [data-baseweb="tab"] p { color: #334155 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] { background-color: #0F382C !important; }
    .stTabs [aria-selected="true"] p { color: #FFFFFF !important; font-weight: 800 !important; }
    </style>
""",
    unsafe_allow_html=True,
)
