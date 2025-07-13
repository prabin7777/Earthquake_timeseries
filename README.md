#!/bin/bash
#
# =============================================================
# |   Setup Script for macOS & Linux                          |
# |   Earthquake Early Warning System Data Visualization App  |
# =============================================================
#
# This script automates the backend setup process.
# It will:
# 1. Check if python3 is installed.
# 2. Create a virtual environment named 'venv'.
# 3. Install the required Python packages into the venv.
# 4. Provide clear instructions for the final steps.
#
# To run:
# 1. Save this script as 'setup.sh' in your project root.
# 2. Make it executable: chmod +x setup.sh
# 3. Run it: ./setup.sh
#

echo "--- Starting Backend Setup for macOS/Linux ---"

# --- 1. Check for Python 3 ---
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: python3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi
echo "✅ Python 3 found."

# --- 2. Create Virtual Environment ---
echo "⚙️  Creating virtual environment 'venv'..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment."
    exit 1
fi
echo "✅ Virtual environment created."

# --- 3. Install Dependencies ---
echo "📦 Installing dependencies using pip..."
# We call the pip from the newly created venv directly to ensure packages are installed there.
./venv/bin/pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install one or more dependencies."
    echo "   Please check your network connection and try again."
    echo "   Note: Cartopy may require additional system dependencies. See https://scitools.org.uk/cartopy/docs/latest/installing.html"
    exit 1
fi
echo "✅ All dependencies installed successfully."

# --- 4. Final Instructions ---
echo ""
echo "--- 🎉 Setup Complete! ---"
echo ""
echo "Your next steps are:"
echo "1. Activate the virtual environment by running:"
echo "   source venv/bin/activate"
echo ""
echo "2. Once activated, run the Flask server:"
echo "   cd backend_serve"
echo "   python app.py"
echo ""
echo "The server will then be available at http://127.0.0.1:5000/"


# =============================================================
# |   Setup Script for Windows                                |
# |   Earthquake Early Warning System Data Visualization App  |
# =============================================================
#
# To use this on Windows:
# 1. Copy the text from the '@echo off' line to the end.
# 2. Save it in a new file named 'setup.bat' in your project root.
# 3. Double-click 'setup.bat' or run it from your command prompt.
#

: <<'BATCH_SCRIPT'
@echo off
cls
echo --- Starting Backend Setup for Windows ---

:: --- 1. Check for Python ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Error: python is not installed or not in your system's PATH.
    echo   Please install Python 3.8+ and ensure it's added to your PATH.
    pause
    goto :eof
)
echo V Python found.

:: --- 2. Create Virtual Environment ---
echo O Creating virtual environment 'venv'...
python -m venv venv
if %errorlevel% neq 0 (
    echo X Error: Failed to create virtual environment.
    pause
    goto :eof
)
echo V Virtual environment created.

:: --- 3. Install Dependencies ---
echo O Installing dependencies using pip...
.\venv\Scripts\pip.exe install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy
if %errorlevel% neq 0 (
    echo X Error: Failed to install one or more dependencies.
    echo   Please check your network connection and try again.
    echo   Note: Cartopy may require additional system dependencies. See https://scitools.org.uk/cartopy/docs/latest/installing.html
    pause
    goto :eof
)
echo V All dependencies installed successfully.

:: --- 4. Final Instructions ---
echo.
echo --- --- --- --- --- --- ---
echo --- Setup Complete! ---
echo --- --- --- --- --- --- ---
echo.
echo Your next steps are:
echo 1. Activate the virtual environment by running:
echo    .\venv\Scripts\activate
echo.
echo 2. Once activated, run the Flask server:
echo    cd backend_serve
echo    python app.py
echo.
echo The server will then be available at http://127.0.0.1:5000/
echo.
pause
goto :eof
BATCH_SCRIPT
