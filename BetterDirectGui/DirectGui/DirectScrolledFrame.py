"""Contains the DirectScrolledFrame class.

See the :ref:`directscrolledframe` page in the programming manual for a more
in-depth explanation and an example of how to use this class.
"""

__all__ = ['DirectScrolledFrame']

from panda3d.core import *
from direct.gui import DirectGuiGlobals as DGG
from .DirectFrame import *
from .DirectScrollBar import *

DGG.MWUP = PGButton.getPressPrefix() + MouseButton.wheel_up().getName() + '-'
DGG.MWDOWN = PGButton.getPressPrefix() + MouseButton.wheel_down().getName() + '-'


"""
import DirectScrolledFrame
d = DirectScrolledFrame(borderWidth=(0, 0))
"""


class DirectScrolledFrame(DirectFrame):
    """
    DirectScrolledFrame -- a special frame that uses DirectScrollBar to
    implement a small window (the frameSize) into a potentially much
    larger virtual canvas (the canvasSize, scrolledFrame.getCanvas()).

    Unless specified otherwise, scroll bars are automatically created
    and managed as needed, based on the relative sizes od the
    frameSize and the canvasSize.  You can also set manageScrollBars =
    0 and explicitly position and hide or show the scroll bars
    yourself.
    """
    def __init__(self, parent = None, **kw):
        optiondefs = (
            # Define type of DirectGuiWidget
            ('pgFunc',         PGScrollFrame,      None),
            ('frameSize',      (-0.5, 0.5, -0.5, 0.5), None),

            ('canvasSize',     (-1, 1, -1, 1),        self.setCanvasSize),
            ('manageScrollBars', 1,                self.setManageScrollBars),
            ('autoHideScrollBars', 1,              self.setAutoHideScrollBars),
            ('scrollBarWidth', 0.08,               self.setScrollBarWidth),
            ('borderWidth',    (0.01, 0.01),       self.setBorderWidth),
            ('enableScrollWheel', True,            self.enableScroll),
            ('horizontalScrollKey', 'shift',       self.enableScroll),
            )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectFrame.__init__(self, parent)

        # The scrollBarWidth parameter is just used at scroll bar
        # construction time, and supplies a default frame.  It does
        # not override an explicit frame specified on the scroll bar.
        # If you want to change the frame width after construction,
        # you must specify their frameSize tuples explicitly.
        w = self['scrollBarWidth']

        self.verticalScroll = self.createcomponent(
            "verticalScroll", (), None,
            DirectScrollBar, (self,),
            borderWidth = self['borderWidth'],
            frameSize = (-w / 2.0, w / 2.0, -1, 1),
            orientation = DGG.VERTICAL)

        self.horizontalScroll = self.createcomponent(
            "horizontalScroll", (), None,
            DirectScrollBar, (self,),
            borderWidth = self['borderWidth'],
            frameSize = (-1, 1, -w / 2.0, w / 2.0),
            orientation = DGG.HORIZONTAL)

        self.guiItem.setVerticalSlider(self.verticalScroll.guiItem)
        self.guiItem.setHorizontalSlider(self.horizontalScroll.guiItem)

        self.canvas = NodePath(self.guiItem.getCanvasNode())

        # Call option initialization functions
        self.initialiseoptions(DirectScrolledFrame)
        # Apply the theme to self
        self.add_theming_options(kw, parent, DirectScrolledFrame)

        self.verticalScroll._comp_update_func = self._verticalScroll_comp_update_func
        self.horizontalScroll._comp_update_func = self._horizontalScroll_comp_update_func

    def _verticalScroll_comp_update_func(self, **kwargs):
        if self["manageScrollBars"]:
            return

        self.verticalScroll._comp_update_func(**kwargs)

    def _horizontalScroll_comp_update_func(self, **kwargs):
        if self["manageScrollBars"]:
            return

        self.horizontalScroll._comp_update_func(**kwargs)

    def scrollStep(self, direction, steps):
        if direction == "v":
            active_bar = self.verticalScroll
        elif direction == "h":
            active_bar = self.horizontalScroll
        else:
            raise ValueError("An invalid value for 'direction' was passed, it should be the string 'v' or 'h'")

        active_bar.scrollStep(steps)

    def setup_scroll_bind(self, item):
        if not self["enableScrollWheel"]:
            return False

        if item.isUnbound(DGG.MWUP) and item.isUnbound(DGG.MWDOWN):
            item.bind(DGG.MWUP, self._scroll, extraArgs=[-1])
            item.bind(DGG.MWDOWN, self._scroll, extraArgs=[1])
            return True

        return False

    def _scroll(self, step, _):
        speed = 5
        if base.mouseWatcherNode.is_button_down(self["horizontalScrollKey"]):
            direction = "h"
            if self.horizontalScroll.isHidden():
                return
        else:
            direction = "v"
            if self.verticalScroll.isHidden():
                return

        self.scrollStep(direction, step * speed)

    def enableScroll(self):
        element_list = [
            self,
            self.verticalScroll,
            self.verticalScroll.thumb,
            # self.verticalScroll.incButton,  # scrolling does not really work with these buttons
            # self.verticalScroll.decButton,
            self.horizontalScroll,
            self.horizontalScroll.thumb,
            # self.horizontalScroll.incButton,
            # self.horizontalScroll.decButton,
        ]

        if self["enableScrollWheel"]:
            for node in element_list:
                node.bind(DGG.MWUP, self._scroll, extraArgs=[-1])
                node.bind(DGG.MWDOWN, self._scroll, extraArgs=[1])

            # set state to 'normal' to be able to catch scroll events
            self["state"] = DGG.NORMAL

        else:
            for node in element_list:
                node.unbind(DGG.MWUP)
                node.unbind(DGG.MWDOWN)

    def addItem(self, item):
        item.reparentTo(self.canvas)
        self.setup_scroll_bind(item)

    def setScrollBarWidth(self):
        if self.fInit: return

        w = self['scrollBarWidth']
        self.verticalScroll["frameSize"] = (-w / 2.0, w / 2.0, self.verticalScroll["frameSize"][2], self.verticalScroll["frameSize"][3])
        self.horizontalScroll["frameSize"] = (self.horizontalScroll["frameSize"][0], self.horizontalScroll["frameSize"][1], -w / 2.0, w / 2.0)

    def setCanvasSize(self):
        f = self['canvasSize']
        self.guiItem.setVirtualFrame(f[0], f[1], f[2], f[3])

    def getCanvas(self):
        """Returns the NodePath of the virtual canvas.  Nodes parented to this
        canvas will show inside the scrolled area.
        """
        return self.canvas

    def setManageScrollBars(self):
        self.guiItem.setManagePieces(self['manageScrollBars'])

    def setAutoHideScrollBars(self):
        self.guiItem.setAutoHide(self['autoHideScrollBars'])

    def commandFunc(self):
        if self['command']:
            self['command'](*self['extraArgs'])

    def destroy(self):
        # Destroy children of the canvas
        for child in self.canvas.getChildren():
            childGui = self.guiDict.get(child.getName())
            if childGui:
                childGui.destroy()
            else:
                parts = child.getName().split('-')
                simpleChildGui = self.guiDict.get(parts[-1])
                if simpleChildGui:
                    simpleChildGui.destroy()
        if self.verticalScroll:
            self.verticalScroll.destroy()
        if self.horizontalScroll:
            self.horizontalScroll.destroy()
        self.verticalScroll = None
        self.horizontalScroll = None
        DirectFrame.destroy(self)
