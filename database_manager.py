
import json
from pathlib import Path

class DeviceDatabase:
    def __init__(self, path):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}

    def lookup(self, model):
        return self.data.get(model, {})
