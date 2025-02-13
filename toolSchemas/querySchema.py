from pydantic import BaseModel, Field

class ExpenseQuery(BaseModel):
    phone_number: str = Field(..., description="User's phone number to fetch expenses.")