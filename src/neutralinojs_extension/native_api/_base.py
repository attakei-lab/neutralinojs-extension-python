"""Base class for all native API classes."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import ClassVar


@dataclass
class CustomEventData:
    pass


class APISchema:
    """Base class for all native API classes."""

    ID: ClassVar[str]

    def asdict(self, keep_null_key: bool = False) -> dict:
        """Generate dict object from this.

        :param keep_null_key: Whether to keep keys with null values.
        """
        if not is_dataclass(self):
            raise TypeError(f"{self.__class__.__name__} is not a dataclass")
        data = asdict(self)  # type: ignore[invalid-argument-type] - Previous ``if`` block may pass only dataclasses instances.
        if not keep_null_key:
            data = {k: v for k, v in data.items() if v is not None}
        return data
