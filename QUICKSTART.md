# LispCanvas Quick Start Guide

## 🎯 Project Overview

LispCanvas is a **canvas-based civil engineering design system** that generates professional drawings with DXF export capabilities. The project includes 10 specialized modules for various civil engineering design tasks.

## 📁 Project Structure

```
LispCanvas/
├── frontend/              # React-based UI
│   ├── src/
│   │   ├── modules/      # 10 design modules
│   │   ├── components/   # Shared components
│   │   └── App.jsx       # Main application
│   └── package.json
├── backend/              # FastAPI backend
│   └── app/
│       ├── modules/      # API endpoints for each module
│       └── main.py       # FastAPI application
├── modules/              # Existing Python modules (legacy)
├── shared/               # Shared configurations
├── templates/            # DXF templates
└── requirements.txt      # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Step 1: Install Backend Dependencies

```cmd
cd backend
pip install -r ..\requirements.txt
```

### Step 2: Install Frontend Dependencies

```cmd
cd frontend
npm install
```

## ▶️ Running the Application

### Start Backend Server

```cmd
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Start Frontend Development Server

```cmd
cd frontend
npm start
```

Frontend will be available at: `http://localhost:3000`

## 📐 Available Modules

| Module | Description | Status |
|--------|-------------|--------|
| **Bridge Design** | GAD drawings from parameters | ✅ Ready |
| **Rectangle Column** | Structural column with footing | ✅ Ready |
| **Road L-Section** | Longitudinal road profiles | ✅ Ready |
| **Road Plan** | Plan view road alignments | ✅ Ready |
| **Road Cross Section** | Transverse road profiles | ✅ Ready |
| **PMGSY Road** | Rural road specifications | ✅ Ready |
| **Lintel** | Structural beam design | ✅ Ready |
| **Sunshed** | Architectural element design | ✅ Ready |
| **T-Beam/L-Beam** | Structural beam design | ✅ Ready |
| **Staircase** | Structural stair design | ✅ Ready |

## 🔧 Development Workflow

### Adding a New Feature to a Module

1. **Frontend**: Edit `frontend/src/modules/{module_name}/{module_name}.jsx`
2. **Backend**: Edit `backend/app/modules/{module_name}/routes.py`
3. **Test**: Run both servers and test in browser

### Creating DXF Output

Each module's backend route includes a `/generate-dxf` endpoint:

```python
@router.post("/generate-dxf")
def generate_dxf_bridge(params: dict):
    # Use ezdxf library to create DXF
    import ezdxf
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # Add drawing entities
    doc.saveas('output.dxf')
    return {"dxf": "output.dxf"}
```

## 🧪 Testing

### Test Backend API

```cmd
cd backend
python -m pytest
```

### Test Frontend

```cmd
cd frontend
npm test
```

### Manual API Testing

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 📦 Building for Production

### Build Frontend

```cmd
cd frontend
npm run build
```

Output will be in `frontend/build/`

### Deploy Backend

```cmd
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔄 Maintenance Script

Use the automated maintenance script:

```cmd
maintain-lispcanvas.bat
```

This script will:
1. Pull latest changes
2. Install dependencies
3. Run tests
4. Clean cache
5. Commit and push changes

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8000 is available

### Frontend won't start
- Clear node_modules: `rmdir /s /q node_modules && npm install`
- Check port 3000 is available
- Clear npm cache: `npm cache clean --force`

### CORS errors
- Ensure backend CORS middleware is configured
- Check backend is running on port 8000

## 📚 API Endpoints

### Root
- `GET /` - API status and available modules

### Module Endpoints (for each module)
- `GET /{module}` - Get module status
- `POST /{module}/calculate` - Perform calculations
- `POST /{module}/generate-dxf` - Generate DXF output

Example:
```bash
curl http://localhost:8000/bridge
curl -X POST http://localhost:8000/bridge/calculate -H "Content-Type: application/json" -d '{"span": 10, "width": 5}'
```

## 🎨 Customization

### Styling
- Edit `frontend/src/App.jsx` for global styles
- Each module has inline styles that can be customized

### Adding New Modules
1. Create frontend component: `frontend/src/modules/new_module/new_module.jsx`
2. Create backend routes: `backend/app/modules/new_module/routes.py`
3. Register in `frontend/src/App.jsx`
4. Register in `backend/app/main.py`

## 📝 Git Workflow

```cmd
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add bridge calculation logic"

# Push to GitHub
git push origin main
```

## 🔗 Integration with Existing Modules

The project already has Python modules in the `modules/` directory. To integrate:

1. Import existing module in backend route
2. Call functions from existing modules
3. Return results to frontend

Example:
```python
from modules.bridge import generate_bridge_drawing

@router.post("/generate-dxf")
def generate_dxf_bridge(params: dict):
    result = generate_bridge_drawing(params)
    return {"dxf": result}
```

## 🎯 Next Steps

1. ✅ Project structure created
2. ⏳ Implement calculation logic for each module
3. ⏳ Add canvas drawing functionality
4. ⏳ Integrate DXF generation
5. ⏳ Add PDF export
6. ⏳ Deploy to production

## 📞 Support

For issues or questions, check:
- Backend logs: Terminal running uvicorn
- Frontend logs: Browser console (F12)
- API docs: http://localhost:8000/docs

---

**Happy Building! 🏗️**
