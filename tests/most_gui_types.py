#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG
from BetterDirectGui.DirectGui import *
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)


def test():
    print("pressed button")


class GUI:
    def __init__(self, rootParent=None):
        
        self.pg196 = DirectButton(
            pos = LPoint3f(-1.125, 0, 0.675),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'button',
            parent=rootParent,
            pressEffect=1,
            command=test
        )
        self.pg196.setTransparency(0)
        self.pg196["pressEffect"] = 1
        self.pg196["pressEffect"] = 0

        self.pg1363 = DirectEntry(
            pos = LPoint3f(-0.85, 0, 0.65),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            parent=rootParent,
        )
        self.pg1363.setTransparency(0)

        self.pg2152 = DirectEntry(
            # parent=self.pg2153,
            initialText="hello"
        )
        print(self.pg2152["enteredText"])
        self.pg2152["enteredText"] = "some string"
        print(self.pg2152["enteredText"])
        self.pg2152.set("other")
        print(self.pg2152["enteredText"])
        self.pg2152.setTransparency(0)
        self.pg2153 = DirectEntryScroll(
            parent=rootParent,
            scale=LVecBase3f(0.1, 0.1, 0.1),
            entry=self.pg2152,
        )
        self.pg2153.setTransparency(0)
        self.pg2152.reparentTo(self.pg2153)

        self.pg2627 = DirectCheckBox(
            pos = LPoint3f(0.525, 0, 0.675),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            parent=rootParent,
            uncheckedImage="models/maps/circle.png",
            checkedImage="models/maps/envir-bamboo.png"
        )
        self.pg2627.setTransparency(0)
        self.pg2627["pressEffect"] = 1

        self.pg3182 = DirectCheckButton(
            pos = LPoint3f(-0.9, 0, 0.5),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'Checkbutton',
            parent=rootParent
        )
        self.pg3182.setTransparency(0)
        self.pg3182["pressEffect"] = 1

        self.pg5339 = DirectOptionMenu(
            pos = LPoint3f(-0.525, 0, 0.5),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            popupMarker_pos = None,
            text_align = 0,
            parent=rootParent,
            items=["button1", "button2", "button3"]
        )
        self.pg5339.setTransparency(0)
        self.pg5339["selectedItem"] = "button2"
        print(self.pg5339["selectedItem"])
        self.pg5339["pressEffect"] = 1

        self.pg8076 = DirectRadioButton(
            pos = LPoint3f(0.225, 0, 0.475),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'Radiobutton',
            others = [],
            parent=rootParent,
            variable=[],
            value=[],
        )
        self.pg8076.setTransparency(0)

        self.pg9880 = DirectSlider(
            pos = LPoint3f(-0.05, 0, 0.25),
            text = 'Slider',
            text0_scale = (0.1, 0.1),
            parent=rootParent,
        )
        self.pg9880.setTransparency(0)

        self.pg11012 = DirectScrollBar(
            pos = LPoint3f(-0.45, 0, 0.05),
            parent=rootParent,
        )
        self.pg11012.setTransparency(0)

        self.pg12261 = DirectLabel(
            pos = LPoint3f(0.35, 0, 0.075),
            scale = LVecBase3f(0.1, 0.1, 0.1),
            text = 'Label',
            parent=rootParent,
        )
        self.pg12261.setTransparency(0)

        self.pg12869 = DirectWaitBar(
            state = 'normal',
            pos = LPoint3f(-0.05, 0, -0.1),
            text = '0%',
            text0_scale = (0.1, 0.1),
            parent=rootParent,
        )
        self.pg12869.setTransparency(0)

        self.pg13530 = DirectFrame(
            frameSize = (-0.2, 0.2, -0.2, 0.2),
            frameColor = (1, 1, 1, 1),
            pos = LPoint3f(-1, 0, -0.45),
            parent=rootParent,
        )
        self.pg13530.setTransparency(0)

        self.pg14617 = DirectScrolledFrame(
            state = 'normal',
            frameSize = (-0.2, 0.2, -0.2, 0.2),
            frameColor = (1, 1, 1, 1),
            pos = LPoint3f(-0.5, 0, -0.45),
            parent=rootParent,
        )
        self.pg14617.setTransparency(0)

        self.pg16851 = DirectScrolledList(
            state = 'normal',
            frameSize = (-0.5, 0.5, -0.01, 0.75),
            pos = LPoint3f(0.25, 0, -0.95),
            forceHeight = 0.1,
            numItemsVisible = 5,
            text = 'scrolled list',
            decButton_borderWidth = (0.005, 0.005),
            decButton_pos = LPoint3f(-0.45, 0, 0.03),
            decButton_text = 'Prev',
            decButton_text0_scale = (0.05, 0.05),
            decButton_text0_align = 0,
            decButton_text1_scale = (0.05, 0.05),
            decButton_text1_align = 0,
            decButton_text2_scale = (0.05, 0.05),
            decButton_text2_align = 0,
            decButton_text3_scale = (0.05, 0.05),
            decButton_text3_align = 0,
            incButton_borderWidth = (0.005, 0.005),
            incButton_pos = LPoint3f(0.45, 0, 0.03),
            incButton_text = 'Next',
            incButton_text0_scale = (0.05, 0.05),
            incButton_text0_align = 1,
            incButton_text1_scale = (0.05, 0.05),
            incButton_text1_align = 1,
            incButton_text2_scale = (0.05, 0.05),
            incButton_text2_align = 1,
            incButton_text3_scale = (0.05, 0.05),
            incButton_text3_align = 1,
            itemFrame_frameSize = (-0.47, 0.47, -0.5, 0.1),
            itemFrame_frameColor = (1, 1, 1, 1),
            itemFrame_pos = LPoint3f(0, 0, 0.6),
            text0_scale = (0.1, 0.1),
            parent=rootParent,
        )
        self.pg16851.setTransparency(0)

        l1 = DirectLabel(text="Test1", text_scale=0.1)
        l2 = DirectLabel(text="Test2", text_scale=0.1)
        l3 = DirectLabel(text="Test3", text_scale=0.1)
        l4 = DirectLabel(text="Test4", text_scale=0.1)
        l5 = DirectLabel(text="Test5", text_scale=0.1)
        l6 = DirectLabel(text="Test6", text_scale=0.1)

        self.pg16851.addItem(l1)
        self.pg16851.addItem(l2)
        self.pg16851.addItem(l3)
        self.pg16851.addItem(l4)
        self.pg16851.addItem(l5)
        self.pg16851.addItem(l6)
        self.pg16851["itemsWordwrap"] = 4
        self.pg16851["itemsAlign"] = TextNode.ARight

        self.pg18888 = OkDialog(
            state = 'normal',
            pos = LPoint3f(0.9, 0.1, 0.675),
            text = 'Ok Dialog',
            parent=rootParent,
            buttonTextList=["b1"],
            buttonSize=(-.1, .1, -.1, .1)
        )
        self.pg18888.setTransparency(0)
        self.pg18888["topPad"] = 0.4
        self.pg18888["sidePad"] = 0.1
        self.pg18888["midPad"] = 0.1
        self.pg18888["buttonPadSF"] = 1.1
        self.pg18888["buttonSize"] = (-.1, .1, -.1, .1)
        self.pg18888["buttonTextList"] = ["b1", "b2", "b3"]

    def show(self):
        self.pg196.show()
        self.pg1363.show()
        self.pg2153.show()
        self.pg2627.show()
        self.pg3182.show()
        self.pg5339.show()
        self.pg8076.show()
        self.pg9880.show()
        self.pg11012.show()
        self.pg12261.show()
        self.pg12869.show()
        self.pg13530.show()
        self.pg14617.show()
        self.pg16851.show()
        self.pg18888.show()

    def hide(self):
        self.pg196.hide()
        self.pg1363.hide()
        self.pg2153.hide()
        self.pg2627.hide()
        self.pg3182.hide()
        self.pg5339.hide()
        self.pg8076.hide()
        self.pg9880.hide()
        self.pg11012.hide()
        self.pg12261.hide()
        self.pg12869.hide()
        self.pg13530.hide()
        self.pg14617.hide()
        self.pg16851.hide()
        self.pg18888.hide()

    def destroy(self):
        self.pg196.destroy()
        self.pg1363.destroy()
        self.pg2153.destroy()
        self.pg2627.destroy()
        self.pg3182.destroy()
        self.pg5339.destroy()
        self.pg8076.destroy()
        self.pg9880.destroy()
        self.pg11012.destroy()
        self.pg12261.destroy()
        self.pg12869.destroy()
        self.pg13530.destroy()
        self.pg14617.destroy()
        self.pg16851.destroy()
        self.pg18888.destroy()
