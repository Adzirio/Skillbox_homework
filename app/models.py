from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .db import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    credit_card = Column(String(50), nullable=True)
    car_number = Column(String(50), nullable=True)

    client_parkings = relationship(
        "ClientParking", back_populates="client", cascade="all, delete-orphan"
    )


class Parking(Base):
    __tablename__ = "parking"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    opened = Column(Boolean, nullable=True)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)

    client_parkings = relationship(
        "ClientParking", back_populates="parking", cascade="all, delete-orphan"
    )


class ClientParking(Base):
    __tablename__ = "client_parking"
    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    parking_id = Column(Integer, ForeignKey("parking.id"), nullable=False)
    time_in = Column(DateTime, nullable=True)
    time_out = Column(DateTime, nullable=True)

    client = relationship("Client", back_populates="client_parkings")
    parking = relationship("Parking", back_populates="client_parkings")
