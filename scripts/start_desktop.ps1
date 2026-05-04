$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Desktop = Join-Path $Root "desktop"
$Python = "C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path $Python)) {
  $Python = "python"
}

$apiListening = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if (-not $apiListening) {
  Start-Process -FilePath $Python `
    -ArgumentList "-m", "uvicorn", "api.app.main:app", "--host", "127.0.0.1", "--port", "8000" `
    -WorkingDirectory $Root `
    -WindowStyle Hidden
}

Push-Location $Desktop
try {
  npm run dev:electron
}
finally {
  Pop-Location
}
