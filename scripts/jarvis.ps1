param(
  [ValidateSet("start", "stop", "restart", "status")]
  [string]$Action = "status",

  [switch]$NoElectron
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Desktop = Join-Path $Root "desktop"
$Runtime = Join-Path $Root "runtime"
$PidDir = Join-Path $Runtime "pids"
$LogDir = Join-Path $Runtime "logs"

New-Item -ItemType Directory -Force -Path $PidDir, $LogDir | Out-Null

$ApiPort = 8000
$UiPort = 5173
$OllamaPort = 11434

function Write-Jarvis {
  param([string]$Message)
  Write-Host "[JARVIS] $Message"
}

function Get-PythonPath {
  $Bundled = "C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  if (Test-Path $Bundled) {
    return $Bundled
  }
  $Command = Get-Command python -ErrorAction SilentlyContinue
  if ($Command) {
    return $Command.Source
  }
  throw "Python was not found. Install Python or update Get-PythonPath in scripts\jarvis.ps1."
}

function Get-OllamaPath {
  $Command = Get-Command ollama -ErrorAction SilentlyContinue
  if ($Command) {
    return $Command.Source
  }

  $Candidates = @(
    "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe",
    "$env:LOCALAPPDATA\Ollama\ollama.exe",
    "C:\Program Files\Ollama\ollama.exe"
  )

  foreach ($Candidate in $Candidates) {
    if ($Candidate -and (Test-Path $Candidate)) {
      return $Candidate
    }
  }

  return $null
}

function Get-PortOwners {
  param([int]$Port)
  $Connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  @($Connections | Select-Object -ExpandProperty OwningProcess -Unique)
}

function Test-Port {
  param([int]$Port)
  return [bool](Get-PortOwners -Port $Port)
}

function Wait-Http {
  param(
    [string]$Url,
    [int]$TimeoutSeconds = 30
  )

  $Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $Deadline) {
    try {
      Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 2 | Out-Null
      return $true
    }
    catch {
      Start-Sleep -Milliseconds 500
    }
  }
  return $false
}

function Save-Pid {
  param(
    [string]$Name,
    [int]$ProcessId
  )
  Set-Content -Path (Join-Path $PidDir "$Name.pid") -Value $ProcessId -Encoding ascii
}

function Get-SavedPid {
  param([string]$Name)
  $Path = Join-Path $PidDir "$Name.pid"
  if (-not (Test-Path $Path)) {
    return $null
  }
  $Value = (Get-Content $Path -ErrorAction SilentlyContinue | Select-Object -First 1)
  if ($Value -match "^\d+$") {
    return [int]$Value
  }
  return $null
}

function Remove-SavedPid {
  param([string]$Name)
  Remove-Item -LiteralPath (Join-Path $PidDir "$Name.pid") -Force -ErrorAction SilentlyContinue
}

function Stop-SavedProcess {
  param([string]$Name)
  $SavedProcessId = Get-SavedPid -Name $Name
  if ($SavedProcessId) {
    $Process = Get-Process -Id $SavedProcessId -ErrorAction SilentlyContinue
    if ($Process) {
      Stop-Process -Id $SavedProcessId -Force
    }
  }
  Remove-SavedPid -Name $Name
}

function Stop-PortOwners {
  param(
    [int]$Port,
    [string]$Label
  )

  $Owners = Get-PortOwners -Port $Port
  foreach ($Owner in $Owners) {
    $Process = Get-Process -Id $Owner -ErrorAction SilentlyContinue
    if ($Process) {
      Write-Jarvis "Stopping $Label pid=$Owner"
      Stop-Process -Id $Owner -Force
    }
  }
}

function Start-Ollama {
  if (Test-Port -Port $OllamaPort) {
    Write-Jarvis "Ollama already running on port $OllamaPort."
    return
  }

  $Ollama = Get-OllamaPath
  if (-not $Ollama) {
    Write-Jarvis "Ollama executable was not found. Start Ollama manually or add it to PATH."
    return
  }

  $OutLog = Join-Path $LogDir "ollama.out.log"
  $ErrLog = Join-Path $LogDir "ollama.err.log"
  $Process = Start-Process -FilePath $Ollama `
    -ArgumentList "serve" `
    -WorkingDirectory $Root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -PassThru
  Save-Pid -Name "ollama" -ProcessId $Process.Id

  if (Wait-Http -Url "http://127.0.0.1:$OllamaPort/api/tags" -TimeoutSeconds 20) {
    Write-Jarvis "Ollama started on port $OllamaPort."
  }
  else {
    Write-Jarvis "Ollama start requested, but health check timed out."
  }
}

