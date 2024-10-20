from enums import BaseEnum
from typing import List, Any

class BaseEnum(Enum):
    @classmethod
    def all_value(cls) -> List[Any]:
        return list(map(lambda c: c.value, cls))
