"""Package generator."""

from __future__ import annotations

import sys
from dataclasses import is_dataclass
from importlib import import_module
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neutralinojs_extension.native_api._base import APISchema


def generate_exports(package_dir: Path) -> dict[str, type[APISchema]]:
    from neutralinojs_extension.native_api._base import APISchema

    def is_schema_class(cls):
        return is_dataclass(cls) and issubclass(cls, APISchema)

    modules: list[tuple] = [
        (
            module_file.stem,
            import_module(f"neutralinojs_extension.native_api.{module_file.stem}"),
        )
        for module_file in package_dir.glob("*.py")
        if not module_file.name.startswith("_")
    ]
    classes: list[list[tuple]] = [
        [
            (f"{name.capitalize()}_{attr}", getattr(module, attr))
            for attr in dir(module)
            if is_schema_class(getattr(module, attr))
        ]
        for name, module in modules
    ]
    return {name: cls for name, cls in chain.from_iterable(classes)}


target = Path(__file__).parents[1] / "src/neutralinojs_extension/native_api/__init__.py"
template = '''"""Definition of data types for calling native APIs.

.. note::

    This package does not have all definitions because they are used only type hints.
    I will add them when I want to add, but I accept PR for them if you want.

:ref: https://neutralino.js.org/docs/api/overview
"""

from __future__ import annotations

{imports}

__all__ = [
{class_names}
]
'''

before = target.read_text()
target.write_text("")
exports = generate_exports(target.parent)
imports = "\n".join(
    f"from .{cls.__module__.split('.')[-1]} import {cls.__name__} as {name}"
    for name, cls in exports.items()
)
class_names = "\n".join(f'    "{name}",' for name in exports.keys())
after = template.format(imports=imports, class_names=class_names)
target.write_text(after)

sys.stderr.write(f"{target} has updates, please add it to commit.")
sys.exit(0 if before == after else 1)
