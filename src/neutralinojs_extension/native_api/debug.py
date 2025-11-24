"""Data types of Neutralino.debug API.

:ref: https://neutralino.js.org/docs/api/debug
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._base import APISchema

if TYPE_CHECKING:
    from typing import Literal


@dataclass
class Log(APISchema):
    """Writes messages to neutralinojs.log file or/and standard output streams.

    :ref: https://neutralino.js.org/docs/api/debug/#debuglogmessage-type
    """

    ID = "debug.log"

    message: str
    type: Literal["INFO", "WARNING", "ERROR"] = "INFO"
