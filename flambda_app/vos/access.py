import uuid
from datetime import datetime


class AccessV0:
    """
    Value Object for Access
    """

    def __init__(self, data: dict = None, default_values=True):
        """
        Initialize the AccessV0 object with the given data or set default values.
        """
        self.id = data.get('id') if data and "id" in data else None
        self.type = data.get('type') if data and "type" in data else None
        self.timestamp = data.get('timestamp') if data and "timestamp" in data \
            else datetime.now().isoformat() if default_values else None
        self.created_at = data.get('created_at') if data and 'created_at' in data \
            else datetime.now().isoformat() if default_values else None
        self.updated_at = data.get('updated_at') if data and 'updated_at' in data else None
        self.deleted_at = data.get('deleted_at') if data and 'deleted_at' in data else None
        self.turnstile_uuid = data.get(
            'turnstile_uuid') if data and 'turnstile_uuid' in data else None

    def __str__(self):
        """
        String representation of the AccessV0 instance.
        """
        return f"AccessV0(id={self.id}, type={self.type}, timestamp={self.timestamp}, " \
               f"created_at={self.created_at}, updated_at={self.updated_at}, " \
               f"deleted_at={self.deleted_at}, turnstile_uuid={self.turnstile_uuid})"

    def to_dict(self):
        """
        Converts the AccessV0 to a dictionary.
        """
        return {
            'id': self.id,
            'type': self.type,
            'timestamp': self.timestamp,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
            'turnstile_uuid': self.turnstile_uuid
        }

    def to_api_response(self):
        """
        Prepare the data for API response in the requested order.
        """
        return {
            "turnstile_uuid": self.turnstile_uuid,
            "type": self.type,
            "timestamp": self.timestamp,
            "created_at": self.created_at
        }
