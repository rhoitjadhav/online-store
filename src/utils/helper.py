# Packages
import string
import random
from typing import Optional, Dict, Any, AnyStr
from dataclasses import dataclass, field, asdict


@dataclass
class ReturnValue:
    """ReturnValue class is responsible for holding returned value from operations

    Args:
        success: True if operation is successful otherwise False
        http_code: http status code
        message: message after successful operation
        error: error message after failed operation
        data: resulted data after operation completion
    """
    status: bool = True
    http_code: Optional[int] = -1
    message: str = ""
    error: str = ""
    data: Any = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


class Helper:
    @staticmethod
    def generate_random_text(l: int = 6) -> AnyStr:
        """Generate random alphanumeric string

        Args:
            l: length of string. Defaults to 6.

        Returns:
            random string
        """
        return ''.join(random.choices(string.ascii_letters +
                                      string.digits, k=l))
