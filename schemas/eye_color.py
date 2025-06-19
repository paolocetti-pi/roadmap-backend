from pydantic import BaseModel


class EyeColorResponse(BaseModel):
    id: int
    color: str

    class Config:
        from_attributes = True 