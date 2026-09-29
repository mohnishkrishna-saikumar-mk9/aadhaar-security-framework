@echo off
echo ========================================================
echo        Identity Shield Verification Portal
echo ========================================================
echo.
echo [1/3] Setting up environment variables...
set PYTHONIOENCODING=utf-8

echo [2/3] Starting the FastAPI backend server (loading AI models)...
:: Start the server in the background
start /B python api/main.py

:: Give the server 7 seconds to load DeepFace and Scikit-learn models into memory
timeout /t 7 /nobreak >nul

echo [3/3] Launching the Frontend Interface...
start "" "frontend\index.html"

echo.
echo ========================================================
echo System is running! 
echo Keep this command prompt window open to keep the 
echo backend server alive.
echo.
echo To STOP the server, press Ctrl+C in this window.
echo ========================================================
