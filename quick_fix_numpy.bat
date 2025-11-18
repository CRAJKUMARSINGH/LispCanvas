@echo off
echo LispCanvas NumPy Quick Fix
echo =========================
echo This script will fix the NumPy compatibility issue
echo by downgrading to a compatible version.
echo.

echo Step 1: Uninstalling current NumPy...
pip uninstall numpy -y

echo.
echo Step 2: Installing compatible NumPy version...
pip install numpy==1.24.3

echo.
echo Step 3: Verifying the fix...
python -c "import numpy as np; print('Success! NumPy version:', np.__version__); print('Basic operation result:', np.pi * 2)"

echo.
echo Fix complete! You can now run your LispCanvas application.
echo Press any key to exit...
pause >nul