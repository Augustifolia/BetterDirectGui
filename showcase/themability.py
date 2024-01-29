#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

# from direct.gui.DirectButton import DirectButton
# from direct.gui.DirectEntry import DirectEntry
# from direct.gui.DirectCheckButton import DirectCheckButton
# from direct.gui.DirectDialog import OkDialog
# from direct.gui.DirectScrollBar import DirectScrollBar
# from direct.gui.DirectScrolledFrame import DirectScrolledFrame
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
        self.pg215 = DirectButton(
            pos=LPoint3f(-0.85, 0, 0.5),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=rootParent,
            pressEffect=1,
        )

        self.pg1415 = DirectEntry(
            pos=LPoint3f(-0.6, 0, 0.5),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            parent=rootParent,
        )

        self.pg3127 = OkDialog(
            state='normal',
            pos=LPoint3f(0.775, 0.1, 0.425),
            text='Ok Dialog',
            parent=rootParent,
        )

        self.pg2002 = DirectCheckButton(
            pos=LPoint3f(-0.625, 0, 0.325),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Checkbutton',
            parent=rootParent,
        )

        self.pg5973 = DirectScrollBar(
            pos=LPoint3f(-0.2, 0, 0.175),
            parent=rootParent,
        )

        self.pg7200 = DirectScrolledFrame(
            state='normal',
            frameColor=(1, 1, 1, 1),
            pos=LPoint3f(0, 0, -0.5),
            parent=rootParent,
        )

        self.pg216 = DirectButton(
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='button',
            parent=self.pg7200.canvas,
            pressEffect=1,
        )

    def show(self):
        self.pg215.show()
        self.pg1415.show()
        self.pg2002.show()
        self.pg3127.show()
        self.pg5973.show()
        self.pg7200.show()

    def hide(self):
        self.pg215.hide()
        self.pg1415.hide()
        self.pg2002.hide()
        self.pg3127.hide()
        self.pg5973.hide()
        self.pg7200.hide()

    def destroy(self):
        self.pg215.destroy()
        self.pg1415.destroy()
        self.pg2002.destroy()
        self.pg3127.destroy()
        self.pg5973.destroy()
        self.pg7200.destroy()


def main():
    ShowBase()
    theme = {
        "general": dict(
            text_shadow=(1, .1, 1, 1),
            frameColor=(.4, .7, .1, 1),
            relief=DGG.FLAT,
            frameTexture="models/maps/circle.png",
            transparency=True
        ),
        "DirectButton": dict(
            frameColor=(0.1, 1, 1, 1),
            borderWidth=(0.4, 0.4),
            text_scale=0.6,
            text_shadow=(1, 1, 0.1, 1),
            text_shadowOffset=(0.1, 0.1),
        ),
        "DirectEntry": dict(
            enteredText="initial text"
        ),
        "DirectCheckButton": dict(
            indicatorValue=1,
        ),
        "OkDialog": dict(
            # buttonTextList=["Ok", "No"],
            # buttonValueList=[DGG.DIALOG_OK, DGG.DIALOG_NO]
        ),
        "DirectScrollBar": dict(
            relief=DGG.SUNKEN,
            borderWidth=(0.01, 0.01),
            thumb_frameColor=(1, 1, .1, 1)
        ),
        "DirectScrolledFrame": dict(
            scrollBarWidth=0.15
        )
    }
    # set a global theme for everything
    BetterDirectGui.init(theme=theme)
    # alternatively use:
    # base.gui_controller.set_theme(theme)
    # clear a global theme:
    # base.gui_controller.clear_theme()

    gui = GUI()

    # Changing some values manually, this will override the theme
    gui.pg5973["frameColor"] = (1, 0.1, 1, 1)
    gui.pg5973["thumb_frameColor"] = (1, 0.1, 1, 1)

    button_theme = {
        "DirectButton": dict(
            frameColor=(1, 1, 1, 1),
            scale=3,  # does not have any effect because scale was already set at init time
        )
    }
    # set a different theme for the button, this will override the old theme.
    # gui.pg215.set_theme(button_theme, 1)
    # If you wish to keep the options set by the old theme, set the option "clear_old_theme" to False.
    # gui.pg215.set_theme(button_theme, 1, clear_old_theme=False)

    # clear the theme for the "Ok" button on the OkDialog, this resets all options from the last set theme
    # gui.pg3127.buttonList[0].clear_theme()
    base.run()


if __name__ == '__main__':
    main()
