#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

# from direct.gui.DirectScrolledFrame import DirectScrolledFrame
# from direct.gui.DirectButton import DirectButton
# from direct.gui.DirectEntry import DirectEntry
# from direct.gui.DirectSlider import DirectSlider
from BetterDirectGui.DirectGui import *
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

from direct.showbase.ShowBase import ShowBase
import BetterDirectGui


class GUI:
    def __init__(self, rootParent=None):
        self.pg1641 = DirectScrolledFrame(
            state='normal',
            frameColor=(1, 1, 1, 1),
            pos=LPoint3f(0, 0, 0),
            frameSize=(-.8, .8, -.8, .8),
            parent=rootParent,
        )
        self.pg1641.setTransparency(0)

        self.pg7323 = DirectButton(
            pos=LPoint3f(-0.35, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=self.pg1641.canvas,
            pressEffect=1,
        )
        self.pg7323.setTransparency(0)

        self.pg7363 = DirectEntry(
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            parent=self.pg1641.canvas,
        )
        self.pg7363.setTransparency(0)

        self.pg8605 = DirectButton(
            pos=LPoint3f(-0.35, 0, -0.225),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=self.pg1641.canvas,
            pressEffect=1,
        )
        self.pg8605.setTransparency(0)

        self.pg8655 = DirectEntry(
            pos=LPoint3f(0, 0, -0.225),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            parent=self.pg1641.canvas,
        )
        self.pg8655.setTransparency(0)

        self.pg11625 = DirectSlider(
            pos=LPoint3f(0.175, 0, -0.45),
            text='Slider',
            text0_scale=(0.1, 0.1),
            parent=self.pg1641.canvas,
        )
        self.pg11625.setTransparency(0)

        self.pg1674 = DirectButton(
            pos=LPoint3f(1.225, 0, 0.9),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=rootParent,
            pressEffect=1,
        )
        self.pg1674.setTransparency(0)

        self.pg2514 = DirectButton(
            pos=LPoint3f(1.225, 0, 0.7),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=rootParent,
            pressEffect=1,
        )
        self.pg2514.setTransparency(0)

        self.pg12850 = DirectButton(
            pos=LPoint3f(1.225, 0, 0.5),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=rootParent,
            pressEffect=1,
        )
        self.pg12850.setTransparency(0)

        self.pg13801 = DirectButton(
            pos=LPoint3f(1.225, 0, 0.3),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=rootParent,
            pressEffect=1,
        )
        self.pg13801.setTransparency(0)

    def show(self):
        self.pg1641.show()
        self.pg1674.show()
        self.pg2514.show()
        self.pg12850.show()
        self.pg13801.show()

    def hide(self):
        self.pg1641.hide()
        self.pg1674.hide()
        self.pg2514.hide()
        self.pg12850.hide()
        self.pg13801.hide()

    def destroy(self):
        self.pg1641.destroy()
        self.pg1674.destroy()
        self.pg2514.destroy()
        self.pg12850.destroy()
        self.pg13801.destroy()


def main():
    ShowBase()
    BetterDirectGui.init()
    GUI()
    base.run()


if __name__ == '__main__':
    main()
