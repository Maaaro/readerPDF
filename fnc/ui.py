from dataclasses import dataclass
from enum import Enum

class SearchMode(Enum):
    LIMITED = 1
    FULL = 2

@dataclass
class SearchRequest:
    search_mode: SearchMode
    invoice_folder: str
    target_folder: str
    excel_path: str
