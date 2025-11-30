"""Data types of Neutralino.window API.

:ref: https://neutralino.js.org/docs/api/window
"""

from __future__ import annotations

from ._base import APISchema


class SetTitle(APISchema):
    """Sets the title of the native window.

    :ref: https://neutralino.js.org/docs/api/window#windowsettitletitle
    """

    ID = "window.setTitle"

    title: str | None = None
