import json

from pathlib import Path
from config import DATA_FILE

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / DATA_FILE

class Database:
    @staticmethod
    def read():
        if not DATA_PATH.exists():
            return []
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write(data):
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DATA_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
