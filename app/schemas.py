from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

class IdentityOut(BaseModel):
    id: int
    license_number: str
    full_name: str
    address: Optional[str] = None
    expires_at: Optional[date] = None

    class Config:
        orm_mode = True


class ScanOut(BaseModel):
    id: int
    identity_id: int
    created_at: datetime
    verdict_value: str

    class Config:
        orm_mode = True