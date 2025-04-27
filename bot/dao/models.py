import enum
from datetime import datetime
from sqlalchemy import BigInteger, String
from bot.dao.database import Base
from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum


class CatEnum(enum.Enum):
    FOOD = "food"
    ENTERTAINMENT = "entertainment"
    TRANSPORT = "transport"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    
    transactions: Mapped[list["Transactions"]] = relationship(back_populates="user")


class Transactions(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[int]
    description: Mapped[str | None]

    cat = mapped_column(Enum(CatEnum), nullable=False)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="transactions")