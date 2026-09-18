$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Edge-Cloud Inventory Intelligence Platform" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python environment
if (!(Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "ERROR: Python virtual environment not found." -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
$pg = Test-NetConnection -ComputerName localhost -Port 5432 -WarningAction SilentlyContinue

if (!$pg.TcpTestSucceeded) {
    Write-Host "ERROR: PostgreSQL is not running on port 5432." -ForegroundColor Red
    Write-Host "Start PostgreSQL and run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "PostgreSQL: OK" -ForegroundColor Green

# Apply latest migrations
Write-Host "Checking database migrations..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -m alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Database migration failed." -ForegroundColor Red
    exit 1
}

Write-Host "Database: OK" -ForegroundColor Green

# Check frontend dependencies
if (!(Test-Path ".\frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location ".\frontend"
    npm install
    Set-Location $ProjectRoot
}

Write-Host ""
Write-Host "Starting backend..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot'; .\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload"
)

Start-Sleep -Seconds 2

Write-Host "Starting frontend..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$ProjectRoot\frontend'; npm run dev"
)

Start-Sleep -Seconds 4

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " PROJECT STARTED SUCCESSFULLY" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard : http://localhost:5173" -ForegroundColor Cyan
Write-Host "API       : http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs  : http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening dashboard..." -ForegroundColor Yellow

Start-Process "http://localhost:5173"
