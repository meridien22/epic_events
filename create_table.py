from private.parameter import parameter

from decimal import Decimal

from typing import List, Optional

from datetime import date, datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    sessionmaker,
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    Boolean,
    Text,
    ForeignKey,
    CheckConstraint,
    create_engine,
    MetaData,
)

engine = create_engine(
    f'postgresql+psycopg2://epic_user:{parameter["password_db"]}@localhost:5432/epic_events',
    echo=False
)

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    metadata = MetaData(schema="dev")


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50))

    clients: Mapped[List["Client"]] = relationship(back_populates="commercial")

    contracts: Mapped[List["Contract"]] = relationship(back_populates="commercial")

    __table_args__ = (
        CheckConstraint(
            "department IN ('Sales', 'Support', 'Management')",
            name="check_department"
        ),
    )


class Enterprise(Base):
    __tablename__ = 'enterprise'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))

    clients: Mapped[List["Client"]] = relationship(back_populates="enterprise")

    events: Mapped[List["Event"]] = relationship(back_populates="support")


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

    events: Mapped[List["Event"]] = relationship(back_populates="client")

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprise.id"))
    enterprise: Mapped["Enterprise"] = relationship(back_populates="clients")

    commercial_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    commercial: Mapped["User"] = relationship(back_populates="clients")


class Contract(Base):
    __tablename__ = 'contract'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    remaining_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    date_creation: Mapped[date] = mapped_column(Date, default=date.today)
    is_signed: Mapped[bool] = mapped_column(Boolean, default=False)

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped["Client"] = relationship(back_populates="contracts")

    commercial_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    commercial: Mapped["User"] = relationship(back_populates="contracts")

    event: Mapped[Optional["Event"]] = relationship(back_populates="contract")


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_event: Mapped[str] = mapped_column(String(50))
    date_start: Mapped[date] = mapped_column(Date)
    date_end: Mapped[date] = mapped_column(Date)
    expected_audience: Mapped[int] = mapped_column(Integer)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id"), unique=True)
    contract: Mapped["Contract"] = relationship(back_populates="event")

    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped["Client"] = relationship(back_populates="events")

    support_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    support: Mapped["User"] = relationship(back_populates="events")

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


Base.metadata.create_all(engine)