"""Data types of Neutralino.app API.

:ref: https://neutralino.js.org/docs/api/app
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._base import APISchema

if TYPE_CHECKING:
    from ._base import CustomEventData


@dataclass
class App_Broadcast(APISchema):
    """Dispatches an event to all app instances.

    :ref: https://neutralino.js.org/docs/api/app#appbroadcastevent-data
    """

    ID = "app.broadcast"

    event: str
    data: CustomEventData | dict | str | None
