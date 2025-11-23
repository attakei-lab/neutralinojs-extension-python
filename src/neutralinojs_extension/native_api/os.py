"""Data types of Neutralino.os API.

:ref: https://neutralino.js.org/docs/api/os
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._base import APISchema

if TYPE_CHECKING:
    from typing import Literal


@dataclass
class Os_ShowNotification(APISchema):
    """Displays a notification message.

    :ref: https://neutralino.js.org/docs/api/os#osshownotificationtitle-content-icon
    """

    ID = "os.showNotification"

    title: str
    content: str
    icon: Literal["INFO", "WARNING", "ERROR", "QUESTION"] = "INFO"
