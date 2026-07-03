import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Logística Pro", page_icon="🚚", layout="wide")

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame([
        {"ID": "PED-001", "Cliente": "Tienda Alfa", "Destino": "Av. Larco 123", "Estado": "En Ruta", "Evidencia": "Ninguna", "Fecha": "2026-07-02"},
        {"ID": "PED-002", "Cliente": "Boutique Beta", "Destino": "Calle Flores 456", "Estado": "Entregado", "Evidencia": "Firmado por María", "Fecha": "2026-07-02"}
    ])

st.title("🚚 Sistema de Logística - Panel de Control")
st.markdown("---")

modo = st.sidebar.radio("Selecciona tu Vista:", ["👨‍💼 Administrador (Tú)", "🛵 Repartidor (Celular)"])

if modo == "👨‍💼 Administrador (Tú)":
    st.header("Panel de Administración")
    st.subheader("1. Carga Masiva de Pedidos")
    
    plantilla = pd.DataFrame(columns=["ID", "Cliente", "Destino"])
    excel_plantilla = plantilla.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Plantilla (Formato CSV)",
        data=excel_plantilla,
        file_name="plantilla_logistica.csv",
        mime="text/csv"
    )
    
    archivo_subido = st.file_uploader("Arrastra aquí tu plantilla CSV con los pedidos del día", type=["csv"])
    
    if archivo_subido is not None:
        try:
            nuevos_pedidos = pd.read_csv(archivo_subido)
            nuevos_pedidos["Estado"] = "En Almacén"
            nuevos_pedidos["Evidencia"] = "Ninguna"
            nuevos_pedidos["Fecha"] = datetime.today().strftime('%Y-%m-%d')
            
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevos_pedidos], ignore_index=True)
            st.success("¡Éxito! Los pedidos se cargaron correctamente.")
        except Exception as e:
            st.error(f"Error al leer el archivo. Asegúrate de usar la plantilla descargada. Detalle: {e}")

    st.markdown("---")
    st.subheader("2. Estado de todos los Envíos")
    st.dataframe(st.session_state.pedidos, use_container_width=True)

else:
    st.header("📱 Portal del Repartidor")
    pedidos_activos = st.session_state.pedidos[st.session_state.pedidos["Estado"] != "Entregado"]
    
    if pedidos_activos.empty:
        st.success("🎉 ¡Felicidades! No tienes rutas pendientes.")
    else:
        lista_ids = pedidos_activos["ID"].tolist()
        pedido_seleccionado = st.selectbox("Selecciona el Pedido:", lista_ids)
        
        datos_pedido = st.session_state.pedidos[st.session_state.pedidos["ID"] == pedido_seleccionado].iloc[0]
        st.info(f"**Cliente:** {datos_pedido['Cliente']}\n\n**Dirección:** {datos_pedido['Destino']}")
        
        foto_evidencia = st.camera_input("📸 Toma una foto de la evidencia")
        comentario = st.text_input("Nota opcional:")
        
        if st.button("✅ Marcar como ENTREGADO"):
            fila_index = st.session_state.pedidos[st.session_state.pedidos["ID"] == pedido_seleccionado].index[0]
            st.session_state.pedidos.at[fila_index, "Estado"] = "Entregado"
            st.session_state.pedidos.at[fila_index, "Evidencia"] = f"Foto subida + '{comentario}'" if foto_evidencia else f"Sin foto + '{comentario}'"
            st.success(f"¡Pedido {pedido_seleccionado} actualizado!")
            st.rerun()