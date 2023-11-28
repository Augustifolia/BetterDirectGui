#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

# from direct.gui.DirectSlider import DirectSlider
# from direct.gui.DirectScrollBar import DirectScrollBar
from BetterDirectGui.DirectGui import *
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)


class GUI:
    def __init__(self, rootParent=None):
        self.pg215 = DirectSlider(
            pos=LPoint3f(0, 0, 0),
            text='Slider',
            text0_scale=(0.1, 0.1),
            parent=rootParent,
            orientation="vertical"
        )
        self.pg215.setTransparency(0)

        self.pg573 = DirectSlider(
            pos=LPoint3f(-0.01, 0, -0.175),
            text='Slider',
            text0_scale=(0.1, 0.1),
            parent=rootParent,
            # orientation="vertical_inverted"
        )
        self.pg573.setTransparency(0)

        self.pg2338 = DirectScrollBar(
            pos=LPoint3f(0.025, 0, 0.225),
            parent=rootParent,
        )
        self.pg2338.setTransparency(0)

        self.pg3482 = DirectScrollBar(
            pos=LPoint3f(0, 0, 0.375),
            parent=rootParent,
            # orientation="horizontal_inverted"
        )
        self.pg3482.setTransparency(0)

        self.pg5250 = DirectScrollBar(
            pos=LPoint3f(1.15, 0, 0.5),
            orientation='vertical',
            parent=rootParent,
        )
        self.pg5250.setTransparency(0)

        self.pg5303 = DirectScrollBar(
            pos=LPoint3f(0.875, 0, 0.525),
            orientation='vertical_inverted',
            parent=rootParent,
        )
        self.pg5303.setTransparency(0)

    def show(self):
        self.pg215.show()
        self.pg573.show()
        self.pg2338.show()
        self.pg3482.show()
        self.pg5250.show()
        self.pg5303.show()

    def hide(self):
        self.pg215.hide()
        self.pg573.hide()
        self.pg2338.hide()
        self.pg3482.hide()
        self.pg5250.hide()
        self.pg5303.hide()

    def destroy(self):
        self.pg215.destroy()
        self.pg573.destroy()
        self.pg2338.destroy()
        self.pg3482.destroy()
        self.pg5250.destroy()
        self.pg5303.destroy()