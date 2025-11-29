@echo off
echo ========================================
echo STRUCTURAL DESIGN SUITE - INTEGRATION TEST
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Running integration tests...
python test_integration.py
echo.

echo ========================================
echo Test complete! Check results above.
echo ========================================
pause
