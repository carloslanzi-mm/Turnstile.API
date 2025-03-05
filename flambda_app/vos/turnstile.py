import uuid
from datetime import datetime


class TurnstileVO:
    """
    Value Object for Turnstile
    """

    def __init__(self, data: dict = None, default_values=True):
        """
        Initialize the TurnstileVO object with the given data or set default values.
        """
        self.id = data.get('id') if data and "id" in data else None
        self.uuid = data.get('uuid') if data and "uuid" in data \
            else str(uuid.uuid4()) if default_values else None
        self.name = data.get('name') if data and "name" in data else None
        self.is_active = data.get('is_active') if data and "is_active" in data else True
        self.created_at = data.get('created_at') if data and 'created_at' in data \
            else datetime.now().isoformat() if default_values else None
        self.updated_at = data.get('updated_at') if data and 'updated_at' in data else None
        self.deleted_at = data.get('deleted_at') if data and 'deleted_at' in data else None

    def __str__(self):
        """
        String representation of the TurnstileVO instance.
        """
        return f"TurnstileVO(id={self.id}, uuid={self.uuid}, name={self.name}, " \
               f"is_active={self.is_active}, created_at={self.created_at}, " \
               f"updated_at={self.updated_at}), deleted_at={self.deleted_at}"

    def to_dict(self):
        """
        Converts the TurnstileVO to a dictionary.
        """
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }

    def update(self, data: dict):
        """
        Update the TurnstileVO instance with the provided data.
        """
        if 'name' in data:
            self.name = data['name']
        if 'is_active' in data:
            self.is_active = data['is_active']
        if 'created_at' in data:
            self.created_at = data['created_at']
        if 'updated_at' in data:
            self.updated_at = data['updated_at']
        if 'deleted_at' in data:
            self.updated_at = data['deleted_at']

    def to_api_response(self):
        """
        Prepare the data for API response.
        """
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }
