#!/bin/bash

# ==============================================================================
# SUGARRUSH - MASTER SETUP & DEPLOYMENT SCRIPT (SYNC V11 - COMPLETE)
# ==============================================================================

CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
GRAY='\033[0;90m'
NC='\033[0m'

echo -e "${MAGENTA}🚀 Iniciando despliegue total de entorno SugaRush (rush-core)...${NC}"

# 1. Purga de caché
CACHE_PATHS=(".astro" "dist" "node_modules/.vite")
for path in "${CACHE_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo -e "${GRAY}🧹 Dropping: $path${NC}"
        rm -rf "$path"
    fi
done

# 2. Estructura base (Aseguramos src/pages)
mkdir -p src/data img svg public/api src/pages

# 3. Manifest (rush-core)
cat << 'JSON_EOF' > package.json
{
  "name": "rush-core",
  "type": "module",
  "version": "8.0.0",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "astro": "^4.0.0"
  }
}
JSON_EOF

cat << 'MJS_EOF' > astro.config.mjs
import { defineConfig } from 'astro/config';
export default defineConfig({
  srcDir: "./src",
  publicDir: "./public",
  outDir: "./dist",
  server: { port: 3000 }
});
MJS_EOF

# 4. Catálogo (Centro de Comando)
cat <<EOF > src/data/catalog.json
{
    "ALFAJORES": {
        "variants": {
            "ALFAJOR X5": { "desc": "Clásicos y suaves.", "price": "$16.000", "min": 1, "spec": "5 UNIDADES" },
            "ALFAJOR X6": { "desc": "Caja premium variada.", "price": "$20.000", "min": 1, "spec": "6 UNIDADES" },
            "ALFAJOR X50": { "desc": "Ideal para banquetes.", "price": "$100.000", "min": 50, "spec": "50 UNIDADES" }
        }
    },
    "POSTRES": {
        "variants": {
            "MARIA LUISA": { "desc": "Bizcochuelo con mora y arequipe.", "price": "$45.000", "min": 1, "spec": "TORTA ENTERA" }
        }
    },
    "BROWNIES": {
        "variants": {
            "BROWNIE X50": { "desc": "Cacao gourmet melcochudo.", "price": "$100.000", "min": 50, "spec": "50 UNIDADES" }
        }
    }
}
EOF

# 4.5. Backend Cerebro (FastAPI con filtro corporativo)
cat << 'PY_EOF' > main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def leer_catalogo():
    with open("src/data/catalog.json", "r") as f:
        return json.load(f)

@app.get("/api/catalog")
async def get_catalog():
    return leer_catalogo()

@app.get("/api/catalog/eventos")
async def get_eventos():
    data = leer_catalogo()
    eventos = {}
    for cat, content in data.items():
        # Filtra solo productos con min >= 20
        v_eventos = {k: v for k, v in content["variants"].items() if v.get("min", 0) >= 20}
        if v_eventos:
            eventos[cat] = {"variants": v_eventos}
    return eventos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
PY_EOF

cat << 'EOF' > src/pages/index.astro
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>SUGARRUSH.WORLD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root[data-theme="dark"] {
            --jako-bg: rgba(190, 151, 183, 0.95); 
            --jako-text: #ffffff;
            --gradient-start: rgba(0, 140, 255, 0.025);
            --gradient-mid: rgba(10, 10, 10, 0.9);
            --gradient-end: #222222;
        }
        body { overscroll-behavior: none; background-color: var(--jako-bg); }
        #page-bg-overlay { background: radial-gradient(circle at 50% 50%, var(--gradient-start) 35%, var(--gradient-mid) 85%, var(--gradient-end) 95%); }
        .glass-footer, .glass-header { backdrop-filter: blur(40px) saturate(120%); }
        .img-glow-transition { transition: background-image 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s ease-out; }
    </style>
