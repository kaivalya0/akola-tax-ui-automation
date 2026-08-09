import json
from pathlib import Path


class DataLoader:
    @staticmethod
    def load_json(file_name: str) -> dict:
        base_path = Path(__file__).parent.parent
        with open(base_path / "data" / file_name, "r", encoding="utf-8") as f:
            return json.load(f)