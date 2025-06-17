from pydantic import BaseModel

class CreateConfigRequest(BaseModel):
    config_name: str
