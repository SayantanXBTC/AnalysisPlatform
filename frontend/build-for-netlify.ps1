# Build script for Netlify deployment (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Techathon Frontend for Netlify" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm install failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Building production bundle..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "The 'dist' folder is ready for deployment." -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://app.netlify.com/drop" -ForegroundColor White
Write-Host "2. Drag the 'dist' folder to the page" -ForegroundColor White
Write-Host "3. Wait for deployment to complete" -ForegroundColor White
Write-Host "4. Copy your Netlify URL" -ForegroundColor White
Write-Host ""
Write-Host "Opening dist folder..." -ForegroundColor Yellow
Start-Process explorer.exe -ArgumentList (Get-Location).Path\dist

Write-Host ""
Read-Host "Press Enter to exit"