import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="Sugar Rush Admin", page_icon="🍩", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }
    .main { background: linear-gradient(135deg, #fffcf9 0%, #fff1e6 100%); }
    .stButton>button { border-radius: 50px; font-weight: bold; transition: all 0.2s; }
    .login-card { background-color: white; padding: 40px; border-radius: 2rem; border: 1px solid #ffedd5; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
    .card { background-color: white; padding: 25px; border-radius: 2rem; border: 1px solid #ffedd5; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1, h2, h3 { color: #7c2d12 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN DE LOGIN
def check_password():
    """Devuelve True si el usuario ingresó la contraseña correcta."""
    if "password_correct" not in st.session_state:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/jalkn/sugarRush/main/img/sugarrush_logo.jpg", width=100) # Ajusta la URL de tu logo
        st.markdown("<h3>🔐 Acceso Administrativo</h3>", unsafe_allow_html=True)
        
        password = st.text_input("Introduce la contraseña", type="password")
        if st.button("Entrar"):
            # AQUÍ DEFINES TU CONTRASEÑA (Cámbiala por la que quieras)
            if password == "SugarAdmin2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("😕 Contraseña incorrecta")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# Solo mostrar el contenido si el login es exitoso
if check_password():
    
    # --- INICIO DEL PORTAL DE ADMINISTRACIÓN ---
    
    # 3. INVENTARIO (Mantenemos los datos sincronizados)
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

    st.markdown("<h1>🍩 Panel Sugar Rush</h1>", unsafe_allow_html=True)

    # --- SECCIÓN DE VENTAS ---
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🛒 Registro de Ventas")
    
    col_prod, col_cant, col_btn = st.columns([2, 1, 1])
    
    with col_prod:
        prod = st.selectbox("Producto:", ["Lasaña de Pollo", "Lasaña Mixta"])
    with col_cant:
        cant = st.number_input("Cantidad:", min_value=1, value=50)
    with col_btn:
        st.write(" ")
        if st.button("🚀 Descontar Venta"):
            # Lógica de descuento (Simplificada para el ejemplo)
            st.success(f"Venta de {cant} unidades procesada.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- TABLA DE INVENTARIO ---
    st.subheader("📋 Inventario Real")
    st.table(pd.DataFrame.from_dict(st.session_state.inventario, orient='index'))

    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state["password_correct"]
        st.rerun()