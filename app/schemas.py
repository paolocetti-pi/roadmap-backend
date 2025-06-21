from pydantic import BaseModel

class TaskControl(BaseModel):
    enabled: bool 