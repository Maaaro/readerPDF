from dataclasses import dataclass
from enum import Enum

class LimitedSearch(Enum):
    LIMITED = 1
    FULL = 2

@dataclass
class SearchRequest:
    limited_search: LimitedSearch
    invoice_folder: str
    target_folder: str
    excel_path: str
