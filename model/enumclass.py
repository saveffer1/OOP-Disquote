from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class UserStatus(Enum):
    online = 1
    idle = 2
    invisible = 3
