#!/bin/bash
# ============================================
#  解忧树洞 - 一键启动脚本
# ============================================

echo "🌳 正在启动解忧树洞系统..."

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 backend/.env 文件，从模板创建..."
    cp backend/.env.example backend/.env
    echo "📝 请编辑 backend/.env 文件，填入你的 DeepSeek API Key"
fi

# 启动后端
echo "🚀 启动后端服务..."
cd backend
pip install -r requirements.txt -q 2>/dev/null
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm install --silent 2>/dev/null
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 系统启动完成！"
echo "   后端 API:  http://localhost:8000/docs"
echo "   前端页面:  http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获退出信号，清理进程
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
