#!/usr/bin/env python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models  # Import models module, not storage directly


class BaseModel:
    """Represents the BaseModel class for the AirBnB clone project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)  # Use models.storage instead of direct import

    def save(self):
        """Update `updated_at` and save to storage."""
        self.updated_at = datetime.now()
        models.storage.save()  # Use models.storage here

    def to_dict(self):
        """Return a dictionary representation of the BaseModel."""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
