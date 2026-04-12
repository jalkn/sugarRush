import streamlit as st
import pandas as pd

# Configuración de página con el estilo de la marca
st.set_page_config(page_title="Sugar Rush Admin", page_icon="🍩", layout="wide")

# Estilos personalizados para igualar el index.html
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #fffcf9 0%, #fff1e6 100%);
    }
    
    .stButton>button {
        border-radius: 50px;
        font-weight: bold;
        padding: 0.5rem 2rem;
        transition: all 0.2s;
    }
    
    .btn-confirmar {
        background-color: #f97316 !important;
        color: white !important;
    }
    
    .btn-ver {
        background-color: #fdf2f8 !important;
        color: #db2777 !important;
        border: 1px solid #fbcfe8 !important;
    }
    
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 2rem;
        border: 1px solid #ffedd5;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: #7c2d12 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialización de Inventario basada en facturas recientes
if 'inventario' not in st.session_state:
    st.session_state.inventario = {
        "Pechuga sin Piel (AVSA/Granja)": {"cant": 6.44, "un": "kg", "costo": 120156},
        "Copete (Maxicarnes)": {"cant": 3.61, "un": "kg", "costo": 111910},
        "Queso Mozzarella": {"cant": 2.0, "un": "kg", "costo": 37600},
        "Leche Entera": {"cant": 5.0, "un": "L", "costo": 19600},
        "Pasta Doria Lasaña": {"cant": 0.2, "un": "kg", "costo": 6371},
        "Moldes Aluminio Lasaña": {"cant": 60, "un": "und", "costo": 17700},
        "Tapas Lasaña": {"cant": 50, "un": "und", "costo": 4410},
        "Harina Trigo": {"cant": 5.0, "un": "kg", "costo": 25000},
        "Azúcar": {"cant": 4.0, "un": "kg", "costo": 16000}
    }

# Definición de recetas (ingredientes por tanda)
recetas = {
    "Lasaña Pollo (20 und)": {
        "Pechuga sin Piel (AVSA/Granja)": 2.8,
        "Moldes Aluminio Lasaña": 20,
        "Tapas Lasaña": 20,
        "Queso Mozzarella": 1.5,
        "Leche Entera": 1.0
    },
    "Alfajores (70 und)": {
        "Harina Trigo": 1.5,
        "Azúcar": 0.5,
        "Leche Entera": 0.2
    },
    "Torta María Luisa": {
        "Harina Trigo": 0.4,
        "Azúcar": 0.3,
        "Leche Entera": 0.2
    }
}

st.markdown("<h1>🍩 Panel de Control Sugar Rush</h1>", unsafe_allow_html=True)

# --- SECCIÓN DE PRODUCCIÓN ---
st.markdown("<div class='card'><h3>🚀 Gestión de Producción</h3>", unsafe_allow_html=True)

col_sel, col_btn1, col_btn2 = st.columns([2, 1, 1])

with col_sel:
    producto_seleccionado = st.selectbox("Selecciona la tanda a preparar:", list(recetas.keys()), label_visibility="collapsed")

with col_btn1:
    btn_ver = st.button("🔍 Ver Ingredientes", use_container_width=True)

with col_btn2:
    btn_confirmar = st.button("✅ Confirmar y Descontar", use_container_width=True)

# Lógica del botón "Ver Ingredientes"
if btn_ver:
    st.info(f"**Ingredientes necesarios para {producto_seleccionado}:**")
    ingredientes = recetas[producto_seleccionado]
    for ing, cant in ingredientes.items():
        unidad = st.session_state.inventario[ing]["un"]
        st.write(f"- {ing}: **{cant} {unidad}**")

# Lógica del botón "Confirmar y Descontar"
if btn_confirmar:
    ingredientes = recetas[producto_seleccionado]
    # Verificar si hay suficiente stock antes de descontar
    puede_descontar = True
    for ing, cant_necesaria in ingredientes.items():
        if st.session_state.inventario[ing]["cant"] < cant_necesaria:
            puede_descontar = False
            st.error(f"Stock insuficiente de {ing}")
    
    if puede_descontar:
        for ing, cant_necesaria in ingredientes.items():
            st.session_state.inventario[ing]["cant"] -= cant_necesaria
        st.success(f"¡Producción registrada! Se han descontado los insumos de {producto_seleccionado}.")

st.markdown("</div>", unsafe_allow_html=True)

# --- TABLA DE INVENTARIO ---
st.markdown("<h3>📋 Estado de Insumos</h3>", unsafe_allow_html=True)
df = pd.DataFrame.from_dict(st.session_state.inventario, orient='index')
st.dataframe(df.style.format(precision=2), use_container_width=True)

st.markdown("<p style='text-align: center; color: #f97316;'>Sugar Rush Admin | Un instante de dulzura</p>", unsafe_allow_html=True)