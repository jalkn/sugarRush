import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sugar Rush Admin", page_icon="🍩", layout="wide")

# Estilos personalizados (Igual al index.html)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }
    .main { background: linear-gradient(135deg, #fffcf9 0%, #fff1e6 100%); }
    .stButton>button { border-radius: 50px; font-weight: bold; transition: all 0.2s; }
    .btn-venta { background-color: #22c55e !important; color: white !important; border: none !important; }
    .card { background-color: white; padding: 25px; border-radius: 2rem; border: 1px solid #ffedd5; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 20px; }
    h1, h2, h3 { color: #7c2d12 !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Inventario Inicial (Sincronizado con tus facturas)
if 'inventario' not in st.session_state:
    st.session_state.inventario = {
        "Pechuga sin Piel (Pollo)": {"cant": 6.44, "un": "kg"},
        "Copete (Res/Cerdo)": {"cant": 3.61, "un": "kg"},
        "Queso Mozzarella": {"cant": 2.0, "un": "kg"},
        "Pasta Doria Lasaña": {"cant": 1.2, "un": "kg"},
        "Leche Entera": {"cant": 5.0, "un": "L"},
        "Moldes Aluminio": {"cant": 60, "un": "und"},
        "Tapas Lasaña": {"cant": 50, "un": "und"}
    }

# 2. Definición de Gasto por Unidad (Receta unitaria)
# Estos valores se multiplican por la cantidad vendida
gasto_unitario = {
    "Lasaña de Pollo": {
        "Pechuga sin Piel (Pollo)": 0.14, # 140g
        "Queso Mozzarella": 0.07,         # 70g
        "Leche Entera": 0.12,             # 120ml para bechamel
        "Moldes Aluminio": 1,
        "Tapas Lasaña": 1
    },
    "Lasaña Mixta": {
        "Pechuga sin Piel (Pollo)": 0.08, # 80g
        "Copete (Res/Cerdo)": 0.08,        # 80g
        "Queso Mozzarella": 0.07,
        "Leche Entera": 0.12,
        "Moldes Aluminio": 1,
        "Tapas Lasaña": 1
    }
}

st.markdown("<h1>🍩 Gestión de Ventas Sugar Rush</h1>", unsafe_allow_html=True)

# --- SECCIÓN DE VENTAS REALIZADAS ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Registrar Venta Finalizada")
st.write("Usa esta sección para descontar del inventario lo que ya se entregó al cliente.")

col_prod, col_cant, col_btn = st.columns([2, 1, 1])

with col_prod:
    prod_vendido = st.selectbox("Producto vendido:", list(gasto_unitario.keys()))

with col_cant:
    cantidad_vendida = st.number_input("Cantidad unidades:", min_value=1, value=50)

with col_btn:
    st.write(" ") # Espaciador
    if st.button("🚀 Actualizar por Venta", use_container_width=True):
        receta = gasto_unitario[prod_vendido]
        
        # Validación de Stock
        error_stock = False
        for ing, gasto in receta.items():
            total_gasto = gasto * cantidad_vendida
            if st.session_state.inventario[ing]["cant"] < total_gasto:
                st.error(f"¡No hay suficiente {ing}! Necesitas {total_gasto:.2f} y solo hay {st.session_state.inventario[ing]['cant']:.2f}")
                error_stock = True
        
        if not error_stock:
            for ing, gasto in receta.items():
                st.session_state.inventario[ing]["cant"] -= (gasto * cantidad_vendida)
            st.success(f"✅ ¡Inventario actualizado! Se descontaron los insumos de {cantidad_vendida} {prod_vendido}.")

st.markdown("</div>", unsafe_allow_html=True)

# --- VISUALIZACIÓN DE INVENTARIO ---
st.subheader("📋 Estado Actual de Insumos")
df = pd.DataFrame.from_dict(st.session_state.inventario, orient='index')
st.dataframe(df.style.format(precision=2), use_container_width=True)

# Alerta de resurtido
if st.session_state.inventario["Pasta Doria Lasaña"]["cant"] < 1.0:
    st.warning("⚠️ ¡Atención! Te queda menos de 1kg de pasta. Hora de volver a la Mayorista.")

st.markdown("<p style='text-align: center; color: #f97316; margin-top: 50px;'>Sugar Rush Admin | Hecho en Santa Elena</p>", unsafe_allow_html=True)