</head>
<body class="antialiased overflow-hidden h-screen w-screen text-white font-sans">
    <div id="page-bg-overlay" class="fixed inset-0 z-10 flex flex-col justify-between">
        <header class="w-full shrink-0 z-50 py-5 px-9 flex justify-center items-center border-b border-white/10">
            <div class="w-full max-w-[675px] flex items-center justify-between">
                <button onclick="navegarCategoria(-1)" class="p-3 opacity-50 hover:opacity-100">◀</button>
                <div class="flex flex-col items-center gap-1"> 
                    <span class="text-[17px] tracking-[0.3em] uppercase">SUGARRUSH</span>
                    <span id="sugar-category-indicator" class="text-[7.5px] font-mono opacity-40">ALFAJORES</span>
                </div>
                <button onclick="navegarCategoria(1)" class="p-3 opacity-50 hover:opacity-100">▶</button>
            </div>
        </header>

        <main id="main-vault" class="flex-1 flex flex-col items-center justify-center relative z-10 p-6">
            <div id="artepanel-pack-container" onclick="adquirirNodoSugar()" class="w-[300px] h-[300px] rounded-full overflow-hidden cursor-pointer hover:scale-[1.03] transition-transform">
                <div id="artepanel-mask-wrapper" class="w-full h-full bg-cover bg-center img-glow-transition" style="background-image: url('img/alfajores_x5.jpg');"></div>
            </div>
            <div class="mt-6 text-center max-w-[380px]">
                <p id="sugar-variant-desc" class="text-xs text-white/70">Cargando...</p>
                <div class="mt-3 flex justify-center gap-3 font-mono text-[9px] text-white/40">
                    <span id="sugar-variant-spec">-</span>
                    <span>|</span>
                    <span id="sugar-variant-price" class="font-bold">-</span>
                </div>
            </div>
        </main>

        <footer class="w-full shrink-0 z-50 py-5 px-9 flex justify-center items-center border-t border-white/10">
            <div class="w-full max-w-[675px] flex items-center justify-between">
                <button onclick="navigateVariant(-1)" class="opacity-50 hover:opacity-100 p-3">◀</button>
                <div id="laser-variant-title-footer" class="text-[10px] tracking-[0.25em] uppercase">ALFAJOR X5</div>
                <button onclick="navigateVariant(1)" class="opacity-50 hover:opacity-100 p-3">▶</button>
            </div>
        </footer>
    </div>
<script>
        let currentCategory = 'ALFAJORES';
        let currentVariant = 'ALFAJOR X5';
        let catalogoRemoto = null;

        const $ = (id) => document.getElementById(id);

        async function cargarCatalogo() {
            try {
                // Intenta conectar al backend
                const response = await fetch('http://127.0.0.1:8000/api/catalog');
                if (!response.ok) throw new Error('Servidor no responde');
                catalogoRemoto = await response.json();
                actualizarInterfaz();
            } catch (error) {
                console.error("Error:", error);
                document.getElementById('sugar-variant-desc').textContent = "Esperando servidor...";
            }
        }

        function actualizarInterfaz() {
            if (!catalogoRemoto) return;
            const data = catalogoRemoto[currentCategory].variants[currentVariant];
            $('sugar-category-indicator').textContent = currentCategory;
            $('sugar-variant-desc').textContent = data.desc;
            $('sugar-variant-spec').textContent = data.spec;
            $('sugar-variant-price').textContent = data.price;
            $('laser-variant-title-footer').textContent = currentVariant;
        }

        document.addEventListener('DOMContentLoaded', cargarCatalogo);
    </script>
</body>
</html>
EOF

# 6. Build
echo -e "\n${YELLOW}[5/5] Ejecutando build final...${NC}"
if [ ! -d "node_modules/astro" ]; then
    npm install
fi

npx astro sync
npx astro build

echo -e "${CYAN}🎉 Entorno rush-core listo. Recuerda ejecutar 'uvicorn main:app --reload'${NC}"
