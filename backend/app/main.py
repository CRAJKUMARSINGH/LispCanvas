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
