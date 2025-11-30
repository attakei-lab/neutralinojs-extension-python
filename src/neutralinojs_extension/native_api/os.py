"""Data types of Neutralino.os API.

:ref: https://neutralino.js.org/docs/api/os
"""

from __future__ import annotations

from typing import Literal

from ._base import APISchema


class ShowMessageBox(APISchema):
    """Displays a message box.

    :ref: https://neutralino.js.org/docs/api/os#osshowmessageboxtitle-content-choice-icon
    """

    ID = "os.showMessageBox"

    title: str
    content: str
    choice: Literal[
        "OK",
        "OK_CANCEL",
        "YES_NO",
        "YES_NO_CANCEL",
        "RETRY_CANCEL",
        "ABORT_RETRY_IGNORE",
    ] = "OK"
    icon: Literal["INFO", "WARNING", "ERROR", "QUESTION"] = "INFO"


class ShowNotification(APISchema):
    """Displays a notification message.

    :ref: https://neutralino.js.org/docs/api/os#osshownotificationtitle-content-icon
    """

    ID = "os.showNotification"

    title: str
    content: str
    icon: Literal["INFO", "WARNING", "ERROR", "QUESTION"] = "INFO"


class ShowOpenDialog(APISchema):
    """Shows the file open dialog. You can use this function to obtain paths of existing files.

    :ref: https://neutralino.js.org/docs/api/os#osshowopendialogtitle-options
    """

    ID = "os.showOpenDialog"

    title: str
    # TODO: Define details after.
    options: dict
