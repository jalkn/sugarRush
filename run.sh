#!/bin/bash

# ==============================================================================
# SUGARRUSH - EJECUTOR PARALELO (FRONTEND + BACKEND)
# ==============================================================================

echo "🚀 Iniciando Ecosistema SugaRush..."

# Lanzar FastAPI en segundo plano
echo "🌐 Iniciando Backend (FastAPI)..."
uvicorn main:app --port 8000 --reload &

# Lanzar Astro en segundo plano
echo "🎨 Iniciando Frontend (Astro)..."
npm run dev &

# Mantener el script vivo y capturar señales de cierre
trap "kill 0" EXIT
wait