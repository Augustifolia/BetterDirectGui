from __future__ import annotations

from typing import Any
from collections.abc import MutableMapping, MutableSet, MutableSequence
from copy import deepcopy

import direct.gui.OnscreenImage as oi


__all__ = ['OnscreenImage']


class OnscreenImage(oi.OnscreenImage):
    def __init__(self,
                 image=None,
                 pos=None,
                 hpr=None,
                 scale=None,
                 color=None,
                 parent=None,
                 sort=0):
        super().__init__(image,
                         pos,
                         hpr,
                         scale,
                         color,
                         parent,
                         sort)

        self._defaults: dict[str: Any] = {}
        self._set_default()

    def _set_default(self):
        self._defaults["image"] = self["image"]
        self._defaults["pos"] = self["pos"]
        self._defaults["hpr"] = self["hpr"]
        self._defaults["scale"] = self["scale"]
        self._defaults["color"] = self["color"]
        self._defaults["parent"] = self["parent"]
        self._defaults["sort"] = self["sort"]

        for key, value in self._defaults.items():
            # Trying to copy some options can cause a crash, so only copy what we have to.
            if isinstance(value, (MutableSet, MutableSequence, MutableMapping)):
                self._defaults[key] = deepcopy(value)
