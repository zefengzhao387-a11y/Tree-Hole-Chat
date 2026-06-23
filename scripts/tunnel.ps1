# 内网穿透：Cloudflare Quick Tunnel（比 loca.lt 在国内更稳定）
# 用法：先确保前端 npm run dev (5173) 与后端 uvicorn (8000) 已启动，再运行：
#   powershell -ExecutionPolicy Bypass -File scripts\tunnel.ps1

$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root "tools\cloudflared.exe"

if (-not (Test-Path $exe)) {
  Write-Host "正在下载 cloudflared..."
  New-Item -ItemType Directory -Force -Path (Split-Path $exe) | Out-Null
  Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile $exe
}

Write-Host "启动隧道 -> http://127.0.0.1:5173"
Write-Host "请等待下方出现 https://xxxx.trycloudflare.com 链接"
Write-Host ""

& $exe tunnel --url http://127.0.0.1:5173
