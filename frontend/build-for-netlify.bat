@echo off
echo ========================================
echo Building Techathon Frontend for Netlify
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed!
        pause
        exit /b 1
    )
)

echo.
echo Building production bundle...
call npm run build

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo The 'dist' folder is ready for deployment.
echo.
echo Next steps:
echo 1. Go to https://app.netlify.com/drop
echo 2. Drag the 'dist' folder to the page
echo 3. Wait for deployment to complete
echo 4. Copy your Netlify URL
echo.
echo Opening dist folder...
explorer dist

echo.
pause