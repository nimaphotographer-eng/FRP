
import json
from pathlib import Path
from datetime import datetime

class ReportManager:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def export_txt(self, record):
        name = datetime.now().strftime("diagnostic_%Y%m%d_%H%M%S.txt")
        path = self.root / name
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        return path
