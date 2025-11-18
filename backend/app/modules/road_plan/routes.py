from fastapi import APIRouter

router = APIRouter(prefix="/road_plan", tags=["road_plan"])

@router.get("/")
def get_road_plan():
    return {"module": "road_plan", "status": "ready"}

@router.post("/calculate")
def calculate_road_plan(params: dict):
    # TODO: Implement calculation logic
    return {"result": "calculation pending"}

@router.post("/generate-dxf")
def generate_dxf_road_plan(params: dict):
    # TODO: Implement DXF generation
    return {"dxf": "generation pending"}
