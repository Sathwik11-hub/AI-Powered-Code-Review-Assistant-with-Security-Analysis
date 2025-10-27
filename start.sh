#!/bin/bash
# Start both frontend and backend servers

echo "🚀 Starting AI Code Review Assistant..."
echo ""

# Check if in the root directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Start backend
echo "📦 Starting backend server on http://localhost:8000..."
cd backend
uvicorn app:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend dev server on http://localhost:5173..."
cd frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servers started successfully!"
echo ""
echo "📝 Backend API: http://localhost:8000"
echo "🌐 Frontend UI: http://localhost:5173"
echo ""
echo "📋 Backend PID: $BACKEND_PID"
echo "📋 Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend: backend/backend.log"
echo "  Frontend: frontend/frontend.log"
echo ""

# Wait for user to stop
echo "Press Ctrl+C to stop all servers..."
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '✅ Servers stopped'; exit 0" INT

# Keep script running
wait
