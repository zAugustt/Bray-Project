"""
Models Module

This module provides a representations of the entities in the database.

Authors:
   Josh Werner (joshdwerner2@tamu.edu), Texas A&M University
   Abdiel Rivera (arivera15@tamu.edu), Texas A&M University

Date:
    March 2025
"""

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

class Base(DeclarativeBase):
    pass

class Event(Base):
    """
    Sensor Events
    """

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)

    deviceInfoID: Mapped[int] = mapped_column(ForeignKey("device_info.id"), unique=True, nullable=False)
    deviceDataID: Mapped[int] = mapped_column(ForeignKey("device_data.id"), unique=True, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

class DeviceInfo(Base):
    """
    Information on the individual sensor
    """

    __tablename__ = "device_info"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensorName: Mapped[str] = mapped_column(String, nullable=False)
    serialNumber: Mapped[str] = mapped_column(String, nullable=False)
    deviceType: Mapped[str] = mapped_column(String, nullable=False)
    deviceLocation: Mapped[str] = mapped_column(String, nullable=False)

    event: Mapped["Event"] = relationship(back_populates="deviceInfo")

class DeviceData(Base):
    """
    Data collected by sensor. Can be expanded to fit specific devices
    """

    __tablename__ = "device_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    measurementData: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)

    event: Mapped["Event"] = relationship(back_populates="deviceData")