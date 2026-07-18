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

# 2. Estructura base
mkdir -p src/data img svg public/api src/layouts
rm -rf src/pages

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
        "defaultVariant": "ALFAJOR X5",
        "variants": {
            "ALFAJOR X5": {
                "label": "SUGARRUSH ALFAJORES X5",
                "price": "$16.000",
                "recipe": [{"item": "harina", "qty": 250, "unit": "g"}],
                "id": "SR-ALF-X5"
            }
        }
    }
}
EOF

# 4.5. Backend Cerebro (FastAPI Endpoint con edición dinámica)
cat << 'PY_EOF' > main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/catalog")
async def get_catalog():
    with open("src/data/catalog.json", "r") as f:
        return json.load(f)

@app.post("/api/catalog")
async def update_catalog(request: Request):
    new_data = await request.json()
    with open("src/data/catalog.json", "w") as f:
        json.dump(new_data, f, indent=4)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
PY_EOF

# 5. UI Base (Frontend con lógica de fetch integrada)
cat <<EOF > src/layouts/index.html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SUGARRUSH.WORLD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root { --jako-bg: rgba(161, 106, 151, 0.95); }
        body { background-color: var(--jako-bg); font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
</head>
<body class="h-screen flex flex-col items-center justify-center text-white">
    <header class="glass-header w-full p-5 text-center">
        <span class="text-[14px] tracking-[0.3em] uppercase font-sans">SUGARRUSH</span>
    </header>
    <main class="flex-1 flex flex-col items-center justify-center">
        <div id="artepanel" class="w-64 h-64 rounded-full bg-black/20 backdrop-blur flex items-center justify-center">
            <!-- Interacción futura aquí -->
        </div>
    </main>
    <script>
        console.log("Sistema SugarRush inicializado.");
        fetch('http://localhost:8000/api/catalog')
            .then(res => res.json())
            .then(data => console.log("Catálogo dinámico cargado desde FastAPI:", data))
            .catch(err => console.error("Error conectando con el Centro de Comando:", err));
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

if [ -f "dist/index.html" ]; then
    cp dist/index.html ./index.html
    echo -e "${GREEN}✔ index.html extraído a la raíz.${NC}"
fi

echo -e "${CYAN}🎉 Entorno rush-core listo. Recuerda ejecutar 'uvicorn main:app --reload'${NC}"
