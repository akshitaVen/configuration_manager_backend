from fastapi import APIRouter, HTTPException
from app.models.schemas import CreateConfigRequest
from app.services.create_configuration_service import create_new_configuration

router = APIRouter()

@router.post("/configurations")
def create_configuration(req: CreateConfigRequest):
    try:
        create_new_configuration(req.config_name)
        return {"message": f"Configuration '{req.config_name}' created successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))