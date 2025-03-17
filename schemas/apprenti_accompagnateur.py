from pydantic import BaseModel

class ApprentiAccompagnateurCreate(BaseModel):
    apprenti_id: int
    accompagnateur_id: int
    lien: str

class ApprentiAccompagnateurResponse(ApprentiAccompagnateurCreate):
    id: int

    class Config:
        orm_mode = True