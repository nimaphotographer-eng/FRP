
import json
from pathlib import Path
from datetime import datetime

class HistoryManager:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, record):
        data = []
        if self.path.exists():
            try: data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception: data = []
        data.append({"time": datetime.now().isoformat(timespec="seconds"), "record": record})
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
