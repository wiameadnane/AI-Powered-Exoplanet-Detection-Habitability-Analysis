@echo off
echo Installing required packages for Exoplanet Detection...
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available. Please install Python with pip.
    pause
    exit /b 1
)

echo Installing packages from requirements.txt...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Some packages failed to install.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ All packages installed successfully!
echo You can now run the Jupyter notebook.
echo.
pause
