from sources.dao.base_dao import Base

from decimal import Decimal

from typing import List, Optional

from datetime import date, datetime

from passlib.hash import argon2

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from sqlalchemy import (

    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    Boolean,
    Text,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Column,
    Table,
)

departement_permissions = Table(
    "departement_permission",
    Base.metadata,
    Column("department_id", ForeignKey("department.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)

class Permission(Base):
    __tablename__ = 'permission'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    departments: Mapped[list["Department"]] = relationship(
        secondary=departement_permissions, back_populates="permissions"
    )


class Department(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[List["User"]] = relationship(back_populates="department")

    permissions: Mapped[list["Permission"]] = relationship(
        secondary=departement_permissions, back_populates="departments"
    )

    __table_args__ = (
        UniqueConstraint("name", name="unique_department_name"),
        CheckConstraint(
            "name IN ('Sales', 'Support', 'Management', 'Admin')",
            name="check_name"
        ),
    )

    def __str__(self):
         return f"{self.name} ({self.id})"


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String(50), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="session")


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))

    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"))
    department: Mapped["Department"] = relationship(back_populates="users")

    clients: Mapped[List["Client"]] = relationship(back_populates="commercial")

    events: Mapped[List["Event"]] = relationship(back_populates="support")

    session: Mapped[List["Session"]] = relationship(back_populates="user")

    __table_args__ = (
        UniqueConstraint("email", name="unique_email_user_name"),
    )

    def set_password(self, password):
            self.password = argon2.hash(password)

    def check_password(self, password):
            try:
                return argon2.verify(password, self.password)
            except Exception:
                return False
            
    def __str__(self):
         return f"{self.first_name} {self.last_name} ({self.id})"


class Enterprise(Base):
    __tablename__ = 'enterprise'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    clients: Mapped[List["Client"]] = relationship(back_populates="enterprise")

    __table_args__ = (
        UniqueConstraint("name", name="unique_enterprise_name"),
    )

    def __str__(self):
         return f"{self.name} ({self.id})"


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_creation: Mapped[date] = mapped_column(Date, default=date.today)
    date_update: Mapped[datetime] = mapped_column(DateTime,
                                                  default=datetime.now,
                                                  onupdate=datetime.now
    )

    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprise.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="clients")

    commercial_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    commercial: Mapped["User"] = relationship(back_populates="clients")

    __table_args__ = (
        UniqueConstraint("email", name="unique_email_client_name"),
    )

    def __str__(self):
         return f"{self.first_name} {self.last_name} ({self.id})"



class Contract(Base):
    __tablename__ = 'contract'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    remaining_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    date_creation: Mapped[date] = mapped_column(Date, default=date.today)
    is_signed: Mapped[bool] = mapped_column(Boolean, default=False)

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped["Client"] = relationship(back_populates="contracts")

    event: Mapped[Optional["Event"]] = relationship(back_populates="contract")

    def __str__(self):
         return f"{self.total_amount} {self.date_creation} ({self.id})"


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    type_event: Mapped[str] = mapped_column(String(50))
    date_start: Mapped[date] = mapped_column(Date)
    date_end: Mapped[date] = mapped_column(Date)
    expected_audience: Mapped[int] = mapped_column(Integer)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id"), unique=True)
    contract: Mapped["Contract"] = relationship(back_populates="event")

    support_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    support: Mapped[Optional["User"]] = relationship(back_populates="events")

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    location: Mapped["Location"] = relationship(back_populates="events")


    __table_args__ = (
        CheckConstraint(
            "type_event IN ('Partie', 'Business meeting', 'Off-site event')",
            name="check_event_type"
        ),
    )


class Location(Base):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String(150))
    postal_code: Mapped[str] = mapped_column(String(10))
    city: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(50))

    events: Mapped[List["Event"]] = relationship(back_populates="location")

    def __str__(self):
         return f"{self.street} {self.postal_code} {self.city} {self.country} ({self.id}) "
