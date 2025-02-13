from pydantic import BaseModel, Field
from typing import Optional

class Expense(BaseModel):
    amount: float = Field(..., description="The amount spent.")
    currency: Optional[str] = Field(default="INR", description="Currency (default is INR).")
    category: str = Field(..., description="Category of expense.")
    note: str = Field(..., description="Short description of the expense.")
    phone_number: str = Field(..., description="User's phone number.")