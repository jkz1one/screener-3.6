from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.screenbuilder import build_screening_output

router = APIRouter()

@router.get("/")
def get_autowatchlist():
    try:
        data = build_screening_output()
        return JSONResponse(content=data.to_dict("records"))
    except Exception as e:
        print(f"❌ Error generating autowatchlist: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate autowatchlist."})
