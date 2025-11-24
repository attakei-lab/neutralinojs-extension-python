"""Definition of data types for calling native APIs.

.. note::

    This package does not have all definitions because they are used only type hints.
    I will add them when I want to add, but I accept PR for them if you want.

:ref: https://neutralino.js.org/docs/api/overview
"""

from __future__ import annotations

from .app import Broadcast as App_Broadcast
from .debug import Log as Debug_Log
from .os import ShowMessageBox as Os_ShowMessageBox
from .os import ShowNotification as Os_ShowNotification
from .window import SetTitle as Window_SetTitle

__all__ = [
    "App_Broadcast",
    "Debug_Log",
    "Os_ShowMessageBox",
    "Os_ShowNotification",
    "Window_SetTitle",
]
