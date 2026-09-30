#!/usr/bin/env bash

echo "=========================================="
echo " Launching FloodMesh AI Command Center    "
echo "=========================================="

# 1. Clean up old processes on ports 8000 and 3000
fuser -k 8000/tcp 2>/dev/null || pkill -f uvicorn || true
fuser -k 3000/tcp 2>/dev/null || pkill -f vite || true
sleep 1

# 2. Start FastAPI Backend (Port 8000)
echo "-> Starting FastAPI Backend..."
cd ~/floodmesh-ai/backend
nohup .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > uvicorn.log 2>&1 &

# 3. Start React Frontend (Port 3000) in background
echo "-> Starting React Command Center..."
cd ~/floodmesh-ai/frontend
nohup npm run dev > vite.log 2>&1 &

# 4. Wait for both servers to finish booting
echo "-> Waiting for servers to initialize..."
sleep 4

# 5. Now open the browser (Vite is now ready!)
echo "-> Opening Dashboard in Browser..."
xdg-open http://localhost:3000 &> /dev/null || true

echo "=========================================="
echo " [OK] FloodMesh AI is fully operational!"
echo " Backend:   http://127.0.0.1:8000"
echo " Dashboard: http://localhost:3000"
echo "=========================================="
