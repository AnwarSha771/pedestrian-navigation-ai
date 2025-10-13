# Quick Setup Script for Windows PowerShell
# Run this to set up the project quickly

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🦯 Pedestrian Navigation AI - Quick Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install some dependencies" -ForegroundColor Red
    Write-Host "Try running: pip install -r requirements.txt" -ForegroundColor Yellow
}

# Test imports
Write-Host ""
Write-Host "Testing installations..." -ForegroundColor Yellow
$testScript = @"
try:
    import cv2
    import numpy
    import ultralytics
    import torch
    print('✓ All core libraries imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
"@

python -c $testScript

# Create data directory
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}
if (-not (Test-Path "data/sample_videos")) {
    New-Item -ItemType Directory -Path "data/sample_videos" | Out-Null
}
Write-Host "✓ Directories created" -ForegroundColor Green

# Download YOLOv8 model (will happen automatically on first run)
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run demo: python demo.py" -ForegroundColor White
Write-Host "2. Or run main app: python main.py" -ForegroundColor White
Write-Host "3. For help: python main.py --help" -ForegroundColor White
Write-Host ""
Write-Host "Note: YOLOv8 model will be downloaded automatically on first run (~6MB)" -ForegroundColor Cyan
Write-Host ""
