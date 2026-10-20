import json
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_FILE = Path(__file__).parent / "inventory.json"

@dataclass
class InventoryItem:
    name: str
    quantity: int
    price: float