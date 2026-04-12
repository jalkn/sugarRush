import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sugar Rush Admin", page_icon="🍩", layout="wide")

# Inicialización de Inventario Completo
if 'inventario' not in st.session_state:
    st.session_state.inventario = {
        # Salados
        "Pechuga de Pollo": {"cant": 6.5, "un": "kg", "costo": 120051},
        "Copete (Carne)": {"cant": 3.61, "un": "kg", "costo": 111910},
        "Pasta Lasaña": {"cant": 1.2, "un": "kg", "costo": 39900},
        "Queso Mozzarella": {"cant": 2.5, "un": "kg", "costo": 37600},
        "Leche": {"cant": 5.0, "un": "L", "costo": 19600},
        # Repostería (Estimados iniciales)
        "Harina Trigo": {"cant": 5.0, "un": "kg", "costo": 25000},
        "Mantequilla": {"cant": 2.0, "un": "kg", "costo": 32000},
        "Azúcar": {"cant": 4.0, "un": "kg", "costo": 16000},
        "Arequipe / Manjar": {"cant": 3.0, "un": "kg", "costo": 45000},
        # Empaques
        "Moldes Lasaña": {"cant": 60, "un": "und", "costo": 17700},
        "Cajas Alfajores/Brownies": {"cant": 40, "un": "und", "costo": 28000}
    }

st.title("🍩 Administración Sugar Rush")

# --- BARRA LATERAL: TANDAS DE PRODUCCIÓN ---
with st.sidebar:
    st.header("🚀 Registrar Producción")
    tipo_producto = st.selectbox("Seleccionar Producto", [
        "Lasaña Pollo (20 und)", 
        "Alfajores (70 und)", 
        "Brownies (20 und)", 
        "Torta María Luisa (1 und)"
    ])
    
    confirmar = st.button("Confirmar Tanda")

    if confirmar:
        # Lógica de descuento por producto
        if "Lasaña" in tipo_producto:
            st.session_state.inventario["Pechuga de Pollo"]["cant"] -= 2.8
            st.session_state.inventario["Pasta Lasaña"]["cant"] -= 1.2
            st.session_state.inventario["Queso Mozzarella"]["cant"] -= 1.5
            st.session_state.inventario["Moldes Lasaña"]["cant"] -= 20
        elif "Alfajores" in tipo_producto:
            st.session_state.inventario["Harina Trigo"]["cant"] -= 1.5
            st.session_state.inventario["Mantequilla"]["cant"] -= 0.8
            st.session_state.inventario["Arequipe / Manjar"]["cant"] -= 1.0
        elif "Brownies" in tipo_producto:
            st.session_state.inventario["Harina Trigo"]["cant"] -= 0.5
            st.session_state.inventario["Azúcar"]["cant"] -= 0.6
            st.session_state.inventario["Mantequilla"]["cant"] -= 0.4
        elif "María Luisa" in tipo_producto:
            st.session_state.inventario["Harina Trigo"]["cant"] -= 0.3
            st.session_state.inventario["Leche"]["cant"] -= 0.2
            
        st.success(f"Inventario actualizado tras tanda de {tipo_producto}")

# --- PANTALLA PRINCIPAL ---
tab1, tab2 = st.tabs(["📋 Inventario Actual", "📊 Metas y Ganancias"])

with tab1:
    st.subheader("Suministros en Bodega")
    # Convertir a DataFrame para mostrar
    df_inv = pd.DataFrame.from_dict(st.session_state.inventario, orient='index')
    st.dataframe(df_inv.style.highlight_min(axis=0, color='#ffcccc'), use_container_width=True)
    
    st.warning("⚠️ Los ítems en rojo están llegando a su nivel mínimo de stock.")

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Venta Proyectada Lasañas", "$440,000", "+$210k utilidad")
    with col2:
        st.metric("Venta Proyectada Dulces", "$435,000", "+$259k utilidad")
    with col3:
        costo_fijo = 150000 # Gas, Moto, Mano de obra
        st.metric("Costos Operativos", f"${costo_fijo:,}")

st.divider()
st.info("💡 Tip de Orden: No olvides registrar las facturas de la Mayorista apenas llegues para mantener los costos unitarios al día.")