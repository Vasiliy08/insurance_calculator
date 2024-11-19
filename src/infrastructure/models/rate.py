from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Rate(Base):
    __tablename__ = "rates"

    oid: Mapped[int] = mapped_column(primary_key=True)
    cargo_type: Mapped[str]
    rate: Mapped[float]
    effective_date: Mapped[datetime]
