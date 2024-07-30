#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from BetterDirectGui.DirectGui.DirectScrolledFrame import DirectScrolledFrame
from BetterDirectGui.DirectGui.DirectButton import DirectButton
from BetterDirectGui.DirectGui.DirectEntry import DirectEntry
from BetterDirectGui.DirectGui.DirectFrame import DirectFrame
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)


class GUI:
    def __init__(self, rootParent=None):
        
        self.pg298 = DirectScrolledFrame(
            # state = 'normal',
            # frameSize = (1, 1, 1, 1),
            # pos = LPoint3f(0, 0, 0),
            # borderWidth=(.03, .03),
            # scale=2,
            parent=rootParent,
        )
        self.pg298.setTransparency(0)

        self.pg714 = DirectButton(
            pos = LPoint3f(-.675, 0, 0.8),
            # scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'button',
            # parent=self.pg298.canvas,
            # pressEffect=1,
        )
        self.pg714.setTransparency(0)
        self.pg714.reparentTo(self.pg298.canvas)

        self.pg1911 = DirectEntry(
            pos = LPoint3f(-1.075, 0, 0.525),
            # scale = LVecBase3f(0.1, 0.1, 0.1),
            parent=self.pg298.canvas,
        )
        self.pg1911.setTransparency(0)

        self.pg2861 = DirectButton(
            pos = LPoint3f(-0.75, 0, 0.25),
            # scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'button',
            parent=self.pg298.canvas,
            # pressEffect=1,
        )
        self.pg2861.setTransparency(0)

        self.pg4088 = DirectFrame(
            frameSize = (-1, 1, -1, 1),
            frameColor = (1, 1, 1, 1),
            pos = LPoint3f(0.975, 0, 0.075),
            # scale=0.5,
            parent=self.pg298.canvas,
        )
        self.pg4088.setTransparency(0)

        self.pg4417 = DirectButton(
            pos = LPoint3f(-0.525, 0, 0.425),
            # scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'button',
            parent=self.pg4088,
            # pressEffect=1,
        )
        self.pg4417.setTransparency(0)

        self.pg5438 = DirectEntry(
            pos = LPoint3f(-0.775, 0, 0.075),
            # scale = LVecBase3f(0.1, 0.1, 0.1),
            parent=self.pg4088,
        )
        self.pg5438.setTransparency(0)


    def show(self):
        self.pg298.show()

    def hide(self):
        self.pg298.hide()

    def destroy(self):
        self.pg298.destroy()
