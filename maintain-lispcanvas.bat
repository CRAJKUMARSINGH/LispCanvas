@echo off
REM maintain-lispcanvas.bat
REM Safe maintenance script for LispCanvas
setlocal enabledelayedexpansion

set REPO_NAME=LispCanvas
echo Starting maintenance for %REPO_NAME%...

REM 1. UPDATE
echo Pulling latest changes...
git checkout main 2>nul || git checkout master 2>nul
git pull --ff-only 2>nul || echo No remote changes

REM 2. INITIALIZE IF EMPTY
if not exist "README.md" (
    echo Initializing repository structure...
    call :init_repo
)

REM 3. OPTIMIZE
echo Optimizing code...
if exist "frontend\package.json" (
    where npm >nul 2>&1
    if !errorlevel! equ 0 (
        cd frontend && call npm install >nul 2>&1 && cd ..
    )
)

if exist "requirements.txt" (
    where pip >nul 2>&1
    if !errorlevel! equ 0 (
        pip install -r requirements.txt >nul 2>&1
    )
)

REM 4. TEST
echo Running tests...
if exist "backend\app\main.py" (
    python -c "import sys; sys.path.append('backend'); from app.main import app" 2>nul
)

REM 5. CLEAN CACHE
echo Clearing caches...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul

REM 6. PUSH
echo Pushing changes...
git add .
git diff-index --quiet HEAD -- 2>nul
if !errorlevel! neq 0 (
    git commit -m "chore: maintenance update"
    git push origin main 2>nul || git push origin master 2>nul
)

echo Maintenance complete!
goto :eof

:init_repo
call :create_files
call :create_dirs
if not exist ".git" git init
git add .
git commit -m "feat: initialize LispCanvas structure" 2>nul
goto :eof

:create_files
echo Creating README...
(
echo # LispCanvas
echo.
echo Canvas-based civil engineering design system with DXF export.
echo.
echo ## Modules
echo 1. Bridge Design
echo 2. Rectangle Column with Footing
echo 3. Road L-Section
echo 4. Road Plan
echo 5. Road Cross Section
echo 6. PMGSY Road
echo 7. Lintel
echo 8. Sunshed
echo 9. T-Beam/L-Beam
echo 10. Staircase
) > README.md

(
echo fastapi
echo uvicorn
echo ezdxf
echo numpy
) > requirements.txt

(
echo node_modules/
echo __pycache__/
echo *.pyc
echo .env
echo venv/
) > .gitignore
goto :eof

:create_dirs
mkdir frontend\src\components 2>nul
mkdir frontend\src\modules 2>nul
mkdir frontend\src\lib 2>nul
mkdir backend\app\modules 2>nul
mkdir backend\app\lib 2>nul
mkdir shared\config 2>nul
mkdir templates 2>nul
mkdir docs 2>nul
mkdir samples 2>nul

REM Create backend main.py
(
echo from fastapi import FastAPI
echo from fastapi.middleware.cors import CORSMiddleware
echo.
echo app = FastAPI^(^)
echo.
echo app.add_middleware^(
echo     CORSMiddleware,
echo     allow_origins=["*"],
echo     allow_credentials=True,
echo     allow_methods=["*"],
echo     allow_headers=["*"]
echo ^)
echo.
echo @app.get^("/")
echo def read_root^(^):
echo     return {"message": "LispCanvas API"}
) > backend\app\main.py

REM Create frontend package.json
(
echo {
echo   "name": "lispcanvas-frontend",
echo   "version": "0.1.0",
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0"
echo   },
echo   "scripts": {
echo     "start": "react-scripts start",
echo     "build": "react-scripts build"
echo   }
echo }
) > frontend\package.json

REM Create module structure
call :create_modules
goto :eof

:create_modules
set MODULES=bridge rectangle_column road_lsection road_plan road_cross_section pmgsy_road lintel sunshed tbeam_lbeam staircase

for %%m in (%MODULES%) do (
    mkdir frontend\src\modules\%%m 2>nul
    mkdir backend\app\modules\%%m 2>nul
    
    REM Frontend module
    (
    echo import React from 'react';
    echo.
    echo const %%mModule = ^(^) =^> {
    echo   return ^(
    echo     ^<div^>
    echo       ^<h2^>%%m Module^</h2^>
    echo       ^<canvas width="800" height="600"^>^</canvas^>
    echo     ^</div^>
    echo   ^);
    echo };
    echo.
    echo export default %%mModule;
    ) > frontend\src\modules\%%m\%%m.jsx
    
    REM Backend module
    echo # %%m module > backend\app\modules\%%m\__init__.py
    
    (
    echo from fastapi import APIRouter
    echo.
    echo router = APIRouter^(prefix="/%%m", tags=["%%m"]^)
    echo.
    echo @router.get^("/")
    echo def get_%%m^(^):
    echo     return {"module": "%%m", "status": "ready"}
    ) > backend\app\modules\%%m\routes.py
)
goto :eof
