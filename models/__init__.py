from abc import ABC, abstractmethod
from datetime import datetime
import json
import os

class BaseModel(ABC):
    def __init__(self):
        self.id = None
        self.type = self.__class__.__name__.lower()
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass
    
    @staticmethod
    def save_records(records, filename):
        # Ensure all IDs are integers before saving
        for record in records:
            if 'id' in record:
                record['id'] = int(record['id'])
            if 'client_id' in record:
                record['client_id'] = int(record['client_id'])
            if 'airline_id' in record:
                record['airline_id'] = int(record['airline_id'])
        with open(filename, 'r+') as f:
            try:
                append_record = json.load(f)
                append_record.update(records)
                f.seek(0)
                json.dump(append_record, f, default=str, indent=4)
            except:
                append_record = {}
                json.dump(records, f, default=str, indent=4)
    
    @staticmethod
    def load_records(filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                if not content:  # File is empty
                    return []
                records = json.load(f)
                # Convert any string IDs back to integers
                for record in records:
                    if 'id' in record:
                        record['id'] = int(record['id'])
                    if 'client_id' in record:
                        record['client_id'] = int(record['client_id'])
                    if 'airline_id' in record:
                        record['airline_id'] = int(record['airline_id'])
                return records
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is invalid 