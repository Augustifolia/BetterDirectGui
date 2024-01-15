from __future__ import annotations

from copy import deepcopy
from typing import Any
from collections.abc import MutableMapping, MutableSet, MutableSequence

import direct.gui.OnscreenText as ot
from panda3d.core import TextProperties

__all__ = ['OnscreenText', 'Plain', 'ScreenTitle', 'ScreenPrompt', 'NameConfirm', 'BlackOnWhite']

Plain = ot.Plain
ScreenTitle = ot.ScreenTitle
ScreenPrompt = ot.ScreenPrompt
NameConfirm = ot.NameConfirm
BlackOnWhite = ot.BlackOnWhite


class OnscreenText(ot.OnscreenText):
    def __init__(self, text = '',
                 style = ot.Plain,
                 pos = (0, 0),
                 roll = 0,
                 scale = None,
                 fg = None,
                 bg = None,
                 shadow = None,
                 shadowOffset = (0.04, 0.04),
                 frame = None,
                 align = None,
                 wordwrap = None,
                 drawOrder = None,
                 decal = 0,
                 font = None,
                 parent = None,
                 sort = 0,
                 mayChange = True,
                 direction = None):
        super().__init__(text,
                         style,
                         pos,
                         roll,
                         scale,
                         fg,
                         bg,
                         shadow,
                         shadowOffset,
                         frame,
                         align,
                         wordwrap,
                         drawOrder,
                         decal,
                         font,
                         parent,
                         sort,
                         mayChange,
                         direction)

        self._defaults: dict[str: Any] = {}
        self._set_default()

    def _set_default(self):
        self._defaults["text"] = self["text"]
        self._defaults["pos"] = self["pos"]
        self._defaults["x"] = self["x"]
        self._defaults["y"] = self["y"]
        self._defaults["roll"] = self["roll"]
        self._defaults["scale"] = self["scale"]
        self._defaults["fg"] = self["fg"]
        self._defaults["bg"] = self["bg"]
        self._defaults["shadow"] = self["shadow"]
        self._defaults["shadowOffset"] = self["shadowOffset"]
        self._defaults["frame"] = self["frame"]
        self._defaults["align"] = self["align"]
        self._defaults["wordwrap"] = self["wordwrap"]
        self._defaults["drawOrder"] = self["drawOrder"]
        self._defaults["decal"] = self["decal"]
        self._defaults["font"] = self["font"]
        self._defaults["parent"] = self["parent"]
        self._defaults["sort"] = self["sort"]
        # self._defaults["mayChange"] = self["mayChange"]
        self._defaults["direction"] = self["direction"]

        for key, value in self._defaults.items():
            # Trying to copy some options can cause a crash, so only copy what we have to.
            if isinstance(value, (MutableSet, MutableSequence, MutableMapping)):
                self._defaults[key] = deepcopy(value)

    def get_default(self, option: str) -> Any:
        return self._defaults[option]

    def cget(self, option):
        # Get current configuration setting.
        # This is for compatibility with DirectGui functions
        func_name = 'get' + option[0].upper() + option[1:]
        if hasattr(self, func_name):
            getter = getattr(self, func_name)
        else:
            getter = getattr(self, "_OnscreenText__" + func_name)
        return getter()

    __getitem__ = cget

    def setShadowOffset(self, values: tuple | list):
        if self["shadow"][3] != 0:
            self.textNode.setShadow(*values)
        else:
            self.textNode.clearShadow()

    def getShadowOffset(self):
        return self.textNode.getShadow()

    def setDrawOrder(self, value: int):
        self.textNode.setDrawOrder(value)

    def getDrawOrder(self):
        return self.textNode.getDrawOrder()

    def setShadow(self, shadow):
        if shadow[3] != 0:
            # If we have a shadow color, create a shadow.
            self.textNode.setShadowColor(shadow[0], shadow[1], shadow[2], shadow[3])
            # self.textNode.setShadow(0.04, 0.04)
            self.textNode.setShadow(*self["shadowOffset"])
        else:
            # Otherwise, remove the shadow.
            self.textNode.clearShadow()

    def setDirection(self, direction):
        """Toggle to make the text go from left to right or right to left. Requires harfbuzz to be enabled."""
        if direction is not None:
            if isinstance(direction, str):
                direction = direction.lower()
                if direction == 'rtl':
                    direction = TextProperties.D_rtl
                elif direction == 'ltr':
                    direction = TextProperties.D_ltr
                else:
                    raise ValueError('invalid direction')
            self.textNode.setDirection(direction)

    def getDirection(self):
        return self.textNode.getDirection()
