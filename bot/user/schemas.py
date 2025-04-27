from pydantic import BaseModel, Field, computed_field
from datetime import date, datetime
from bot.dao.models import CatEnum

class SUser(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None


class STransactions(BaseModel):
    price: int
    cat: CatEnum
    description: str | None = Field(default=None)
    user_id: int

    class Config:
        from_attributes = True


class SExpenses(BaseModel):
    food: int
    entertainment: int
    transport: int
    other: int

    @computed_field
    def total(self) -> int:
        return self.food + self.entertainment + self.transport + self.other