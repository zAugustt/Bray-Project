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

    deviceinfoid: Mapped[int] = mapped_column(ForeignKey("device_info.id"), unique=True, nullable=False)
    devicedataid: Mapped[int] = mapped_column(ForeignKey("device_data.id"), unique=True, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    deviceInfo: Mapped["DeviceInfo"] = relationship("DeviceInfo", back_populates="events")
    deviceData: Mapped["DeviceData"] = relationship("DeviceData", back_populates="events")

class DeviceInfo(Base):
    """
    Information on the individual sensor
    """

    __tablename__ = "device_info"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensorname: Mapped[str] = mapped_column("sensorname", String, nullable=False)
    serialnumber: Mapped[str] = mapped_column("serialnumber", String, nullable=False)
    devicetype: Mapped[str] = mapped_column("devicetype", String, nullable=False)
    devicelocation: Mapped[str] = mapped_column("devicelocation", String, nullable=False)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="deviceInfo")

class DeviceData(Base):
    """
    Data collected by sensor. Can be expanded to fit specific devices
    """

    __tablename__ = "device_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    measurementdata: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="deviceData")