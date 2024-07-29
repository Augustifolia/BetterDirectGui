"""Drag and drop system. DraggableItems can be dragged between DraggableTiles in the same group."""
from panda3d.core import MouseButton

from BetterDirectGui.DirectGui.DirectButton import DirectButton
from BetterDirectGui.DirectGui.DirectLabel import DirectLabel
from BetterDirectGui.DirectGui import DGG
from BetterDirectGui.GuiTools import GuiUtil


__all__ = ["DraggableItem", "DraggableTile"]


class DraggableTile(DirectButton):
    """
    A Widget that DraggableItems can be placed in by dropping them on the DraggableTile.

    Only Tiles and Items with the same 'group' number interact with each other.
    The 'content' of the Tile is the item that is currently placed in it.
    If self contains no item, 'content' will be 'None' instead.
    """
    _target = None

    def __init__(self, parent=None, **kw):
        optiondefs = (
            # All DraggableTiles and DraggableItems with the same number can interact with each other.
            ('group',           0,          None),
            # The item that is placed at this tile, if self is empty this is 'None'.
            ('content',         None,       self._addItem),
            ('selectable',      False,      None),
            ('frameSize', [-.1, .1, -.1, .1], None),
            ('borderWidth', (.02, .02),       None),
        )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectButton.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(DraggableTile)

        # Set up stuff related to drag and drop
        self.bind(DGG.WITHIN, self._handle_target, extraArgs=["in"])
        self.bind(DGG.WITHOUT, self._handle_target, extraArgs=["out"])

        # Apply the theme to self
        self.add_theming_options(kw, parent, DraggableTile)

    def addItem(self, item):
        """Convenience method to add some content widget to self.

        The item should be of type 'DraggableItem' for drag and drop to work properly.
        """
        self["content"] = item

    def _handle_target(self, toggle, _):
        if toggle == "in":
            self.__class__._target = self
        elif toggle == "out" and self._target == self:
            self.__class__._target = None

    def _addItem(self):
        item = self["content"]
        if item is None:
            return

        item.wrt_reparent_to(self)
        center_x, center_z = item.getCenterPosition()
        item.setPos(
            item["placementOffset"][0] - center_x,
            0,
            item["placementOffset"][1] - center_z
        )