function Start-Api {
  if (Test-Port -Port $ApiPort) {
    Write-Jarvis "Backend API already running on port $ApiPort."
    return
  }

  $Python = Get-PythonPath
  $OutLog = Join-Path $LogDir "api.out.log"
  $ErrLog = Join-Path $LogDir "api.err.log"
  $Process = Start-Process -FilePath $Python `
    -ArgumentList "-m", "uvicorn", "api.app.main:app", "--host", "127.0.0.1", "--port", "$ApiPort" `
    -WorkingDirectory $Root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -PassThru
  Save-Pid -Name "api" -ProcessId $Process.Id

  if (Wait-Http -Url "http://127.0.0.1:$ApiPort/health" -TimeoutSeconds 30) {
    Write-Jarvis "Backend API started on port $ApiPort."
  }
  else {
    Write-Jarvis "Backend API start requested, but health check timed out."
  }
}

function Start-Ui {
  if (Test-Port -Port $UiPort) {
    Write-Jarvis "Vite UI already running on port $UiPort."
    return
  }

  $Npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
  if (-not $Npm) {
    $Npm = Get-Command npm -ErrorAction SilentlyContinue
  }
  if (-not $Npm) {
    throw "npm was not found."
  }

  $OutLog = Join-Path $LogDir "ui.out.log"
  $ErrLog = Join-Path $LogDir "ui.err.log"
  $Process = Start-Process -FilePath $Npm.Source `
    -ArgumentList "run", "dev" `
    -WorkingDirectory $Desktop `
    -WindowStyle Hidden `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -PassThru
  Save-Pid -Name "ui" -ProcessId $Process.Id

  if (Wait-Http -Url "http://127.0.0.1:$UiPort" -TimeoutSeconds 30) {
    Write-Jarvis "Vite UI started on port $UiPort."
  }
  else {
    Write-Jarvis "Vite UI start requested, but health check timed out."
  }
}

function Start-Electron {
  if ($NoElectron) {
    Write-Jarvis "Electron launch skipped."
    return
  }

  $Electron = Join-Path $Desktop "node_modules\.bin\electron.cmd"
  if (-not (Test-Path $Electron)) {
    Write-Jarvis "Electron executable was not found. Run npm install in desktop first."
    return
  }

  $env:JARVIS_DESKTOP_MODE = "dev"
  $OutLog = Join-Path $LogDir "electron.out.log"
  $ErrLog = Join-Path $LogDir "electron.err.log"
  $Process = Start-Process -FilePath $Electron `
    -ArgumentList "." `
    -WorkingDirectory $Desktop `
    -WindowStyle Hidden `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -PassThru
  Save-Pid -Name "electron" -ProcessId $Process.Id
  Write-Jarvis "Electron desktop app started."
}

function Stop-ElectronProcesses {
  Stop-SavedProcess -Name "electron"

  $EscapedRoot = [Regex]::Escape([string]$Root)
  $Processes = Get-CimInstance Win32_Process -Filter "name = 'electron.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match $EscapedRoot }

  foreach ($Process in $Processes) {
    Write-Jarvis "Stopping Electron pid=$($Process.ProcessId)"
    Stop-Process -Id $Process.ProcessId -Force -ErrorAction SilentlyContinue
  }
}

function Stop-Jarvis {
  Stop-ElectronProcesses
  Stop-SavedProcess -Name "ui"
  Stop-PortOwners -Port $UiPort -Label "Vite UI"
  Stop-SavedProcess -Name "api"
  Stop-PortOwners -Port $ApiPort -Label "Backend API"
  Stop-SavedProcess -Name "ollama"

  $OllamaProcesses = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
  foreach ($Process in $OllamaProcesses) {
    Write-Jarvis "Stopping Ollama pid=$($Process.Id)"
    Stop-Process -Id $Process.Id -Force
  }
}

function Start-Jarvis {
  Start-Ollama
  Start-Api
  Start-Ui
  Start-Electron
}

function Show-Status {
  $Api = Test-Port -Port $ApiPort
  $Ui = Test-Port -Port $UiPort
  $Ollama = Test-Port -Port $OllamaPort
  $ElectronPid = Get-SavedPid -Name "electron"
  $ElectronRunning = $false
  if ($ElectronPid) {
    $ElectronRunning = [bool](Get-Process -Id $ElectronPid -ErrorAction SilentlyContinue)
  }

  [PSCustomObject]@{
    api = if ($Api) { "on : http://127.0.0.1:$ApiPort" } else { "off" }
    ui = if ($Ui) { "on : http://127.0.0.1:$UiPort" } else { "off" }
    ollama = if ($Ollama) { "on : http://127.0.0.1:$OllamaPort" } else { "off" }
    electron = if ($ElectronRunning) { "on : pid=$ElectronPid" } else { "unknown/off" }
    logs = $LogDir
  } | Format-List
}

switch ($Action) {
  "start" {
    Start-Jarvis
    Show-Status
  }
  "stop" {
    Stop-Jarvis
    Show-Status
  }
  "restart" {
    Stop-Jarvis
    Start-Sleep -Seconds 1
    Start-Jarvis
    Show-Status
  }
  "status" {
    Show-Status
  }
}
