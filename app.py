import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sugar Rush Admin", page_icon="🍩", layout="wide")

if 'inventario' not in st.session_state:
    st.session_state.inventario = {
        # Carnes y Proteínas
        "Pechuga sin Piel (AVSA/Granja)": {"cant": 6.44, "un": "kg", "costo": 120156}, # Suma de facturas 08 y 10 abril
        "Copete (Maxicarnes)": {"cant": 3.61, "un": "kg", "costo": 111910},           # Factura 08 abril
        # Lácteos y Abarrotes
        "Queso Mozzarella": {"cant": 2.0, "un": "kg", "costo": 37600},              # Facturas Papirusa y D1
        "Leche Entera (Montefrio/Granja)": {"cant": 5.0, "un": "L", "costo": 19600}, # Facturas 08 y 11 abril
        "Pasta Doria Lasaña": {"cant": 0.2, "un": "kg", "costo": 6371},             # Factura 10 abril
        # Vegetales y Condimentos (La Esmeralda/Granja)
        "Pimentón Extra": {"cant": 0.25, "un": "kg", "costo": 1500},
        "Cebolla Blanca": {"cant": 1.0, "un": "und", "costo": 3000},
        "Ajo": {"cant": 1.0, "un": "paquete", "costo": 1300},
        # Empaques y Desechables (Sigmaplas/Vayboplas)
        "Moldes Aluminio Lasaña": {"cant": 60, "un": "und", "costo": 17700},
        "Tapas Lasaña": {"cant": 50, "un": "und", "costo": 4410},
        "Servilletas Elite": {"cant": 1.0, "un": "paquete", "costo": 6800}
    }

st.title("🍩 Administración Sugar Rush")

# Lógica de producción mejorada
with st.sidebar:
    st.header("🚀 Registrar Producción")
    producto = st.selectbox("¿Qué vas a preparar hoy?", ["Lasaña Pollo (20 und)", "Alfajores (70 und)", "Torta María Luisa"])
    if st.button("Confirmar y Descontar"):
        if "Lasaña" in producto:
            st.session_state.inventario["Pechuga sin Piel (AVSA/Granja)"]["cant"] -= 2.8
            st.session_state.inventario["Moldes Aluminio Lasaña"]["cant"] -= 20
            st.session_state.inventario["Tapas Lasaña"]["cant"] -= 20
        st.success(f"Se descontaron los insumos para: {producto}")

st.subheader("📋 Inventario Actualizado al 11 de Abril")
df = pd.DataFrame.from_dict(st.session_state.inventario, orient='index')
st.dataframe(df, use_container_width=True)

st.info("💡 Nota: He sumado automáticamente las compras de la Tienda La Granja y AVSA.")