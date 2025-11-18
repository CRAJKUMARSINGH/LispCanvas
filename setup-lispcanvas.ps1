# setup-lispcanvas.ps1
# Complete setup script for LispCanvas project

Write-Host "🏗️ Setting up LispCanvas project structure..." -ForegroundColor Cyan

# Create directory structure
$dirs = @(
    "frontend\src\components",
    "frontend\src\modules\bridge",
    "frontend\src\modules\rectangle_column",
    "frontend\src\modules\road_lsection",
    "frontend\src\modules\road_plan",
    "frontend\src\modules\road_cross_section",
    "frontend\src\modules\pmgsy_road",
    "frontend\src\modules\lintel",
    "frontend\src\modules\sunshed",
    "frontend\src\modules\tbeam_lbeam",
    "frontend\src\modules\staircase",
    "frontend\src\lib",
    "frontend\public",
    "backend\app\modules\bridge",
    "backend\app\modules\rectangle_column",
    "backend\app\modules\road_lsection",
    "backend\app\modules\road_plan",
    "backend\app\modules\road_cross_section",
    "backend\app\modules\pmgsy_road",
    "backend\app\modules\lintel",
    "backend\app\modules\sunshed",
    "backend\app\modules\tbeam_lbeam",
    "backend\app\modules\staircase",
    "backend\app\lib",
    "shared\config",
    "templates\dxf",
    "docs",
    "samples",
    "data"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "✅ Directory structure created" -ForegroundColor Green

# Create README.md
@"
# LispCanvas

A canvas-based civil engineering design system for generating professional drawings with DXF export.

## Modules

1. **Bridge Design** - GAD drawings from parameters
2. **Rectangle Column with Footing** - Structural element design
3. **Road L-Section** - Longitudinal road profiles
4. **Road Plan** - Plan view road alignments
5. **Road Cross Section** - Transverse road profiles
6. **PMGSY Road** - Rural road specifications
7. **Lintel** - Structural beam design
8. **Sunshed** - Architectural element design
9. **T-Beam/L-Beam** - Structural beam design
10. **Staircase** - Structural stair design

## Tech Stack

- **Frontend**: React + HTML5 Canvas
- **Backend**: FastAPI + Python
- **Output**: DXF, PDF, PNG

## Quick Start

### Backend
``````
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
``````

### Frontend
``````
cd frontend
npm install
npm start
``````

## API Endpoints

- GET `/` - API status
- GET `/bridge` - Bridge module
- GET `/rectangle_column` - Column module
- (Additional endpoints for each module)

## Development

Each module consists of:
- Frontend React component with canvas drawing
- Backend API for calculations and DXF generation
- Shared configuration for styling

## License

MIT
"@ | Out-File -FilePath "README.md" -Encoding UTF8

Write-Host "✅ README.md created" -ForegroundColor Green

# Create requirements.txt
@"
fastapi==0.104.1
uvicorn[standard]==0.24.0
ezdxf==1.1.3
numpy==1.26.2
pandas==2.1.3
python-dotenv==1.0.0
python-multipart==0.0.6
jinja2==3.1.2
pydantic==2.5.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "✅ requirements.txt created" -ForegroundColor Green

# Create .gitignore
@"
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Build
/dist/
/build/
*.log

# Environment
.env
.env.local

# Output
/output/
/samples/*.dxf
/samples/*.pdf
/data/temp/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

Write-Host "✅ .gitignore created" -ForegroundColor Green

# Create backend main.py
@"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LispCanvas API",
    description="Civil Engineering Design System",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "LispCanvas API - Civil Engineering Design System",
        "version": "0.1.0",
        "modules": [
            "bridge", "rectangle_column", "road_lsection", "road_plan",
            "road_cross_section", "pmgsy_road", "lintel", "sunshed",
            "tbeam_lbeam", "staircase"
        ]
    }

# Import module routers
# from app.modules.bridge.routes import router as bridge_router
# app.include_router(bridge_router)
"@ | Out-File -FilePath "backend\app\main.py" -Encoding UTF8

Write-Host "✅ Backend main.py created" -ForegroundColor Green

# Create backend __init__.py files
"" | Out-File -FilePath "backend\__init__.py" -Encoding UTF8
"" | Out-File -FilePath "backend\app\__init__.py" -Encoding UTF8

# Create module files
$modules = @(
    "bridge", "rectangle_column", "road_lsection", "road_plan",
    "road_cross_section", "pmgsy_road", "lintel", "sunshed",
    "tbeam_lbeam", "staircase"
)

foreach ($module in $modules) {
    # Backend module __init__.py
    "" | Out-File -FilePath "backend\app\modules\$module\__init__.py" -Encoding UTF8
    
    # Backend module routes.py
    @"
from fastapi import APIRouter

router = APIRouter(prefix="/$module", tags=["$module"])

@router.get("/")
def get_${module}():
    return {"module": "$module", "status": "ready"}

@router.post("/calculate")
def calculate_${module}(params: dict):
    # TODO: Implement calculation logic
    return {"result": "calculation pending"}

@router.post("/generate-dxf")
def generate_dxf_${module}(params: dict):
    # TODO: Implement DXF generation
    return {"dxf": "generation pending"}
"@ | Out-File -FilePath "backend\app\modules\$module\routes.py" -Encoding UTF8

    # Frontend module component
    $moduleName = (Get-Culture).TextInfo.ToTitleCase($module.Replace("_", " ")).Replace(" ", "")
    @"
import React, { useState } from 'react';

const ${moduleName}Module = () => {
  const [params, setParams] = useState({});

  return (
    <div style={{ padding: '20px' }}>
      <h2>${moduleName} Design Module</h2>
      <p>Interactive canvas-based design tool for ${module.Replace("_", " ")}.</p>
      
      <div style={{ marginTop: '20px', display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h3>Parameters</h3>
          <div style={{ background: '#f5f5f5', padding: '15px', borderRadius: '4px' }}>
            <p>Parameter inputs will go here</p>
          </div>
        </div>
        
        <div style={{ flex: 2 }}>
          <h3>Drawing Canvas</h3>
          <canvas 
            width="800" 
            height="600" 
            style={{ 
              border: '2px solid #ddd', 
              borderRadius: '4px',
              background: 'white'
            }}
          />
          <div style={{ marginTop: '10px' }}>
            <button style={{ marginRight: '10px', padding: '8px 16px' }}>Generate DXF</button>
            <button style={{ marginRight: '10px', padding: '8px 16px' }}>Export PDF</button>
            <button style={{ padding: '8px 16px' }}>Clear</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ${moduleName}Module;
"@ | Out-File -FilePath "frontend\src\modules\$module\$module.jsx" -Encoding UTF8
}

Write-Host "✅ Module files created for all 10 modules" -ForegroundColor Green

# Create frontend package.json
@"
{
  "name": "lispcanvas-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": ["react-app"]
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
"@ | Out-File -FilePath "frontend\package.json" -Encoding UTF8

Write-Host "✅ Frontend package.json created" -ForegroundColor Green

# Create frontend App.jsx
@"
import React, { useState } from 'react';
import BridgeModule from './modules/bridge/bridge';
import RectangleColumnModule from './modules/rectangle_column/rectangle_column';
import RoadLsectionModule from './modules/road_lsection/road_lsection';
import RoadPlanModule from './modules/road_plan/road_plan';
import RoadCrossSectionModule from './modules/road_cross_section/road_cross_section';
import PmgsyRoadModule from './modules/pmgsy_road/pmgsy_road';
import LintelModule from './modules/lintel/lintel';
import SunshedModule from './modules/sunshed/sunshed';
import TbeamLbeamModule from './modules/tbeam_lbeam/tbeam_lbeam';
import StaircaseModule from './modules/staircase/staircase';

const modules = [
  { id: 'bridge', name: 'Bridge Design', component: BridgeModule },
  { id: 'rectangle_column', name: 'Rectangle Column', component: RectangleColumnModule },
  { id: 'road_lsection', name: 'Road L-Section', component: RoadLsectionModule },
  { id: 'road_plan', name: 'Road Plan', component: RoadPlanModule },
  { id: 'road_cross_section', name: 'Road Cross Section', component: RoadCrossSectionModule },
  { id: 'pmgsy_road', name: 'PMGSY Road', component: PmgsyRoadModule },
  { id: 'lintel', name: 'Lintel', component: LintelModule },
  { id: 'sunshed', name: 'Sunshed', component: SunshedModule },
  { id: 'tbeam_lbeam', name: 'T-Beam/L-Beam', component: TbeamLbeamModule },
  { id: 'staircase', name: 'Staircase', component: StaircaseModule }
];

function App() {
  const [activeModule, setActiveModule] = useState('bridge');
  
  const ActiveComponent = modules.find(m => m.id === activeModule)?.component;

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      <nav style={{ width: '250px', borderRight: '1px solid #ccc', padding: '20px', background: '#f8f9fa' }}>
        <h1 style={{ fontSize: '24px', marginBottom: '20px', color: '#333' }}>LispCanvas</h1>
        <p style={{ fontSize: '12px', color: '#666', marginBottom: '20px' }}>Civil Engineering Design</p>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {modules.map(module => (
            <li key={module.id} style={{ marginBottom: '8px' }}>
              <button
                onClick={() => setActiveModule(module.id)}
                style={{
                  width: '100%',
                  padding: '12px',
                  textAlign: 'left',
                  background: activeModule === module.id ? '#007bff' : 'white',
                  color: activeModule === module.id ? 'white' : '#333',
                  border: '1px solid #ddd',
                  cursor: 'pointer',
                  borderRadius: '4px',
                  fontSize: '14px',
                  transition: 'all 0.2s'
                }}
              >
                {module.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <main style={{ flex: 1, padding: '20px', overflow: 'auto', background: 'white' }}>
        {ActiveComponent && <ActiveComponent />}
      </main>
    </div>
  );
}

export default App;
"@ | Out-File -FilePath "frontend\src\App.jsx" -Encoding UTF8

Write-Host "✅ Frontend App.jsx created" -ForegroundColor Green

# Create frontend index.js
@"
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"@ | Out-File -FilePath "frontend\src\index.js" -Encoding UTF8

# Create frontend public/index.html
@"
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="LispCanvas - Civil Engineering Design System" />
    <title>LispCanvas</title>
  </head>
  <body style="margin: 0; padding: 0;">
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"@ | Out-File -FilePath "frontend\public\index.html" -Encoding UTF8

Write-Host "✅ Frontend entry files created" -ForegroundColor Green

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 LispCanvas project setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Install backend dependencies: cd backend && pip install -r ../requirements.txt" -ForegroundColor White
Write-Host "2. Install frontend dependencies: cd frontend && npm install" -ForegroundColor White
Write-Host "3. Start backend: cd backend && uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "4. Start frontend: cd frontend && npm start" -ForegroundColor White
Write-Host ""
Write-Host "To commit: git add . && git commit -m 'feat: initialize LispCanvas structure'" -ForegroundColor Cyan