class DraggableItem(DirectButton):
    """
    An item that can be dragged and dropped in different DraggableTiles.

    Make sure that you add your Item to a Tile by using:
        yourTile["content"] = yourItem

    Use 'placementOffset' to adjust the Item position in its' Tile. It should automatically be centered.

    Only Tiles and Items with the same 'group' number interact with each other.
    If you add some child widget to this item,
    make sure that the child does not interfere with mouse events sent to the item.
    """
    def __init__(self, parent=None, **kw):
        optiondefs = (
            # All DraggableTiles and DraggableItems with the same number can interact with each other.
            ('group',           0,         None),
            ('selectable',      True,      None),
            # An offset to apply to the items placement in a tile.
            ('placementOffset', (0, 0),    None),
            # Used to determine if two different items can be combined into a stack
            ('itemType',        0,         None),
            # The number of items that can stack in the same tile,
            # this should be the same for all items of the same itemType
            ('stackSize',       1,         None),
            # The current number of items in the stack
            ('itemCount',       1,         self._itemCount),
            # Button used to grab or release item
            ('selectButton',  DGG.B1CLICK, self._selectButton),
            # Button to grab half the stack or release a single item
            ('splitButton',   DGG.B3CLICK, self._splitButton),
        )

        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectButton.__init__(self, parent)

        self.count = self.createcomponent("count", (), None,
                                          DirectLabel, (self,),
                                          text="X",
                                          scale=0.3
                                          )

        # Call option initialization functions
        self.initialiseoptions(DraggableItem)

        # Set up some stuff for drag and drop
        self._is_dragged = False
        self._old_parent = None
        self._task = None

        self._itemCount()
        self._selectButton()
        self.guiItem.addClickButton(MouseButton.three())
        self._splitButton()

        # Apply the theme to self
        self.add_theming_options(kw, parent, DraggableItem)

    def _selectButton(self):
        button = self["selectButton"]
        if button is None:
            return
        elif isinstance(button, (list, tuple)):
            self.bind(button[0], self._grab)
            self.bind(button[1], self._release)
        else:
            self.bind(button, self._grab_or_release)

    def _splitButton(self):
        button = self["splitButton"]
        if button is None:
            return
        self.bind(button, self._split)

    def resetCountPosition(self):
        """Resets the position of the count component."""
        if self["frameSize"]:
            frameSize = self["frameSize"]
        else:
            frameSize = self.bounds

        if frameSize is None:
            frameSize = (0,) * 4

        if self.count["frameSize"]:
            count_frameSize = self.count["frameSize"]
        else:
            count_frameSize = self.count.bounds

        if count_frameSize is None:
            count_frameSize = (0,) * 4

        self.count.set_pos(frameSize[1] + (count_frameSize[0] + self.count["borderWidth"][0]) * self.count.getScale().x,
                           0,
                           frameSize[2] + (count_frameSize[2] + self.count["borderWidth"][1]) * self.count.getScale().z)

    def _itemCount(self):
        if self["stackSize"] == 1:
            self.count.hide()
        else:
            self.count.show()
        count = self["itemCount"]
        self.count["text"] = str(count)
        self.count.resetFrameSize()
        self.resetCountPosition()

    def getCenterPosition(self) -> tuple[float, float]:
        """Method to get the center position of the self."""
        if self["frameSize"]:
            frameSize = self["frameSize"]
        else:
            frameSize = self.bounds

        if frameSize is None:
            frameSize = (0,) * 4

        height = frameSize[3] - frameSize[2]
        center_z = (height / 2 + frameSize[2]) * self.getScale().z
        width = frameSize[1] - frameSize[0]
        center_x = (width / 2 + frameSize[0]) * self.getScale().x

        return center_x, center_z

    def _split(self, _):
        if not self._is_dragged:
            self._is_dragged = True

            self._old_parent = GuiUtil.get_gui(self.parent)
            assert self._old_parent is not None, f"{self} has an invalid parent node. It should be parented to a 'DraggableTile'"

            self.wrt_reparent_to(base.aspect2d)
            self._task = self.addTask(self._drag_task, "drag")

            count = self["itemCount"]
            self["itemCount"] -= count//2
            if count//2 != 0:
                other_half = self.copy()
                other_half["itemCount"] = count//2
                self._old_parent["content"] = other_half

        else:  # todo fix this
            return
            self._is_dragged = False
            new_parent = DraggableTile._target

            if new_parent is not None and new_parent["group"] != self["group"]:
                new_parent = None

            self.removeTask(self._task)
            self.setPos(self["placementOffset"][0], 0, self["placementOffset"][1])

    def _grab_or_release(self, _):
        if self._is_dragged:
            self._release(None)
        else:
            self._grab(None)

    def _grab(self, _):
        if self._is_dragged:
            return

        self._is_dragged = True
        self._old_parent = GuiUtil.get_gui(self.parent)
        assert self._old_parent is not None, f"{self} has an invalid parent node. It should be parented to a 'DraggableTile'"

        self.wrt_reparent_to(base.aspect2d)
        self._task = self.addTask(self._drag_task, "drag")

    def _release(self, _):
        if not self._is_dragged:
            return

        self._is_dragged = False
        new_parent = DraggableTile._target

        if new_parent is not None and new_parent["group"] != self["group"]:
            new_parent = None

        self.removeTask(self._task)

        if new_parent is None:
            new_parent = self._old_parent
        if new_parent["content"] is not None and new_parent["content"] is not self:

            # The item is unstackable or the itemtypes are different
            if self["stackSize"] == 1 or self["itemType"] != new_parent["content"]["itemType"]:
                if self._old_parent["content"] is self:
                    self._old_parent["content"] = new_parent["content"]
                else:  # The stack was split so there are some items left
                    new_parent["content"]._grab(None)

            # The items can be stacked
            elif self["itemCount"] + new_parent["content"]["itemCount"] <= self["stackSize"]:
                self["itemCount"] += new_parent["content"]["itemCount"]
                new_parent["content"].destroy()
                new_parent["content"] = None
                if self._old_parent["content"] is self:
                    self._old_parent["content"] = None

            # They can be stacked, but some items will be left over
            else:
                items_to_move = self["stackSize"] - new_parent["content"]["itemCount"]
                new_parent["content"]["itemCount"] = self["stackSize"]
                self["itemCount"] -= items_to_move
                self._old_parent["content"] = self
                self._grab(None)
                return

        elif self._old_parent["content"] is self:
            self._old_parent["content"] = None

        new_parent["content"] = self

    def _drag_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
        else:
            return task.cont

        center_x, center_y = self.getCenterPosition()
        self.setPos(base.render2d, x - center_x, 0, y - center_y)
        return task.cont
