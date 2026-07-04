from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class SchemaBase(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserSchema(SchemaBase):
    email: str

class BusinessCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    profile_summary: Optional[str] = None

class BusinessSchema(SchemaBase, BusinessCreate):
    user_id: UUID4
