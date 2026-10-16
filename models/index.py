from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreate(BaseModel):
    name: str = Field(..., description="The name of the project")
    description: Optional[str] = Field(None, description="Project description")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The new name of the project")
    description: Optional[str] = Field(None, description="The new project description")