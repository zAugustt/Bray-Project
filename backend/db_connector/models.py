"""
Models Module

This module provides a representations of the entities in the database.

Authors:
   Josh Werner (joshdwerner2@tamu.edu), Texas A&M University

Date:
    March 2025
"""

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
