"""
Models Module

This module provides a representations of the entities in the database.

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Josh Werner (joshdwerner2@tamu.edu), Texas A&M University

Date:
    November 2024
    March 2025
"""

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, Double
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    """
    Base used for declarative classes. Subclassing allows the creation of the schema with a single command.
    """
    pass


class Sensor(Base):
    """
    Sensor entity.
    """
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)

    devEUI: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="sensor")

class AuxSensor(Base):
    """
    Auxiliary sensor entity containing sensors
    """
    __tablename__ = "aux_sensors"

    id: Mapped[int] = mapped_column(primary_key=True)

    sensor_data: Mapped[list["AuxSensorData"]] = relationship(back_populates="sensor")


class AuxSensorData(Base):
    """
    Auxiliary sensor data entity containing individual data points.
    """
    __tablename__ = "aux_sensor_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    aux_sensor_id: Mapped[int] = mapped_column(ForeignKey("aux_sensors.id"), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    value: Mapped[float] = mapped_column(Double, nullable=False)

    sensor: Mapped["AuxSensor"] = relationship(back_populates="sensor_data")
        

class Event(Base):
    """
    Sensor event entity.
    """
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    isStreaming: Mapped[bool] = mapped_column(Boolean, nullable=False)
    deviceInfoID: Mapped[int] = mapped_column(ForeignKey("device_infos.id"), unique=True, nullable=False)
    deviceDataID: Mapped[int] = mapped_column(ForeignKey("device_datas.id"), unique=True, nullable=False)
    deviceTrendInfoID: Mapped[int] = mapped_column(ForeignKey("device_trend_infos.id"), unique=True, nullable=False)
    sensorID: Mapped[int] = mapped_column(ForeignKey("sensors.id"), nullable=False)

    deviceInfo: Mapped["DeviceInfo"] = relationship(back_populates="event")
    deviceData: Mapped["DeviceData"] = relationship(back_populates="event")
    deviceTrendInfo: Mapped["DeviceTrendInfo"] = relationship(back_populates="event")
    sensor: Mapped["Sensor"] = relationship(back_populates="events")


class DeviceInfo(Base):
    """
    Sensor event information entity containing general information.
    """
    __tablename__ = "device_infos"

    id: Mapped[int] = mapped_column(primary_key=True)

    firmwareVersion: Mapped[str] = mapped_column(String, nullable=False)
    pwaRevision: Mapped[str] = mapped_column(String, nullable=False)
    serialNumber: Mapped[str] = mapped_column(String, nullable=False)
    deviceType: Mapped[str] = mapped_column(String, nullable=False)
    deviceLocation: Mapped[str] = mapped_column(String, nullable=False)
    diagnostic: Mapped[int] = mapped_column(Integer, nullable=False)
    openValveCount: Mapped[int] = mapped_column(Integer, nullable=False)
    closeValveCount: Mapped[int] = mapped_column(Integer, nullable=False)

    event: Mapped["Event"] = relationship(back_populates="deviceInfo")


class DeviceTrendInfo(Base):
    """
    Sensor trend information entity.
    """
    __tablename__ = "device_trend_infos"

    id: Mapped[int] = mapped_column(primary_key=True)

    strokeTime: Mapped[int] = mapped_column(Integer, nullable=False)
    maxTorque: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    batteryVoltage: Mapped[int] = mapped_column(Integer, nullable=False)

    event: Mapped["Event"] = relationship(back_populates="deviceTrendInfo")


class DeviceData(Base):
    """
    Sensor event information entity containing more detailed information.
    """
    __tablename__ = "device_datas"

    id: Mapped[int] = mapped_column(primary_key=True)

    lastTorqueBeforeSleep: Mapped[int] = mapped_column(Integer, nullable=False)
    firstTorqueAfterSleep: Mapped[int] = mapped_column(Integer, nullable=False)
    recordNumbers: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    recordLengths: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    torqueData: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    hiddenDataIndices: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    typeOfStroke: Mapped[int] = mapped_column(Integer, nullable=False)
    dataRecordPayloadCRCs: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    calculatedDataRecordPayloadCRCs: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    eventRecordPayloadCRC: Mapped[int] = mapped_column(Integer, nullable=False)
    calculatedEventRecordPayloadCRC: Mapped[int] = mapped_column(Integer, nullable=False)
    heartbeatRecordPayloadCRC: Mapped[int] = mapped_column(Integer, nullable=False)
    calculatedHeartbeatRecordPayloadCRC: Mapped[int] = mapped_column(Integer, nullable=False)

    event: Mapped["Event"] = relationship(back_populates="deviceData")